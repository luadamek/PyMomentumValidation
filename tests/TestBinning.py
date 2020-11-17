from ConstraintModelMakingUtils import Binning
import utils
import unittest

retriever = utils.get_v24_retriever()
fs = retriever.get_root_files(["_ggH125_"])
df = retriever.get_dataframe(fs, ["lepton_eta", "lepton_pt", "lepton_pt_truth_born"], handle_vector_branches=False)
pt_binning1 = [8.0, 10.0, 20.0, 100.0]
pt_binning2 = [2.0, 5.0, 80.0, 150.0]
eta_binning = [0.5, 1.0, 2.0, 2.7]
import numpy as np
import os
import pickle as pkl

subbins = []
for etal, eteah in zip(eta_binning[:-1], eta_binning[1:]):
    binning = Binning("lepton_pt", pt_binning1, None)
    subbins.append(binning)
subbins[-1] = Binning("lepton_pt", pt_binning2, None)
total_binning = Binning("abs(lepton_eta)", eta_binning, subbins)

triple_nested_binning = Binning("lepton_pt_truth_born", [0.0, 50.0, 150.0, 250.0], [total_binning, total_binning, binning])

class TestBinning(unittest.TestCase):
    def test_nested_binning(self):
        print("test_nested_binning")
        total_binning.recursively_include_overflow(True)
        bindex = total_binning.get_global_bindex(df)

        for bind in range(0, total_binning.get_global_nbins()):
             selection = total_binning.get_global_selection(bind)
             selected = df.query(selection)
             selected_indices = bindex[bindex == bind]
             print(bind)
             print(selection)
             print(len(selected_indices))
             print(len(selected))
             self.assertEqual(len(selected_indices), len(selected))

    def test_nested_binning_overflow(self):
        print("test_nested_binning_overflow")
        total_binning.recursively_include_overflow(False)
        bindex = total_binning.get_global_bindex(df)

        for bind in range(0, total_binning.get_global_nbins()):
             selection = total_binning.get_global_selection(bind)
             selected = df.query(selection)
             selected_indices = bindex[bindex == bind]
             print(bind)
             print(selection)
             print(len(selected_indices))
             print(len(selected))
             self.assertEqual(len(selected_indices), len(selected))

    def test_triple_nested_binning(self):
        triple_nested_binning.recursively_include_overflow(True)
        bindex = triple_nested_binning.get_global_bindex(df)

        for bind in range(0, triple_nested_binning.get_global_nbins()):
             selection = triple_nested_binning.get_global_selection(bind)
             selected = df.query(selection)
             selected_indices = bindex[bindex == bind]
             print(bind)
             print(selection)
             print(len(selected_indices))
             print(len(selected))
             self.assertEqual(len(selected_indices), len(selected))

    def test_triple_nested_binning_overflow(self):
        triple_nested_binning.recursively_include_overflow(False)
        bindex = triple_nested_binning.get_global_bindex(df)

        for bind in range(0, triple_nested_binning.get_global_nbins()):
             selection = triple_nested_binning.get_global_selection(bind)
             selected = df.query(selection)
             selected_indices = bindex[bindex == bind]
             print(bind)
             print(selection)
             print(len(selected_indices))
             print(len(selected))
             self.assertEqual(len(selected_indices), len(selected))

    def test_bins(self):
        self.assertEqual(2*(len(pt_binning1)-1) + (len(pt_binning2)-1), total_binning.get_global_nbins())

    def test_repr(self):
        total_binning.include_overflow = True
        bindex = total_binning.get_global_bindex(df)
        total_binning.repr_override = "|lepton_eta|"

        for bind in range(0, total_binning.get_global_nbins()):
             representation = total_binning.represent_global(bind)
             print(representation)

    def test_example_with_known_answer(self):
        import pandas as pd
        frame = {"A":[0.5, 0.5, 0.5, 1.5], "B":[1.5, 3.5, 2.5, 0.0]}
        frame = pd.DataFrame.from_dict(frame)

        binning = Binning("A", [0.0, 1.0, 2.0], [Binning("B", [1.0, 2.0, 3.0], None), Binning("B", [1.0, 2.0], None)])
        binning.recursively_include_overflow(False)
        bindex = binning.get_global_bindex(frame)
        self.assertTrue(np.all(np.array([0, -2, 1, -1])== bindex))

    def test_edges_global(self):
        for bindex in range(0, binning.get_global_nbins()):
            print(triple_nested_binning.edges_global(bindex))

    def test_variable_global(self):
        for bindex in range(0, binning.get_global_nbins()):
            print(triple_nested_binning.global_variable(bindex))


if __name__ == '__main__':
    unittest.main()

