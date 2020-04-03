import bpy
import os
import sys

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)

import combine_blend_files

import imp
imp.reload(combine_blend_files)

from combine_blend_files import *

in_dir = create_data.get("input_dir")

def main():
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(in_dir, "output.blend"))

main()