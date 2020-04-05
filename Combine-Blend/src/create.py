import bpy
import os
import sys

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)

import data

import importlib
importlib.reload(data)

from data import *

f_data = file_data
in_dir = f_data.get("input_directory")
temp_file = f_data.get("temp_filename")
#print(in_dir)

def main():
    file_path = "%s/%s" % (in_dir, temp_file)
    bpy.ops.wm.save_as_mainfile(filepath=file_path)

main()