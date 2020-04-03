import os
import bpy
import sys

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)

import combine_blend_files

import imp
imp.reload(combine_blend_files)

from combine_blend_files import *

# data variables
output_filename = data.get("output_filename")
input_filename = data.get("input_filename")
input_directory = data.get("input_directory")

# Statistics Variables
file_collections = 0
file_polys = 0
file_objects = 0
objects_in_file_collection = 0
file_materials = 0
in_filesize = 0

def print_statistics():
    # print statistics
    print("Appended Blend File: '%s' to '%s'.\n" % (input_filename, output_filename))
    print("Blend File: %s Contains: %d Collections, %d Objects, %d Polygons, and %d Materials.\n\n" % (input_filename, file_collections, file_objects, file_polys, file_materials)
        
def main():

    # Load output file and get collections
    with bpy.data.libraries.load("%s%s" % (input_directory, output_filename)) as (data_from, data_to):
        data_to.collections = data_from.collections

    # set output collections from load
    output_collections = data_to.collections

    # rename input file's collection
    collection_name = input_filename.split(".")[0]
    bpy.context.scene.collection.name = collection_name

    # get input collection
    input_collections = bpy.context.scene.collection

    # Append input collection to output file
    output_collections.children.link(input_collections)

    print("Appending Collection: '%s' with %d Object(s) in it." % (collection_name, len(input_collections.objects)))
    #total_collections += 1

    # write collections to output file
    bpy.data.libraries.write(out_file, output_collections)

    # get statistics for input file
    for col in input_collections:
        for ob in input_collections.objects:
            file_objects += 1
            file_polys += len(ob.data.polygons)

            # get number of materials in object
            mesh = ob.data
            for faces in mesh.polygons:
                slot = ob.material_slots[faces.material_index]
                mat = slot.material
                if mat is not None:
                    file_materials += 1

        file_collections = += 1

    in_filesize = os.path.getsize(os.path.join(input_directory, input_filename))
    in_filesize_str = ""
        
    if in_filesize <= 1024:
        in_filesize_str = "%d KB" % (in_filesize / 1024)
    elif in_filesize > 1024 and in_filesize <= 1024000:
        in_filesize_str = "%d MB" % (in_filesize / 1024000)
    elif in_filesize > 1024000 and in_filesize <= 1024000000:
        in_filesize_str = "%d GB" % (in_filesize / 1024000000)

    print_statistics()

main()