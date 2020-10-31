import os
from constraint_batchsub import get_parsed_slurm_queue

def monitor(filename, resub=True, force_resub = False):

    assert "{}" in filename
    assert "{}_JOBSET" in filename
    for i in range(1, 100):
        print("Checking for {}".format(i))
        this_fname = filename.format(i)
        this_fname = os.path.join(os.getenv("PWD"), this_fname)
        print(this_fname)
        if os.path.exists(this_fname): break

    if not os.path.exists(this_fname): return

    parsed_queue = get_parsed_slurm_queue()
    import pickle as pkl
    with open(this_fname, "rb") as f:
        jobs = pkl.load(f)

    finisheds = []
    errors = []
    runnings = []

    for j in jobs.jobs:
        if force_resub:
            j.submit()
            continue
        error = j.check_for_error(parsed_queue = parsed_queue)
        running = j.check_if_running(parsed_queue = parsed_queue)
        if running:
           runnings.append(j.jobname)
           print("RUNNING: ", j.jobname)
        elif error:
            errors.append(j.jobname)
            print("ERROR: ", j.jobname)
            if resub: j.submit()
        else:
            finisheds.append(j.jobname)
            print("FINISHED: ", j.jobname)
    if force_resub:
        print("All jobs resubmitted, returning")
        return

    print("Finished: {}".format(finisheds))
    print("Errors: {}".format(errors))
    print("running: {}".format(runnings))

    print("Finished: {}".format(len(finisheds)))
    print("Errors: {}".format(len(errors)))
    print("running: {}".format(len(runnings)))

    with open(filename.format(i+1), "wb") as f:
        pkl.dump(jobs, f)
    os.system("rm {}".format(this_fname))
