import os
import bpy
import sys

# Get index of first argument passes to blender after '--'
idx = sys.argv.index('--') + 1

# Get arguments passed to blender
input_directory = sys.argv[idx]
output_filename = sys.argv[idx + 1]
time_taken = float(sys.argv[idx + 2])
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

    # Set Time Taken To Process Output
    if time_taken <= 60:
        time_taken_str[0] = "%f Seconds" % float(time_taken)
    elif time_taken > 60 and time_taken <= 60 * 60:
        time_taken_str[0] = "%f Minutes" % (float(time_taken) / (60.0))
    elif time_taken > 60 * 60 and time_taken <= 60 * 60 * 24:
        time_taken_str[0] = "%f Hours" % (float(time_taken) / (60.0 * 60.0))

    # Set Output Filesize String
    if filesize <= 1024:
        filesize_str[0] = "%f B" % (float(filesize))
    elif filesize > 1024 and filesize <= 1024000:
        filesize_str[0] = "%f KB" % (float(filesize) / 1024.0)
    elif filesize > 1024000 and filesize <= 1024000000:
        filesize_str[0] = "%f MB" % (float(filesize) / 1024000.0)
    elif filesize > 1024000000 and filesize <= 1024000000000:
        filesize_str[0] = "%f GB" % (float(filesize) / 1024000000.0)

    # Print Statistics
    print("\nFinished Combining Blend Files! Time Taken: %s \n\n" % time_taken_str[0])

    print("----------------------------------------\n")
    print("Blend File: '%s' Statistics: \n\n" % output_filename)
    print("----------------------------------------\n")

    print("\nCollection-Tree: \n----------------------------------------\n")

    # get statistic for output file
    for col in output_collections.children:
        total_collections[0] += 1

        print("\tCollection: %s" % col.name)

        if col.children is not None:
            for subcol in col.children:
                print("\t\tCollection: %s" % subcol.name)

                for ob in subcol.objects:
                    total_objects[0] += 1

                    # get object type
                    objType = getattr(ob, 'type', '')
                    mat_names = [0]
                    polys = [0]
                    
                    if objType in ["MESH"]:

                        # get number of polygons in object
                        total_polys[0] += len(ob.data.polygons)
                        polys[0] = len(ob.data.polygons)

                        mat_names[0] = "["
                        # get number of materials in object
                        mesh = ob.data

                        mat = None
                        if len(ob.material_slots) > 0:
                            slot = ob.material_slots[mesh.polygons[0].material_index]
                            mat = slot.material
                            if mat is not None:
                                mat_names[0] += mat.name + ", "
                                total_materials[0] += 1
                            else:
                                mat_names[0] = "None"

                        mat_names[0] += "]"

                    else:
                        polys[0] = "None"
                        mat_names[0] = "None"
                        
                    ob_str = "\t\t\tObject: %s, Type: %s, Polys : %d, Materials: %s\n" % (ob.data.name, objType, polys[0], mat_names[0])
                    print(ob_str)

                total_collections[0] += 1

    print("----------------------------------------\n")

    # print final statistics
    print("Number of Blend Files Combined: %d\n" % num_files)
    print("Total Number of Collections: %d \n" % total_collections[0])
    print("Total Number of Objects: %d \n" % total_objects[0])
    print("Total Number of Polygons: %d \n" % total_polys[0])
    print("Total Number of Materials: %d \n" % (total_materials[0]))
    print("----------------------------------------\n")
    print("File Size: %s \n\n" % filesize_str[0])

    # write collections to output file
    file_path = "%s/%s" % (input_directory, output_filename)
    bpy.ops.wm.save_as_mainfile(filepath=file_path)

print_stats()