import os
import bpy
import sys
import shlex
import re

def getArg(index):

    args_str = ' '.join(sys.argv[1:])
    args = shlex.split(args_str)
    i = args.index("--") + 1

    val = args[i + index]
    return val

# Get index of first argument passes to blender after '--'
idx = sys.argv.index('--') + 1

# Get arguments passed to blender
temp_filename = getArg(0)
input_filename = getArg(1)
input_directory = getArg(2)
in_filesize = int(getArg(3))

# Statistics Variables
file_collections = [0]
file_polys = [0]
file_objects = [0]
objects_in_file_collection = [0]
file_materials = [0]

def print_statistics():
    # print statistics
    print("Appended Blend File: '%s' to '%s'.\n" % (input_filename, temp_filename))
    print("Blend File: %s Contains: %d Collections, %d Objects, %d Polygons, and %d Materials.\n\n" % (input_filename, file_collections[0], file_objects[0], file_polys[0], file_materials[0]))
        
def combine_blend():

    # Append data from input file
    p = "%s/%s" % (input_directory, input_filename)
    with bpy.data.libraries.load(p) as (data_from, data_to):
        data_to.scenes = data_from.scenes
        data_to.collections = data_from.collections

    # New Collection Name
    new_collection_name = os.path.splitext(input_filename.replace("'", ""))[0]

    # Get input file's collections
    input_collections = data_to.scenes[0].collection

    collection = bpy.data.collections.new(new_collection_name)

    for child in input_collections.children:
        collection.children.link(child)

    bpy.context.scene.collection.children.link(collection)

    for col in collection.children:
        for ob in col.objects:
            file_objects[0] += 1

            # get object type
            objType = getattr(ob, 'type', '')

            if objType in ["MESH"]:
                # get number of polygons in object
                file_polys[0] += len(ob.data.polygons)

                # get number of materials in object
                mesh = ob.data
                mat = None

                if len(ob.material_slots) > 0:
                    slot = ob.material_slots[mesh.polygons[0].material_index]
                    mat = slot.material
                    if mat is not None:
                        file_materials[0] += 1

        file_collections[0] += 1

    # calculate filesize string
    in_filesize_str = [0]
    
    if in_filesize <= 1024:
        in_filesize_str[0] = "%d KB" % (in_filesize / 1024)
    elif in_filesize > 1024 and in_filesize <= 1024000:
        in_filesize_str[0] = "%d MB" % (in_filesize / 1024000)
    elif in_filesize > 1024000 and in_filesize <= 1024000000:
        in_filesize_str[0] = "%d GB" % (in_filesize / 1024000000)

    print_statistics()

    # Save output blend

    file_path = "%s/%s" % (input_directory, temp_filename)
    #data_blocks = set(collection)
    bpy.ops.wm.save_as_mainfile(filepath=file_path)
    #bpy.data.libraries.write(file_path, data_blocks)

    print("Appending Collection: '%s' with %d Object(s) in it." % (new_collection_name, file_objects[0]))

combine_blend()