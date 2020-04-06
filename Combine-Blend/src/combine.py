import os
import bpy
import sys

# Get index of first argument passes to blender after '--'
idx = sys.argv.index('--') + 1

# Get arguments passed to blender
temp_filename = sys.argv[idx]
input_filename = sys.argv[idx + 1]
input_directory = sys.argv[idx + 2]
in_filesize = int(sys.argv[idx + 3])

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

    # create collection with input file's collections in it.
    
    # New Collection Name
    new_collection_name = os.path.splitext(input_filename)[0]

    # Get input file's collections
    input_collections = bpy.context.scene.collection

    # Try to rename input collection
    input_collections.name = new_collection_name # NOT working!

    # -------------------------------------------------------------------------

    # TODO: 
    # 1. Figure out how to use bpy to rename collections.
    # 2. Then figure out how to combine multiple blend files together (Current Only Saves Out The Contents of the Last Blend File Processed)

    # -------------------------------------------------------------------------

    # loop through collections in input collection
    for col in input_collections.children:
        for ob in col.objects:
            file_objects[0] += 1

            # add object to collection
            if not ob.data.name in col:
                col.objects.link(ob)         

            # get object type
            objType = getattr(ob, 'type', '')
	    
            if objType in ["MESH"]:
                # get number of polygons in object
                file_polys[0] += len(ob.data.polygons)

                # get number of materials in object
                mesh = ob.data
                for faces in mesh.polygons:
                    if len(ob.material_slots) > 0:
                        slot = ob.material_slots[faces.material_index]
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
    bpy.ops.wm.save_as_mainfile(filepath=file_path)

    print("Appending Collection: '%s' with %d Object(s) in it." % (new_collection_name, len(input_collections.objects)))

combine_blend()