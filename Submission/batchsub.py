import subprocess
import os

def finished_token_in(filename):
    if not os.path.exists(filename): return False
    with open(filename, "r") as f:
        lines = f.readlines()
        for l in lines[max(-10, -1 * len(lines)):]:
            if "__Finished__" in l or "__FINISHED__" in l  or "__FINSIHED__" in l:
                print("FINISHED {}".format(filename))
                print("\n"*5)
                return True
        print("Output file {} didn't show a sign of finishing".format(filename))
        for l in lines[max(-10, -1 * len(lines)):]:
            print(l.rstrip("\n"))
    return False

#sometimes the slurm batch system fails when queried often, so provide a protection by trying to query it multiple times
def do_multiple_subprocess_attempts(command):
    for i in range(0, 10): 
        try:
           result = subprocess.check_output(command)
        except Exception as e:
           if i != 9: continue
           else: raise(e)
        break
    return result

def get_parsed_slurm_queue():
    long_info = do_multiple_subprocess_attempts(["squeue", "-u", os.getenv("USER")])
    lines = long_info.decode("utf-8").split("\n")
    lines = [l for l in lines if l] #remove empty lines
    new_lines = []
    for l in lines:
        new_lines.append([el for el in l.split(" ") if "" != el]) #split the table by spaces, and then remove those entries that are just blank
    lines=new_lines

    #only parse the table up to the amount of memory used in the job
    mem_index = -1
    for i, el in enumerate(lines[0]):
        if  el == "MIN_MEM": mem_index = i
    assert mem_index != -1

    #only keep the information in the table up to the memory usage
    for i, l in enumerate(lines):
        cleaned_line = l[0: mem_index]
        lines[i] = cleaned_line

    #check that the lines are all of the same length:
    for l in lines:
        for l2 in lines:
            if len(l) != len(l2):
                print(l)
                print(l2)
                raise ValueError("Couldn't parse the slurm output because two lines had a different number of entries")

    entry_dict = { el:i for (i, el) in enumerate(lines[0])}
    job_list = []
    for l in lines[1:]:
        if len(l) > 1:
            job_dict = { key:l[entry_dict[key]] for key in entry_dict }
            job_list.append(job_dict)
    return job_list

class Job:
    def __init__(self, jobname, jobdir, commands, time = "01:00:00", memory="8000M", in_container=True):
        self.jobname = jobname
        self.jobdir = jobdir
        self.commands = commands
        self.time = time
        self.memory = memory
        self.in_container = in_container

        if not os.path.exists(self.jobdir): os.makedirs(jobdir)
        self.errorfile_name = os.path.join(jobdir, jobname  + ".err")
        self.outputfile_name = os.path.join(jobdir, jobname  + ".out")
        self.run_script_name = os.path.join(jobdir, jobname  + ".sh")
        self.batch_script_name = os.path.join(jobdir, jobname  + "_slurm.sh")
        self.jobid = None

    def __repr__(self):
        to_return = "Job Name: {jobname}\nCommands:\n".format(jobname=self.jobname)
        for c in self.commands:
            to_return += (c + "\n")
        return to_return

    def check_jobdir_existence(self):
        if not os.path.exists(self.jobdir): os.makedirs(jobdir)

    def create_submission_files(self):
        print("Creating submission files")
        self.check_jobdir_existence()
        with open(self.run_script_name, "w") as f:
            for c in self.commands:
                f.write(c + "\n")
        if self.in_container: os.system("batchScript \"source {}\" -O {}".format(self.run_script_name, self.batch_script_name))
        else:
            with open(self.batch_script_name, "w") as f:
                f.write("source {}\n".format(self.run_script_name))
        print("Submission files created")

    def submit(self, updates={}):
        self.check_jobdir_existence()
        if self.check_if_running(): return False
        for key in updates:
            setattr(self, key, updates[key])
        self.create_submission_files()
        commands = ["sbatch", "--mem={}".format(self.memory), "--time={}".format(self.time), "--error={}".format(self.errorfile_name), "--output={}".format(self.outputfile_name), self.batch_script_name]
        output = do_multiple_subprocess_attempts(commands)
        output = output.decode("utf-8")
        output = output.replace("\n", "")
        self.jobid = output.split(" ")[-1]
        return True

    def cancel(self):
        if self.check_if_running():
            assert self.jobid
            cancelled = do_multiple_subprocess_attemps(["scancel", self.jobid])
        else:
            print("Job is already finished")

    def run_local(self):
        if self.check_if_running():
            print("Will not run locally. The job is still running")
            return
        if self.check_completion(): return
        self.create_submission_files()
        os.system("source {}".format(self.run_script_name, self.outputfile_name))
        return True

    def check_if_running(self, parsed_queue = None):
        if not self.jobid: return False
        if not parsed_queue: parsed_queue = get_parsed_slurm_queue()
        for job in parsed_queue:
            if self.jobid == job["JOBID"]:
                return True
        return False

    def check_for_error(self, parsed_queue = None):
        if not self.check_if_running(parsed_queue = parsed_queue) and not self.check_completion():
            print("This job did not finish running")
            print(self)
            return True
        return False

    def check_completion(self):
        self.check_jobdir_existence()
        return finished_token_in(self.outputfile_name)

class JobSet:
    def __init__(self, name, jobs = []):
        self.jobs = jobs
        self.name = name

    def add_job(self, job):
        self.jobs.append(job)

    def submit(self):
        for job in self.jobs:
            job.submit()

    def check_completion(self):
       for job in self.jobs:
           if not job.check_completion(): return False

    def check_for_errors(self):
        has_error = False
        for job in self.jobs:
            if not job.check_for_error():
               has_error = True
               print("This job didn't finished:")
               print(job)
        return has_error

    def save(self):
        with open("{}_JOBSET.pkl".format(self.name), "wb") as f:
            import pickle as pkl
            pkl.dump(self, f)
        return True

