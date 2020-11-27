import utils
import unittest
from variables import calc_cos_theta_star_id, calc_cos_theta_star_ms
import numpy as np
from SagittaBiasUtils import convert_df_to_data, put_data_back_in_df

#retriever = utils.get_v24_retriever()
#fs = retriever.get_root_files(["_ggH125_"])
#df = retriever.get_dataframe(fs, ["Pos_ID_Eta", "Pos_ID_Pt", "Pos_TruthPt"], handle_vector_branches=False)
files = utils.get_files("v03_v2")
f = files["MC"][-1]
#(root_file, start, stop,  variables, selection)

variables = ["Pos_ID_Eta", "Pos_ID_Pt", "Pos_ID_Phi",\
             "Neg_ID_Eta", "Neg_ID_Pt", "Neg_ID_Phi"]
variables += ["Pos_MS_Eta", "Pos_MS_Pt", "Pos_MS_Phi",\
             "Neg_MS_Eta", "Neg_MS_Pt", "Neg_MS_Phi"]

df = utils.get_dataframe(f, 0, 200, variables, "") #read the first 200 events
data = convert_df_to_data(df)

class TestVariables(unittest.TestCase):
    def test_cos_theta_star_id_bounds(self):
        cos_theta_star_id = calc_cos_theta_star_id.eval(data)
        not_void = abs(cos_theta_star_id + 999.0) > 2.0
        print("Here are cos theta star values")
        print(cos_theta_star_id)
        self.assertTrue(np.all(cos_theta_star_id[not_void] <= 1.0))
        self.assertTrue(np.all(cos_theta_star_id[not_void] >= -1.0))

    def test_cos_theta_star_ms_bounds(self):
        cos_theta_star_ms = calc_cos_theta_star_ms.eval(data)
        not_void = abs(cos_theta_star_ms + 999.0) > 2.0
        print("Here are cos theta star values")
        print(cos_theta_star_ms)
        self.assertTrue(np.all(cos_theta_star_ms[not_void] <= 1.0))
        self.assertTrue(np.all(cos_theta_star_ms[not_void] >= -1.0))

if __name__ == '__main__':
    unittest.main()
