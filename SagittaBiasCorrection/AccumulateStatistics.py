from SagittaBiasUtils import convert_df_to_data, put_data_back_in_df, get_df_for_job
import numpy as np

def calculate_rms(df, args):
    var = "Pair_{}_Mass".format(args.detector_location)
    xs = df[var].values
    weights = df["TotalWeight"].values
    rms = np.sqrt(np.average(xs**2, weights = weights) - np.average(xs, weights=weights)**2)
    return rms

def calculate_mean(df, args):
    var = "Pair_{}_Mass".format(args.detector_location)
    weights = df["TotalWeight"].values
    mean = np.average(df[var].values, weights=weights)
    return mean

from SagittaBiasUtils import get_mass_selection

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Calculate the statistics associated with the dataframe.')
    parser.add_argument('--filename', type=str, dest='filename')
    parser.add_argument('--start', type=int, dest='start')
    parser.add_argument('--stop', type=int, dest='stop')
    parser.add_argument('--detector_location', type=str, dest='detector_location')
    parser.add_argument('--output_filename', type=str, dest='output_filename')
    parser.add_argument('--inject', '-i', type=str, dest="inject", default = "", required=False)
    parser.add_argument('--correct', '-c', type=str, dest="correct", default = "", required=False)
    parser.add_argument('--resonance', '-r', type=str, dest="resonance", default="Z", required=False)
    args = parser.parse_args()

    args.selection = ""
    df, eta_bins, phi_bins = get_df_for_job(args) #get a dataframe for the statistics calculations

    #calculate the pre correction statistics
    pre_rms = calculate_rms(df, args)
    pre_mean = calculate_mean(df, args)

    var = "Pair_{}_Mass".format(args.detector_location)
    pre_var = np.array(df[var].values)

    with open(args.correct, "rb") as f:
        import pickle as pkl
        correction = pkl.load(f)

    data = convert_df_to_data(df)
    data = correction.calibrate(data)
    df = put_data_back_in_df(data, df)

    post_rms = calculate_rms(df, args)
    post_mean = calculate_mean(df, args)

    df = df.query(get_mass_selection(args))
    post_rms_selection = calculate_rms(df, args)
    post_mean_selection = calculate_mean(df, args)

    print("Previously... min: {:.4f} max {:.4f}".format(min(pre_var), max(pre_var)))
    print("Afterwards... min: {:.4f} max {:.4f}".format(min(df[var].values), max(df[var].values)))
    print("Previously... std: {:.4f} mean {:.4f}".format(np.std(pre_var), np.average(pre_var)))
    print("Afterwards... std: {:.4f} mean {:.4f}".format(np.std(df[var].values), np.average(df[var].values)))

    to_write = {"pre_rms":pre_rms, "post_rms":post_rms, "pos_rms_selection": post_rms_selection,  "pre_mean":pre_mean, "post_mean": post_mean, "args": args, "pos_mean_selection": post_mean_selection}

    with open(args.output_filename, "wb") as f:
        import pickle as pkl
        pkl.dump(to_write, f)
    print("__FINISHED__")
