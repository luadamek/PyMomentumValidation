def convert_df_to_data(df):
    data = {}
    for c in df.columns:
        data[c] = df[c].values
    return data

def put_data_back_in_df(data, df):
    for c in data:
        print(c)
        df[c] = data[c]
    return df

def inject_bias(df, region, injection_function):
    from BiasInjection import injection_histogram
    injection_histogram = injection_function(region)
    if region == "ID":
        pos_varx = calc_pos_id_eta
        neg_varx = calc_neg_id_eta
        pos_vary = calc_pos_id_phi
        neg_vary = calc_neg_id_phi
    elif region == "MS":
        pos_varx = calc_pos_ms_eta
        neg_varx = calc_neg_ms_eta
        pos_vary = calc_pos_ms_phi
        neg_vary = calc_neg_ms_phi
    else: raise ValueError()
    correction = SagittaBiasCorrection([injection_histogram],  pos_varx, neg_varx, pos_vary, neg_vary, pos_selections = [], neg_selections = [],flavour = region)
    data = convert_df_to_data(df)
    data = correction.calibrate(data)
    df = put_data_back_in_df(data, df)
    return df

def add_pair_mass(df):
    from variables import calc_ms_mass
    data = convert_df_to_data(df)
    data["Pair_MS_Mass"] = calc_ms_mass.eval(data)
    df = put_data_back_in_df(data, df)
    print(df["Pair_MS_Mass"].values)
    return df

def get_histogram_function(inject):
    from BiasInjection import injection_histogram_local, injection_histogram_global, injection_histogram_globalpluslocal, injection_histogram_null, injection_histogram_data
    if inject == "Global": injection_function = injection_histogram_global
    if inject == "GlobalPlusLocal": injection_function = injection_histogram_globalpluslocal
    if inject == "Local": injection_function = injection_histogram_local
    if inject == "Null": injection_function = injection_histogram_null
    if inject == "Data": injection_function = injection_histogram_data
    return injection_function

def get_df_for_job(args):
    if (args.inject != "") and (args.inject != None) and (args.inject != "None"):
        injection_histogram_function = get_histogram_function(args.inject)

    variables = ["Pos_{}_Eta", "Neg_{}_Eta", "Pos_{}_Phi", "Neg_{}_Phi", "Pos_{}_Pt", "Neg_{}_Pt", "Pair_{}_Mass", "TotalWeight"] #all of the variables needed
    mean_mass = 91.2 # GeV
    if args.detector_location == "MS": mean_mass = 86.0 # GeV
    selection = "abs(Pair_{}_Mass - {}) < 20.0".format(args.detector_location, mean_mass)
    variables = [v.format(args.detector_location) for v in variables]

    if args.detector_location == "ID": eta_edges = eta_edges_ID
    else: eta_edges = eta_edges_else
    phi_edges = phi_edges

    do_add_pair_mass = False
    if "v03" in args.filename and "v2" in args.filename and "Pair_MS_Mass" in variables:
        variables.remove("Pair_MS_Mass")
        do_add_pair_mass = True

    df = get_dataframe(args.filename, args.start, args.stop, variables, "")
    if "v03" in args.filename and "v2" in args.filename and do_add_pair_mass:
        df = add_pair_mass(df)

    if (args.inject != "") and (args.inject != None) and (args.inject != "None"):
        df = inject_bias(df, args.detector_location, injection_histogram_function)

    df = df.query(selection)

    return df, eta_edges, phi_edges
