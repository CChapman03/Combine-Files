import bpy
import os
import sys

# Get index of first argument passes to blender after '--'
idx = sys.argv.index('--') + 1

# Get arguments passed to blender
in_dir = sys.argv[idx]
temp_file = sys.argv[idx + 1]

def clean():
    # Delete existing Collections
    context = bpy.context
    scene = context.scene

    for c in scene.collection.children:
        scene.collection.children.unlink(c)

    for c in bpy.data.collections:
        bpy.data.collections.remove(c)

    # Delete Existing Objects
    # for o in c.objects:
    #     bpy.data.objects.remove(o)

    # Re-Save Temporary Output File
    file_path = "%s/%s" % (in_dir.replace("'", ""), temp_file.replace("'", ""))
    bpy.ops.wm.save_as_mainfile(filepath=file_path)

clean()