import os
import bpy

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)

import combine_blend_files

import imp
imp.reload(combine_blend_files)

from combine_blend_files import *

o = 1
objs = []

for ob in bpy.context.scene.objects:
    objs.append(ob)
    print(("Object #%d is called: " % o)  + ob.data.name)

    o += 1

blend_data.update(objects = objs)