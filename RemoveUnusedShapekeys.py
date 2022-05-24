# Most of this code is taken from https://blender.stackexchange.com/a/237611
# I just transformed it into a plugin

import bpy
import numpy as np

bl_info = {
    "name": "Remove Unused Shape Keys",
    "author": "https://github.com/PinkP4nther",
    "blender": (2,80,0),
    "location": "Object > Remove Unused Shape Keys",
    "description": "Removes all unused shape keys"
}

class RemoveEmptyShapeKeys(bpy.types.Operator):
    bl_idname = "wm.resk"
    bl_label = "Object"
    
    tolerance = 0.001
    
    def remove_unused_sk(self):
        print("Removing shape keys..")
        assert bpy.context.mode == 'OBJECT', "Must be in object mode!"

        for ob in bpy.context.selected_objects:
            if ob.type != 'MESH': continue
            if not ob.data.shape_keys: continue
            if not ob.data.shape_keys.use_relative: continue

            kbs = ob.data.shape_keys.key_blocks
            nverts = len(ob.data.vertices)
            to_delete = []

            # Cache locs for rel keys since many keys have the same rel key
            cache = {}

            locs = np.empty(3*nverts, dtype=np.float32)

            for kb in kbs:
                if kb == kb.relative_key: continue

                kb.data.foreach_get("co", locs)

                if kb.relative_key.name not in cache:
                    rel_locs = np.empty(3*nverts, dtype=np.float32)
                    kb.relative_key.data.foreach_get("co", rel_locs)
                    cache[kb.relative_key.name] = rel_locs
                rel_locs = cache[kb.relative_key.name]

                locs -= rel_locs
                if (np.abs(locs) < self.tolerance).all():
                    to_delete.append(kb.name)

            print("[*] Removing {} key blocks..".format(len(to_delete)))
            for kb_name in to_delete:
                ob.shape_key_remove(ob.data.shape_keys.key_blocks[kb_name])
        
    def execute(self, context):
        self.remove_unused_sk()
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(RemoveEmptyShapeKeys.bl_idname, text="Remove Unused Shape Keys")

def register():
    bpy.utils.register_class(RemoveEmptyShapeKeys)
    bpy.types.VIEW3D_MT_object.append(menu_func)

if __name__ == "__main__":
    register()