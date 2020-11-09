import pickle as pkl
jobset = pkl.load(open("/project/def-psavard/ladamek/momentumvalidationoutput/Nov9_calib/jobset.pkl", "rb"))
jobset.jobs[0].run_local()
