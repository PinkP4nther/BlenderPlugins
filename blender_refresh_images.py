import bpy

bl_info = {
    "name": "Refresh Images",
    "author": "https://github.com/PinkP4nther",
    "blender": (2,80,0),
    "location": "File > Refresh All Images",
    "description": "Reloads all images into blender."
}

class ImageReload(bpy.types.Operator):

    bl_idname = "wm.image_reload"
    bl_label = "Reloads images/textures"

    def refresh_imgs(self):
        for img in bpy.data.images:
            img.reload()
            print("[*] Image Name: "+img.name)

    def execute(self, context):
        print("[+] Refreshing images..")
        self.refresh_imgs()
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(ImageReload.bl_idname, text="Refresh All Images")

def register():
	bpy.utils.register_class(ImageReload)
	bpy.types.TOPBAR_MT_render.append(menu_func)

if __name__ == "__main__":
	register()
	#bpy.ops.wm.image_reload()