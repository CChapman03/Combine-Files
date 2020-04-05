import os
import subprocess
import platform
import time
import signal

from data import *

# variables
input_dir = os.path.abspath("../blends/")

f_data = file_data
s_data = stat_data

num_files = 0
for f in os.listdir(input_dir):
    fn, fe = os.path.splitext(f)

    if fe == ".blend":
        num_files += 1

first_file = ""
last_file = ""
out_f_name = ""

blend_file_create = None
blender_file_in = None
blender_file_stats = None

start_time = 0
time_taken = 0

def get_platform():
    return platform.system()

def start(cmd):

    fn = cmd.split("-P ")[1].split(".")[0]

    out = open("../logs/%s_out.txt" % fn, "w")
    err = open("../logs/%s_err.txt" % fn, "w")

    p = subprocess.Popen(cmd.split(" "), stdout=out, stderr=err, text=True)
    return p

def execute_blender(cmd, time_limit = 60*5, stop = False):
    fn = cmd.split("-P ")[1].split(".")[0]

    out = open("../logs/%s_out.txt" % fn, "w")
    err = open("../logs/%s_err.txt" % fn, "w")

    p = subprocess.Popen(cmd.split(" "), stdout=out, stderr=err, text=True)
    start_time = time.time()

    is_running = True
    while p.returncode == None:
        p.poll()

        if time.time() - start_time > time_limit:
            if stop:
                p.kill()
                raise Exception("Process with command '%s' has failed to do its job" % cmd)
            
            p.kill()
            raise Exception("Process with command '%s' has failed to do its job" % cmd)
        
    p.wait()


def init(file):
    start_time = time.time()
    fn, fe = os.path.splitext(file)
    first_file = fn

    # update data
    f_data.update(input_directory = input_dir)

    # Create temp output.blend file
    cmd = "blender -b -P create.py" if get_platform() == 'Linux' else "blender.exe -b -P create.py"
    stop_condition = os.path.isfile(os.path.join(input_dir, "output.blend")) and os.path.getsize(os.path.join(input_dir, "output.blend")) == 0
    execute_blender(cmd, 20, stop_condition)

def run(file):
    # update data
    f_data.update(input_filename = file)

    in_filesize = os.path.getsize(os.path.join(input_dir, file))
    f_data.update(input_file_size = in_filesize)

    cmd = "blender -b %s%s -P combine.py" % (input_dir, file) if get_platform() == 'Linux' else "blender.exe -b %s%s -P combine.py" % (input_dir, file)
    #stop_condition = False
    execute_blender(cmd)

def terminate(file):
    last_file = file.split(" ")[0]
    out_f_name = "%s%s" % (first_file, last_file)
    time_taken = time.time() - start_time
    filesize = os.path.getsize(os.path.join(input_dir, "output.blend"))

    # update stats
    f_data.update(output_filename = out_f_name)
    f_data.update(output_file_size = filesize)

    s_data.update(time_taken = time_taken)
    s_data.update(num_files_processed = num_files)

    cmd = "blender -b %s/output.blend -P statistics.py" % input_dir if get_platform() == 'Linux' else "blender.exe -b %s/output.blend -P statistics.py" % input_dir
    execute_blender(cmd)

    os.remove(os.path.join(input_dir, "output.blend"))


def combine_to(i, file, amount):
    if i == 0:
        init(file)

    if i < amount:
        run(file)
    
    else:
        terminate(file)
        i = -1


def combine(i, file):
    if i == 0:
        init(file)

    # if i < num_files:
    #     run(file)
    
    # else:
    #     terminate(file)

def main():

    i = 0
    for file in os.listdir(input_dir):
        fn, fe = os.path.splitext(file)

        if fe == ".blend":
            #combine_to(i, file, 100)
            combine(i, file)
            #print(f_data.get("input_directory"))

            i += 1

main()