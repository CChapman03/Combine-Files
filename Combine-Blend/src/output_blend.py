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

file = combine_data.get("f")
filename = combine_data.get("filename")
filedir = combine_data.get("filedir")
should_save = combine_data.get("should_save")

objs = blend_data.get("objs")

total_polys = 0
total_objects = 0
objects_in_collection = 0
total_materials = 0
total_collections = 0

collection_name = ""

if not should_save:
    collection_name = file.split(".")[0]

    # Create Collection with the objects in the blend file
    bpy.ops.collection.create(collection_name)
    print("Creating Collection: '%s'" % collection_name)
    total_collections += 1

    for ob in objs:
        # add object to collection
        bpy.data.collections[collection_name].objects.link(ob)
        print("Adding Object %s of Type %s to Collection: '%s'" % (ob.data.name, str(ob.type), collection_name))
        
        total_objects += 1
        total_polys += len(ob.data.polygons)

        # get number of materials in object
        mesh = ob.data
        for faces in mesh.polygons:
            slot = ob.material_slots[faces.material_index]
            mat = slot.material
            if mat is not None:
                total_materials += 1

else:
    # save blender file
    bpy.ops.wm.save_mainfile(filename.join(".blend"))
    print("Saved Blend File: '%s' to '%s'" % (filename, filedir))
    print("------------------------------- \n")
    print("------------------------------- \n\n")

    # print statistics
    print("Blend File: '%s' Statistics: \n\n" % filename)
    print("------------------------------- \n")
    print("Number of Collections: %d \n" % total_collections)
    print("Number of Objects in Collection '%s': %d \n" % (collection_name, total_objects))
    print("Number of Polygons in Collection '%s': %d \n" % (collection_name, total_polys))
    print("Total Number of Objects: %d \n" % total_objects * total_collections)
    print("Total Number of Polygons: %d \n" % total_polys * total_collections)
    print("Total Number of Materials: %d \n" % (collection_name, total_materials))
    print("------------------------------- \n")
    filesize = os.path.getsize(os.path.join(filedir, filename))
    print("File Size: %d%s \n\n" % (int(filesize / 1000000.0), "MB") if filesize >= 1000000.0 else (int(filesize / 1000.0), "KB"))