import os
import subprocess
import platform
import time
import signal

#from data import *

# variables
input_dir = os.path.abspath("../blends/")
temp_filename = "output.blend"

num_files = [0]
for f in os.listdir(input_dir):
    fe = os.path.splitext(f)[1]

    if fe == ".blend":
        num_files[0] += 1

first_file = [0]
last_file = [0]
out_f_name = [0]

blend_file_create = None
blender_file_in = None
blender_file_stats = None

start_time = [0]
time_taken = [0]

def get_platform():
    return platform.system()

def execute_blender(cmd, time_limit = 60*5, stop = False):
    fn = cmd.split("-P ")[1].split(".")[0]

    # Craete Log Files Per Subprocess
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

    # Initailize/Create Temporary Output Blend and Delete Everything in it

    start_time[0] = time.time()
    fn = os.path.splitext(file)[0]
    first_file[0] = fn

    # Create temp output.blend file
    linux_mac_cmd = "blender -b -P create.py -- %s %s" % (input_dir, temp_filename)
    win_cmd = "blender.exe -b -P create.py -- %s %s" % (input_dir, temp_filename)

    cmd = linux_mac_cmd if get_platform() == 'Linux' else win_cmd
    stop_condition = os.path.isfile(os.path.join(input_dir, "output.blend")) and os.path.getsize(os.path.join(input_dir, "output.blend")) == 0
    execute_blender(cmd, 20, stop_condition)

    # Clean temp output.blend file
    linux_mac_cmd = "blender -b %s/%s -P clean.py -- %s %s" % (input_dir, temp_filename, input_dir, temp_filename)
    win_cmd = "blender.exe -b %s/%s -P clean.py -- %s %s" % (input_dir, temp_filename, input_dir, temp_filename)

    cmd = linux_mac_cmd if get_platform() == 'Linux' else win_cmd
    stop_condition = os.path.isfile(os.path.join(input_dir, "output.blend")) and os.path.getsize(os.path.join(input_dir, "output.blend")) == 0
    execute_blender(cmd, 20, stop_condition)

    # Remove duplicate output.blend (Created By Cleaning Temporary Output Blend)
    os.remove(os.path.join(input_dir, "output.blend1"))

def run(file):

    # Run Per Input Blend File

    in_filesize = os.path.getsize(os.path.join(input_dir, file))

    linux_mac_cmd = "blender -b %s/%s -P combine.py -- %s %s %s %d" % (input_dir, file, temp_filename, file, input_dir, in_filesize)
    win_cmd = "blender.exe -b %s/%s -P combine.py -- %s %s %s %d" % (input_dir, file, temp_filename, file, input_dir, in_filesize)
    #portable_cmd = "blender -b %s/%s -P combine.py -- $s %s %s %d" % (input_dir, file, input_dir, file, temp_filename, in_filesize)

    cmd = linux_mac_cmd if get_platform() == 'Linux' or get_platform() == 'Darwin' else win_cmd
    #stop_condition = False
    execute_blender(cmd)

    # Remove duplicate output.blend
    os.remove(os.path.join(input_dir, "output.blend1"))

def terminate(file):

    # Save, Print Statistics, and Rename Output Blend

    fn = os.path.splitext(file)[0]
    last_file[0] = fn
    out_f_name[0] = "%s-%s" % (first_file[0], last_file[0])
    time_taken[0] = time.time() - start_time[0]
    filesize = os.path.getsize("%s/%s" % (input_dir, temp_filename))

    linux_mac_cmd = "blender -b %s/output.blend -P statistics.py -- %s %s %d %d %d" % (input_dir, input_dir, out_f_name[0], time_taken[0], num_files[0], filesize)
    win_cmd = "blender.exe -b %s/output.blend -P statistics.py -- %s %s %d %d %d" % (input_dir, input_dir, out_f_name[0], time_taken[0], num_files[0], filesize)

    cmd = linux_mac_cmd if get_platform() == 'Linux' else win_cmd
    execute_blender(cmd)

    # Remove Temporary Output Blend (To Be Replaced by: '<First_Blend_File>-<Last_Blend_File>.blend')
    os.remove(os.path.join(input_dir, "output.blend"))


def combine_to(i, file, amount):
    
    # Combine Blend Files Up To Set Amount (In Case There are Too Many Blends in Input Directory)
    
    if i == 0:
        init(file)

    if i < amount:
        run(file)
    
    if i == amount - 1:
        terminate(file)
        i = -1


def combine(i, file):

    # Combine ALL Blend Files in Input Directory

    if i == 0:
        init(file)

    if i < num_files[0]:
        run(file)
    
    if i == num_files[0] - 1:
        terminate(file)

def main():

    i = [0]
    for file in os.listdir(input_dir):
        fe = os.path.splitext(file)[1]

        if fe == ".blend":
            #combine_to(i, file, 100)
            combine(i[0], file)

            i[0] += 1

main()