from variables import recalc_id_mass, recalc_me_mass, calc_recalc_id_mass, calc_recalc_me_mass, calc_recalc_cb_mass, recalc_cb_mass

class RecalculateMasses:

    #the histogram is a segitta bias correction map for delta s
    def __init__(self):
        self.branches = self.get_branches()

    def get_branches(self):
        branches = []
        for region in ["ID", "ME", "CB"]:
            branches+=calc_recalc_id_mass.branches
            branches+=calc_recalc_me_mass.branches
            branches+=calc_recalc_cb_mass.branches
        return branches

    def calibrate(self, data):
        print("Applying the default combination")

        for region, calc in zip(["ID", "CB", "ME"], [calc_recalc_id_mass, calc_recalc_cb_mass, calc_recalc_me_mass]):
            variable_name = "Pair_{}_Mass".format(region)
            if variable_name in data: data[variable_name] = calc.eval(data)

        return data
