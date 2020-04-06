import bpy
import os
import sys

# Get index of first argument passes to blender after '--'
idx = sys.argv.index('--') + 1

# Get arguments passed to blender
in_dir = sys.argv[idx]
temp_file = sys.argv[idx + 1]

def create():
    # Create and save out temporary blend file for output
    file_path = "%s/%s" % (in_dir, temp_file)
    bpy.ops.wm.save_as_mainfile(filepath=file_path)

create()