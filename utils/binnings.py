global_pt_binning = []
global_pt_binning.append(18.0)
global_pt_binning.append(26.0)
global_pt_binning.append(36.0)
global_pt_binning.append(45.0)
global_pt_binning.append(65.0)
global_pt_binning.append(100.0)
global_pt_binning.append(150.0)
global_pt_binning.append(200.0)
global_pt_binning.append(350.0)
global_pt_binning.append(600.0)
global_pt_binning.append(800.0)
global_pt_binning.append(1000.0)
global_pt_binning.append(2000.0)

global_pt_binning_zipped = zip(global_pt_binning[:-1], global_pt_binning[1:])

binnings = []
this_binning = {}
this_binning["name"] = "coarsest"
this_binning["EtaMS"] = {"nbins": 12, "etalow":-2.7, "etahigh":+2.7}
this_binning["EtaID"] = {"nbins": 12, "etalow":-2.5, "etahigh":+2.5}
this_binning["Phi"] = {"nbins": 8, "philow":-3.142, "phihigh":+3.142}
binnings.append(this_binning)

this_binning = {}
this_binning["name"] = "finer"
this_binning["EtaMS"] = {"nbins": 27, "etalow":-2.7, "etahigh":+2.7}
this_binning["EtaID"] = {"nbins": 25, "etalow":-2.5, "etahigh":+2.5}
this_binning["Phi"] = {"nbins": 16, "philow":-3.142, "phihigh":+3.142}
binnings.append(this_binning)

this_binning = {}
this_binning["name"] = "finest"
this_binning["EtaMS"] = {"nbins": 27, "etalow":-2.7, "etahigh":+2.7}
this_binning["EtaID"] = {"nbins": 25, "etalow":-2.5, "etahigh":+2.5}
this_binning["Phi"] = {"nbins": 32, "philow":-3.142, "phihigh":+3.142}
binnings.append(this_binning)

import numpy as np

class Binning:
    def __init__(self, variable, bin_edges, subbins, repr_override=None):
        assert (subbins is None) or (len(bin_edges) - 1 == len(subbins))
        self.variable = variable
        self.bin_edges = [b for b in bin_edges]
        if not subbins is None: self.subbins = [sb for sb in subbins]
        else: self.subbins = subbins
        self.repr_override = repr_override
        self.include_overflow = True
        self.check_for_common_variable(self.variable)

    def get_global_description(self, bindex, local_func_name, global_func_name, merger_name):
        local_bindex = 0
        global_bindex = 0
        strings = []
        if self.subbins is not None:
            for b in self.subbins:
                global_bindex += b.get_global_nbins()
                if global_bindex > bindex:
                    break
                local_bindex += 1
            local_b = self.subbins[local_bindex] #the bindex is inside of this bin

            to_subtract = 0
            for b in self.subbins[:local_bindex]:
                to_subtract += (b.get_global_nbins())
            bindex_in_bin = bindex - to_subtract
            strings.append(getattr(self, local_func_name)(local_bindex))
            strings.append(getattr(local_b, global_func_name)(bindex_in_bin))
        else:
            strings.append(getattr(self, local_func_name)(bindex))

        return getattr(self, merger_name)(strings)

    def string_merger(self, list_of_strings):
        return " and ".join(["(" + s + ")" for s in list_of_strings])

    def denested_return(self, l):
        if len(l) == 1: return l[0]
        if type(l[1][0]) == list and type(l[1][1]) == list: return [l[0]] + [l[1][0]] + [l[1][0]]
        return l

    def take_first_return(self, l):
        if len(l) == 1: return l
        else: return [l[0]] + l[1]

    def local_variable(self, bindex):
        return self.variable

    def global_variable(self, bindex):
        return self.get_global_description(bindex, "local_variable", "global_variable", "take_first_return")

    def represent_global(self, bindex):
        return self.get_global_description(bindex, "represent_local", "represent_global", "string_merger")

    def represent_local(self, bindex):
        assert bindex < self.get_local_nbins()
        bin_low = self.bin_edges[bindex]
        bin_high = self.bin_edges[bindex + 1]

        edgehigh = bindex == self.get_local_nbins() - 1
        edgelow = bindex == 0

        if self.repr_override is not None: varstr = self.repr_override
        else: varstr = self.variable
        candidate_return = "{} <= {} < {}".format(bin_low, varstr, bin_high)
        if not self.include_overflow: return candidate_return

        if edgehigh: return "{} <= {}".format(bin_low, varstr)
        if edgelow: return "{} < {}".format(varstr, bin_high)
        return candidate_return

    def edges_local(self, bindex):
        assert bindex < self.get_local_nbins()
        return self.bin_edges[bindex:bindex+2]

    def edges_global(self, bindex):
        return self.get_global_description(bindex, "edges_local", "edges_global", "denested_return")

    def recursively_include_overflow(self, include):
        self.include_overflow=include
        if self.subbins is not None:
            for b in self.subbins:
                b.recursively_include_overflow(include)

    def check_for_common_variable(self, variable):
        if self.subbins is not None:
            for sb in self.subbins:
                assert sb.variable != variable
                sb.check_for_common_variable(variable)

    def get_global_nbins(self):#, underoverflow = False):
        if self.subbins is not None:
           nbins = 0
           for b in self.subbins:
                nbins += b.get_global_nbins()
           return nbins
        else:
           return self.get_local_nbins()

    def get_local_nbins(self):
        return len(self.bin_edges) - 1

    def get_local_selection(self, bindex):
        assert bindex < self.get_local_nbins()
        bin_low = self.bin_edges[bindex]
        bin_high = self.bin_edges[bindex + 1]

        edgehigh = bindex == self.get_local_nbins() - 1
        edgelow = bindex == 0

        candidate_return = "( ({} <= {}) and ({} < {}) )".format(bin_low, self.variable, self.variable, bin_high)
        if not self.include_overflow: return "( ({} <= {}) and ({} < {}) )".format(bin_low, self.variable, self.variable, bin_high)

        if edgehigh: return "( {} <= {} )".format(bin_low, self.variable)
        if edgelow: return "({} < {})".format(self.variable, bin_high)
        return candidate_return

    def get_global_selection(self, bindex):
        return self.get_global_description(bindex, "get_local_selection", "get_global_selection", "string_merger")

    def get_local_bindex(self, frame):
        arr = frame.eval(self.variable).values
        indices = np.digitize(arr, self.bin_edges) - 1
        if self.include_overflow:
            indices[indices == -1] = 0
            indices[indices == self.get_local_nbins()] = self.get_local_nbins() - 1
        else:
            indices[indices == -1] = -1
            indices[indices == self.get_local_nbins()] = -2
        return indices

    # I don't know what the issue is...
    #this function needs some serious debugging
    def get_global_bindex(self, frame):
        indices = self.get_local_bindex(frame)
        underflown = indices == -1 #these bins must stay underflown 
        overflown = indices == -2 #these bins must stay overflown
        if self.subbins is not None:
            additions = []
            selections = []
            cum_total = 0
            for i in range(0, self.get_local_nbins()):
                additions.append(cum_total)
                selections.append((indices == i))
                cum_total += self.subbins[i].get_global_nbins()

            to_return = np.zeros(len(indices), np.int64)
            to_return[underflown] = -1 #yes they are underflown
            to_return[overflown] = -2 #yes they are overflown
            index = list(range(0, len(selections)))

            check_total = 0
            for s in selections:
                check_total += np.sum(1 * s)
            assert check_total + (np.sum(1*overflown) + np.sum(1*underflown)) == len(indices)

            #something is wrong here... what is it? how can I debug it?
            for a, in_bin, i in zip(additions, selections, index):
                frame_in_bin = frame.loc[in_bin]
                this_index = self.subbins[i].get_global_bindex(frame_in_bin)
                bin_underflown = (this_index == -1)
                bin_overflown = (this_index == -2)
                return_in_bin = to_return[in_bin]
                return_in_bin = this_index + a
                return_in_bin[bin_underflown] = -1
                return_in_bin[bin_overflown] = -2
                to_return[in_bin] = return_in_bin #you need to do this because only return_in_bin was modified in the lines return_in_bin[bin_overflown] = X
            return to_return
        return indices


