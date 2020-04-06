import os
import bpy
import sys

# Get index of first argument passes to blender after '--'
idx = sys.argv.index('--') + 1

# Get arguments passed to blender
input_directory = sys.argv[idx]
output_filename = sys.argv[idx + 1]
time_taken = int(sys.argv[idx + 2])
num_files = int(sys.argv[idx + 3])
filesize = int(sys.argv[idx + 4])

# Statistics Variables
total_collections = [0]
total_polys = [0]
total_objects = [0]
total_materials = [0]
time_taken_str = [0]
filesize_str = [0]

def print_stats():

    # get collections
    output_collections = bpy.context.scene.collection

    # get statistic for output file
    for col in output_collections.children:
        for ob in col.objects:
            total_objects[0] += 1

            # get object type
            objType = getattr(ob, 'type', '')
	    
            if objType in ["MESH"]:
                # get number of polygons in object
                total_polys[0] += len(ob.data.polygons)

                # get number of materials in object
                mesh = ob.data
                for faces in mesh.polygons:
                    if len(ob.material_slots) > 0:
                        slot = ob.material_slots[faces.material_index]
                        mat = slot.material
                        if mat is not None:
                            total_materials[0] += 1

        total_collections[0] += 1
    
    # Set Output Filesize String
    if filesize <= 1024:
        filesize_str[0] = "%d KB" % (filesize / 1024)
    elif filesize > 1024 and filesize <= 1024000:
        filesize_str[0] = "%d MB" % (filesize / 1024000)
    elif filesize > 1024000 and filesize <= 1024000000:
        filesize_str[0] = "%d GB" % (filesize / 1024000000)

    # Set Time Taken To Process Output
    if time_taken <= 60:
        time_taken_str[0] = "%d Seconds" % (time_taken)
    elif time_taken > 60 and time_taken <= 60 * 60:
        time_taken_str[0] = "%d Minutes" % (time_taken / (60))
    elif time_taken > 60 * 60 and time_taken <= 60 * 60 * 24:
        time_taken_str[0] = "%d Hours" % (time_taken / (60 * 60))

    # print final statistics
    print("Finished Combining Blend Files! Time Taken: %s \n\n" % time_taken_str[0])
    print("Blend File: '%s' Statistics: \n\n" % output_filename)
    print("------------------------------- \n")
    print("Number of Blend Files Combined: %d\n" % num_files)
    print("Total Number of Collections: %d \n" % total_collections[0])
    print("Total Number of Objects: %d \n" % total_objects[0])
    print("Total Number of Polygons: %d \n" % total_polys[0])
    print("Total Number of Materials: %d \n" % (total_materials[0]))
    print("------------------------------- \n")
    print("File Size: %s \n\n" % filesize_str[0])

    # write collections to output file
    file_path = "%s/%s" % (input_directory, output_filename)
    bpy.ops.wm.save_as_mainfile(filepath=file_path)

print_stats()