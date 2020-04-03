import os
import subprocess
import platform
import time

# data structs
create_data = {"input_directory" : ""}
data = {"output_filename" : "", "input_filename" : "", "input_directory" : ""}
stats = {"output_filename" : "", "time_taken" : 0, "num_files" : 0, "file_size" : 0}

# variables
input_dir = os.path.abspath("../blends/")

a = 0
for f in os.listdir(input_dir):
    fn, fe = os.path.splitext(f)

    if fe == ".blend":
        a += 1

num_files = a

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
    p = subprocess.Popen(cmd.split(" "))
    return p

def kill(process):
    #if process is not None:
    process.kill()

def init(file):
    start_time = time.time()
    fn, fe = os.path.splitext(file)
    first_file = fn
    print(first_file)

    # update data
    create_data.update(input_directory = input_dir)
    data.update(input_directory = input_dir)

    # Create temp output.blend file
    cmd = "blender -b -P create.py" if get_platform() == 'Linux' else "blender.exe -b -P create.py"
    blend_file_create = start(cmd)
    blend_file_create.wait()
    kill(blend_file_create)

def run(file):
    # update data
    data.update(input_filename = file)
    data.update(output_filename = "output.blend")

    cmd = "blender -b %s%s -P combine.py" % (input_dir, file) if get_platform() == 'Linux' else "blender.exe -b %s%s -P combine.py" % (input_dir, file)
    blender_file_in = start(cmd)
    blender_file_in.wait()
    kill(blender_file_in)

def terminate(file):
    last_file = file.split(" ")[0]
    out_f_name = "%s%s" % (first_file, last_file)
    time_taken = time.time() - start_time
    filesize = os.path.getsize(os.path.join(input_dir, "output.blend"))

    # update stats
    stats.update(output_filename = out_f_name)
    stats.update(time_taken = time_taken)
    stats.update(num_files = num_files)
    stats.update(file_size = filesize)

    cmd = "blender -b %s/output.blend -P statistics.py" % input_dir if get_platform() == 'Linux' else "blender.exe -b %s/output.blend -P statistics.p" % input_dir
    blender_file_stats = start(cmd)
    blender_file_stats.wait()
    kill(blender_file_stats)

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

    if i < num_files:
        run(file)
    
    else:
        terminate(file)

def main():

    i = 0
    for file in os.listdir(input_dir):
        fn, fe = os.path.splitext(file)

        if fe == ".blend":
            #combine_to(i, file, 100)
            combine(i, file)

            i += 1

main()