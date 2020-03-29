import os
import subprocess
        
combine_data = {"f" : "", "filename" : "", "filedir" : "", "should_save" : False}
blend_data = {"objects" : []}

f_dir = "../blends/"

a = 0
for f in os.listdir(f_dir):
    fn, fe = os.path.splitext(f)
    if os.path.isfile(f) and fe == '.blend':
        a += 1

num_files = a
first_file = ""
last_file = ""

out_f_name = ""

blender_file_out = None

def init(file):
    filepath = os.path.dirname(os.path.abspath(file))
    combine_data.update(filedir = filepath)
    combine_data.update(should_save = False)
    blender_file_out = start("blender -b -P output_blend.py")
    first_file = file.split(".")[0]

def do_work(file):
    blender_file_in = start("blender -b %s -P blend_file.py" % file)
    combine_data.update(f = file)
    kill(blender_file_in)

def save(file):
    last_file = file.split(".")[0]
    out_f_name = first_file.join("-").join(last_file)
    combine_data.update(filename = out_f_name)
    combine_data.update(should_save = True)

def start(cmd):
    p = subprocess.Popen(cmd.split(" "))
    return p

def kill(process):
    if process is not None:
        process.kill()

def combine(i, file):
    if i == 1:
        init(file)

    if i < num_files:
        do_work(file)

    elif i >= num_files:
        save(file)
        kill(blender_file_out)


def combine_to(i, file, amount):
    if i == 1:
        init(file)

    elif i < amount:
        do_work(file)

    else:
        save(file)
        kill(blender_file_out)

i = 1
for file in os.listdir(f_dir):

    fn, fe = os.path.splitext(file)
    if fe == '.blend':
        #combine_to(i, file, 100)
        combine(i, file)

        i += 1