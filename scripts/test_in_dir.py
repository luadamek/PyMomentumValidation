import pickle as pkl
jobset = pkl.load(open("/project/def-psavard/ladamek/momentumvalidationoutput/Nov10_calib/jobset.pkl", "rb"))
jobset.jobs[0].run_local()
