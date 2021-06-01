from variables import recalc_id_mass, recalc_me_mass, calc_recalc_id_mass, calc_recalc_me_mass, calc_recalc_cb_mass, recalc_cb_mass
import xgboost as xgb
import numpy as np


class BDTCombination:

    #the histogram is a segitta bias correction map for delta s
    def __init__(self, model):
        self.branches = self.get_branches()
        self.model = model

    def get_branches(self):
        branches = []
        for region in ["ID", "ME", "CB"]:
            for calib in ["Pos_{}_Pt", "Neg_{}_Pt"]:

                branches.append(calib.format(region))
                branches+=calc_recalc_id_mass.branches
                branches+=calc_recalc_me_mass.branches
                branches+=calc_recalc_cb_mass.branches
        return branches

    def calibrate(self, data, region=None):

        with open(self.model, "rb") as f:
            import pickle as pkl
            m = pkl.load(f)

        vars_pos = {}
        vars_pos["ID_Pt"] = data["Pos_ID_Pt"]
        vars_pos["ME_Pt"] = data["Pos_ME_Pt"]
        vars_pos["ID_Eta"] = data["Pos_ID_Eta"]
        vars_pos["ME_Eta"] = data["Pos_ME_Eta"]
        vars_pos["ID_Phi"] = data["Pos_ID_Phi"]
        vars_pos["ME_Phi"] = data["Pos_ME_Phi"]
        import pandas as pd
        df = pd.DataFrame.from_dict(vars_pos)
        matrix_for_eval = xgb.DMatrix(df)
        p_pos = m.predict(matrix_for_eval, m.best_ntree_limit)
        p_pos = 1.0 / (1.0 +  np.exp(-1.0 *p_pos))

        vars_neg = {}
        vars_neg["ID_Pt"] = data["Neg_ID_Pt"]
        vars_neg["ME_Pt"] = data["Neg_ME_Pt"]
        vars_neg["ID_Eta"] = data["Neg_ID_Eta"]
        vars_neg["ME_Eta"] = data["Neg_ME_Eta"]
        vars_neg["ID_Phi"] = data["Neg_ID_Phi"]
        vars_neg["ME_Phi"] = data["Neg_ME_Phi"]
        import pandas as pd
        df = pd.DataFrame.from_dict(vars_neg)
        matrix_for_eval = xgb.DMatrix(df)
        p_neg = m.predict(matrix_for_eval, m.best_ntree_limit)
        p_neg = 1.0 / (1.0 +  np.exp(-1.0 *p_neg))

        safe_pos = (data["Pos_ME_Pt"] > 0) & ( data["Pos_ID_Pt"] > 0)
        safe_neg = (data["Neg_ME_Pt"] > 0) & ( data["Neg_ID_Pt"] > 0)

        #only modify the safe pts
        data["Pos_CB_Pt"][safe_pos] = (p_pos * (data["Pos_ID_Pt"]) + (1.0 - p_pos) * (data["Pos_ME_Pt"]))[safe_pos]
        data["Neg_CB_Pt"][safe_neg] = (p_neg * (data["Neg_ID_Pt"]) + (1.0 - p_neg) * (data["Neg_ME_Pt"]))[safe_neg]

        data["Pos_CB_Eta"][safe_pos] = data["Pos_ID_Eta"][safe_pos]
        data["Pos_CB_Phi"][safe_pos] = data["Pos_ID_Phi"][safe_pos]

        data["Neg_CB_Eta"][safe_neg] = data["Neg_ID_Eta"][safe_neg]
        data["Neg_CB_Phi"][safe_neg] = data["Neg_ID_Phi"][safe_neg]

        calc = calc_recalc_cb_mass
        region = "CB"
        variable_name = "Pair_{}_Mass".format(region)
        data[variable_name] = calc.eval(data)
        return data


