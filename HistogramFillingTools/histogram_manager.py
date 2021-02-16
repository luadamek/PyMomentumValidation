import ROOT
class HistogramManager:
    '''
    A class to handle the reading of histograms from files produced by the filling script
    '''
    channels = []
    histograms = []
    filename = None

    def __init__(self, file_name):
       print("Initializing histogram manager on file {}".format(file_name))
       self.filename = file_name
       t_file = ROOT.TFile(self.filename, "READ")
       self.channels = [key.GetName() for key in t_file.GetListOfKeys() if not "Binning" in  key.GetName()]
       print("Found these channels in the file {}".format(self.channels))
       dir = t_file.Get(self.channels[0])
       self.histograms = [key.GetName() for key in dir.GetListOfKeys() if not "Binning" in key.GetName()]
       for channel in self.channels:
           self.histograms = [key.replace(channel, "") for key in self.histograms]
       self.histograms = list(set(self.histograms))
       t_file.Close()

       self.channels_merged = {}

    def merge_channels(self, channel_name, channels_to_merge):
        self.channels_merged[channel_name] = channels_to_merge

    def list_histograms(self, wcard):
       print("=" * 50)
       print("listing all histograms:")
       for histogram in sorted(self.histograms, key=str.lower):
           if wcard in histogram: print(histogram)

    def has_histogram(self, histogram_name):
        return histogram_name in self.histograms

    def get_histograms(self, histogram_name, rebin=None):
       t_file = ROOT.TFile(self.filename, "READ")
       histogram_dict = {}
       if not histogram_name in self.histograms:
           raise ValueError("Couldn't find histogram " + histogram_name  + " in the file")

       for channel in self.channels:
           #t_file.cd(channel)
           histogram_dict[channel] = t_file.Get(channel + "/" + histogram_name + channel)
           histogram_dict[channel].SetDirectory(0)
           if rebin is not None:
               histogram_dict[channel].Rebin(rebin)

       for channel in self.channels_merged:
           histogram_dict[channel] = None
           for channel_to_merge in self.channels_merged[channel]:
               if histogram_dict[channel] is None: histogram_dict[channel] = histogram_dict[channel_to_merge].Clone(histogram_dict[channel_to_merge].GetName().replace(channel_to_merge, channel))
               else: histogram_dict[channel].Add(histogram_dict[channel_to_merge])
               histogram_dict[channel].SetDirectory(0)

       t_file.Close()
       return histogram_dict
