import xgboost as xgb
from utils import get_files
import uproot as ur
import numpy as np

import argparse
parser = argparse.ArgumentParser(description='Submit plotting batch jobs for the MuonMomentumAnalysis plotting')
parser.add_argument('--treedepth', '-td', dest="tree_depth", type=str, required=True)
parser.add_argument('--output_name', '-on', dest="output_name", type=str, required=True)
parser.add_argument('--useqoverp', '-uqop', dest="useqoverp", action="store_true")
parser.add_argument('--test', '-t', dest="test", action="store_true")
args = parser.parse_args()

files = get_files("v05_standardvars")

training_variables = ["Pos_ID_Pt", "Neg_ID_Pt", "Pos_ID_Eta", "Neg_ID_Eta", "Pos_ID_Phi", "Neg_ID_Phi"]
training_variables += [el.replace("ID", "ME") for el in training_variables]
if args.useqoverp: training_variables += ["Pos_ID_TrackCovMatrix", "Neg_ID_TrackCovMatrix"]
training_variables += ["EvtNumber"]

ordered_training_variables = []
for key in training_variables:
    cand = key.replace("Pos_", "").replace("Neg_", "")
    if cand not in ordered_training_variables and "Number" not in cand:
       ordered_training_variables.append(cand)

total_arrays = {}
if not args.test: files = files["Data1516"] + files["Data17"] + files["Data18"]
else: files = [(files["Data1516"] + files["Data17"] + files["Data18"])[0]]
for f in files:
    training_arrays = ur.open(f)["MuonMomentumCalibrationTree"].arrays(training_variables)#, entrystart=0, entrystop=1000)
    training_arrays = {key.decode("utf-8"):training_arrays[key] for key in training_arrays}
    for key in training_arrays:
        if key not in total_arrays:
            total_arrays[key] = []
        if "CovMatrix" not in key:
            total_arrays[key].append(training_arrays[key])
        else:
            total_arrays[key].append(training_arrays[key][:,-1] * 10 ** 12)
training_arrays = {key:np.concatenate(total_arrays[key]) for key in total_arrays}
del total_arrays
n_train = len(training_arrays[training_variables[0]])


def calc_mass(arrays, weights_pos, weights_neg, isdict=False):
    if not isdict:
        pos_id_pt = arrays[0]
        neg_id_pt = arrays[1]
        pos_id_eta = arrays[2]
        neg_id_eta = arrays[3]
        pos_id_phi = arrays[4]
        neg_id_phi = arrays[5]

        pos_me_pt = arrays[6]
        neg_me_pt = arrays[7]
        pos_me_eta = arrays[8]
        neg_me_eta = arrays[9]
        pos_me_phi = arrays[10]
        neg_me_phi = arrays[11]

    else:
        pos_id_pt = arrays[training_variables[0]]
        neg_id_pt = arrays[training_variables[1]]
        pos_id_eta = arrays[training_variables[2]]
        neg_id_eta = arrays[training_variables[3]]
        pos_id_phi = arrays[training_variables[4]]
        neg_id_phi = arrays[training_variables[5]]

        pos_me_pt = arrays[training_variables[6]]
        neg_me_pt = arrays[training_variables[7]]
        pos_me_eta = arrays[training_variables[8]]
        neg_me_eta = arrays[training_variables[9]]
        pos_me_phi = arrays[training_variables[10]]
        neg_me_phi = arrays[training_variables[11]]

    print(weights_pos, weights_neg)

    pos_pt = weights_pos * pos_id_pt + (1.0 - weights_pos) * pos_me_pt
    neg_pt = weights_neg * neg_id_pt + (1.0 - weights_neg) * neg_me_pt

    mass = ( 2.0 * pos_pt * neg_pt * (np.cosh(pos_id_eta - neg_id_eta) - np.cos(pos_id_phi - neg_id_phi))) ** 0.5
    return mass


#unpack the training arrays:

def get_dmatrix(training_arrays, folds=None, nfolds=None):

    id_mass = (calc_mass(training_arrays, np.ones(n_train), np.ones(n_train), isdict=True))
    me_mass = (calc_mass(training_arrays, np.zeros(n_train), np.zeros(n_train), isdict=True))
    selection = ((np.abs(id_mass - 91.2) < 12) & (np.abs(me_mass - 91.2) < 12)) & (np.logical_not(np.isnan(me_mass))) & (np.logical_not(np.isnan(id_mass)))

    if folds is not None and nfolds is not None:
        fold_selection = np.zeros(len(selection)) > 1.0
        for f in folds:
            fold_selection |= ( (training_arrays["EvtNumber"] % nfolds) == f )
        selection = selection & (fold_selection)


    training_arrays = {key:training_arrays[key][selection] for key in  training_arrays}

    new_training_arrays = {\
"ID_Pt": [training_arrays["Pos_ID_Pt"], training_arrays["Neg_ID_Pt"]],\
"ME_Pt": [training_arrays["Pos_ME_Pt"], training_arrays["Neg_ME_Pt"]],\
"ID_Eta": [training_arrays["Pos_ID_Eta"], training_arrays["Neg_ID_Eta"]],\
"ME_Eta": [training_arrays["Pos_ME_Eta"], training_arrays["Neg_ME_Eta"]],\
"ID_Phi": [training_arrays["Pos_ID_Phi"], training_arrays["Neg_ID_Phi"]],\
"ME_Phi": [training_arrays["Pos_ME_Phi"], training_arrays["Neg_ME_Phi"]]}
    if args.useqoverp:
        new_training_arrays["ID_TrackCovMatrix"] = [training_arrays["Pos_ID_TrackCovMatrix"], training_arrays["Neg_ID_TrackCovMatrix"]]
    training_arrays = new_training_arrays


    training_arrays = {key:np.concatenate(training_arrays[key]) for key in training_arrays}
    import pandas as pd
    training_df = pd.DataFrame.from_dict(training_arrays)
    targets = np.ones((len(training_df), len(training_arrays)))
    for i, key in enumerate(ordered_training_variables):
        targets[:, i] = training_arrays[key]

    dtrain = xgb.DMatrix(training_df, np.ones(len(training_df)))

    return dtrain, training_arrays

#validation, training and testing samples: 

dvalid, validing_arrays = get_dmatrix(training_arrays, folds=[1], nfolds=3)
dtrain, training_arrays = get_dmatrix(training_arrays, folds=[0], nfolds=3)


#ok let's write some code to calculate the onective function

def gradient(params, pred_pos, pred_neg):
    '''
    '''
    masses = calc_mass(params, pred_pos, pred_neg, isdict=True)
    expectation = np.mean(masses**2)
    N = len(pred_pos) * 2
    common_term = (8.0 / N) * ( (N - 2.0)/N ) * ((masses ** 2) - expectation)
    A = ( np.cosh(params["Pos_ID_Eta"] - params["Neg_ID_Eta"]) - np.cos(params["Pos_ID_Phi"] - params["Neg_ID_Phi"]) )
    pos_grads =  common_term * (params["Pos_ID_Pt"] - params["Pos_ME_Pt"]) * ( (pred_neg * params["Neg_ID_Pt"]) + (1.0 - pred_neg) * params["Neg_ME_Pt"] ) * A
    neg_grads =  common_term * (params["Neg_ID_Pt"] - params["Neg_ME_Pt"]) * ( (pred_pos * params["Pos_ID_Pt"]) + (1.0 - pred_pos) * params["Pos_ME_Pt"] ) * A
    return pos_grads, neg_grads

def hessian(params, pred_pos, pred_neg):
    '''
    '''
    N = len(pred_pos) * 2
    common_term = (16.0 / N) * ( ( (N - 2.0)/N ) ** 2)
    A = ( np.cosh(params["Pos_ID_Eta"] - params["Neg_ID_Eta"]) - np.cos(params["Pos_ID_Phi"] - params["Neg_ID_Phi"]) )
    pos_grads =  common_term * ((params["Pos_ID_Pt"] - params["Pos_ME_Pt"]) * ( (pred_neg * params["Neg_ID_Pt"]) + (1.0 - pred_neg) * params["Neg_ME_Pt"] ) * A) ** 2
    neg_grads =  common_term * ((params["Neg_ID_Pt"] - params["Neg_ME_Pt"]) * ( (pred_pos * params["Pos_ID_Pt"]) + (1.0 - pred_pos) * params["Pos_ME_Pt"] ) * A) ** 2
    return pos_grads, neg_grads

def rms(raw_pred, dtrain):
    ''' Root mean squared log error metric.'''
    if len(raw_pred) == len(training_arrays["ID_Pt"]):
        y = training_arrays
    if len(raw_pred) == len(validing_arrays["ID_Pt"]):
        y = validing_arrays
    assert len(training_arrays["ID_Pt"]) != len(validing_arrays["ID_Pt"])

    halfway = int(len(y["ID_Pt"])/2)
    params={}
    params["Pos_ID_Pt"] = y["ID_Pt"][:halfway]
    params["Neg_ID_Pt"] = y["ID_Pt"][halfway:]
    params["Pos_ME_Pt"] = y["ME_Pt"][:halfway]
    params["Neg_ME_Pt"] = y["ME_Pt"][halfway:]

    params["Pos_ID_Eta"] = y["ID_Eta"][:halfway]
    params["Neg_ID_Eta"] = y["ID_Eta"][halfway:]
    params["Pos_ME_Eta"] = y["ME_Eta"][:halfway]
    params["Neg_ME_Eta"] = y["ME_Eta"][halfway:]

    params["Pos_ID_Phi"] = y["ID_Phi"][:halfway]
    params["Neg_ID_Phi"] = y["ID_Phi"][halfway:]
    params["Pos_ME_Phi"] = y["ME_Phi"][:halfway]
    params["Neg_ME_Phi"] = y["ME_Phi"][halfway:]
    pred = 1.0 /(1.0 + np.exp(-1.0 * raw_pred))
    masses = calc_mass(params, pred[:halfway], pred[halfway:], isdict=True)

    return "PyRMS", np.std(masses)

def rms_loss(raw_pred, dtrain):
    '''
    '''
    global training_arrays
    y = training_arrays
    halfway = int(len(training_arrays["ID_Pt"])/2)
    params = {}
    params["Pos_ID_Pt"] = y["ID_Pt"][:halfway]
    params["Neg_ID_Pt"] = y["ID_Pt"][halfway:]
    params["Pos_ME_Pt"] = y["ME_Pt"][:halfway]
    params["Neg_ME_Pt"] = y["ME_Pt"][halfway:]

    params["Pos_ID_Eta"] = y["ID_Eta"][:halfway]
    params["Neg_ID_Eta"] = y["ID_Eta"][halfway:]
    params["Pos_ME_Eta"] = y["ME_Eta"][:halfway]
    params["Neg_ME_Eta"] = y["ME_Eta"][halfway:]

    params["Pos_ID_Phi"] = y["ID_Phi"][:halfway]
    params["Neg_ID_Phi"] = y["ID_Phi"][halfway:]
    params["Pos_ME_Phi"] = y["ME_Phi"][:halfway]
    params["Neg_ME_Phi"] = y["ME_Phi"][halfway:]

    pred = 1.0 /(1.0 + np.exp(-1.0 * raw_pred))

    def finite_differences(params, pred, step=0.0005):
        add_small_epsilon = np.zeros(len(pred))
        add_small_epsilon[0] = step
        print(pred)
        pred += add_small_epsilon
        print(pred)
        masses_up = np.std((calc_mass(params, pred[:halfway], pred[halfway:], isdict=True))**2)**2
        pred -= 2.0 * add_small_epsilon
        print(pred)

        masses_down = np.std((calc_mass(params, pred[:halfway], pred[halfway:], isdict=True))**2)**2
        pred += add_small_epsilon

        grad = (masses_up - masses_down)/ (2 * step)
        grad_pos, grad_neg = gradient(params, pred[:halfway], pred[halfway:])

        print("Gradients", grad, grad_pos[0])
        return grad, grad_pos[0]

    def second_order_finite_difference(params, pred, step=0.0005):
        add_small_epsilon = np.zeros(len(pred))
        add_small_epsilon[0] = step
        pred += add_small_epsilon
        grad_up, _ =  finite_differences(params, pred, step=step/10.0)

        pred -= 2.0 * add_small_epsilon
        grad_down, _ =  finite_differences(params, pred, step=step/10.0)

        pred += add_small_epsilon

        hess_pos, hess_neg = hessian(params, pred[:halfway], pred[halfway:])

        hess = (grad_up - grad_down)/ (2 * step)

        print("Hessians", hess, hess_pos[0])
        input()

    #finite_differences(params, pred)
    #second_order_finite_difference(params, pred)
    #input()

    #finite_differences(pred, params)
    grad_pos, grad_neg = gradient(params, pred[:halfway], pred[halfway:])
    hess_pos, hess_neg = hessian(params, pred[:halfway], pred[halfway:])

    #print(grad_pos, grad_neg)
    #print(hess_pos, hess_neg)

    d_pred_d_rawpred = np.exp(-1.0 * raw_pred) / ((1 + np.exp(-1.0 * raw_pred)) ** 2)
    d2_pred_d_rawpred2 = (-1.0 * np.exp(-1.0 * raw_pred)  + 2.0 *  np.exp(-2.0 * raw_pred)) / ((1 + np.exp(-1.0 * raw_pred)) ** 3)

    grads = np.concatenate([grad_pos, grad_neg])
    grads_rawpred = d_pred_d_rawpred * grads

    hess = np.concatenate([hess_pos, hess_neg])
    hess_rawpred = grads * d2_pred_d_rawpred2 +  d_pred_d_rawpred * hess

    #print(grads_rawpred, hess_rawpred)

    masses = calc_mass(params, pred[:halfway], pred[halfway:], isdict=True)
    #masses = masses[np.abs(masses - 91.2) < 10]

    #print("Preidictions {}".format(pred))
    #print("Max prediction {}".format(max(pred)))
    #print("Min prediction {}".format(min(pred)))
    return grads_rawpred, hess_rawpred

m = xgb.train({'eta': 0.05, 'max_depth': args.tree_depth, 'subsample': 1.0, 'min_child_weight':1000, 'gamma': 0.4, 'lambda': 0.0, 'alpha': 0.0, 'nthread': 1, 'disable_default_eval_metric':1},  # any other tree method is fine.
           dtrain=dtrain,
           num_boost_round=1000,
           obj=rms_loss,
           feval=rms,
           evals=[(dtrain, 'dtrain'), (dvalid, 'dvalid')],
           early_stopping_rounds=30,\
           )
import pickle as pkl
with open(args.output_name, "wb") as f:
    pkl.dump(m, f)

