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
output_filename = stats.get("output_filename")
time_taken = stats.get("time_taken")
num_files = stats.get("num_files")
filesize = stats.get("file_size")

# Statistics Variables
total_collections = 0
total_polys = 0
total_objects = 0
total_materials = 0
time_taken_str = ""
filesize_str = ""

def main():

    # get collections
    output_collections = bpy.context.scene.collection

    # get statistic for output file
    for col in output_collections:
        for ob in output_collections.objects:
            total_objects += 1
            total_polys += len(ob.data.polygons)

            # get number of materials in object
            mesh = ob.data
            for faces in mesh.polygons:
                slot = ob.material_slots[faces.material_index]
                mat = slot.material
                if mat is not None:
                    total_materials += 1

        total_collections += 1
    
    if filesize <= 1024:
        filesize_str = "%d KB" % (filesize / 1024)
    elif filesize > 1024 and filesize <= 1024000:
        filesize_str = "%d MB" % (filesize / 1024000)
    elif filesize > 1024000 and filesize <= 1024000000:
        filesize_str = "%d GB" % (filesize / 1024000000)

    if time_taken <= 60:
        time_taken_str = "%d Seconds" % (time_taken)
    elif time_taken > 60 time_taken <= 60 * 60:
        time_taken_str = "%d Minutes" % (time_taken / (60))
    elif time_taken > 60 * 60 time_taken <= 60 * 60 * 24:
        time_taken_str = "%d Hours" % (time_taken / (60 * 60))

    # print final statistics
    print("Finished Combining Blend Files! Time Taken: %s \n\n" % time_taken_str)
    print("Blend File: '%s' Statistics: \n\n" % output_filename)
    print("------------------------------- \n")
    print("Number of Blend Files Combined: %d" % num_files)
    print("Total Number of Collections: %d \n" % total_collections)
    print("Total Number of Objects: %d \n" % total_objects)
    print("Total Number of Polygons: %d \n" % total_polys)
    print("Total Number of Materials: %d \n" % (total_materials))
    print("------------------------------- \n")
    print("File Size: %s \n\n" % filesize_str)

    # write collections to output file
    bpy.data.libraries.write(output_filename, output_collections)

main()