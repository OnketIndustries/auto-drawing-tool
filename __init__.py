
if "bpy" in locals():
    import imp
    imp.reload(operate)

else:
    from . import operate

import bpy


bl_info = {
    "name": "Auto Drawing Tool",
    "author": "Nobuyuki Hirakata",
    "version": (0, 1, 0),
    "blender": (2, 76, 0),
    "location": "View3D > Toolshelf > Animation tab",
    "description": "Make auto-drawing setting using Build modifier and Freestyle.",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Animation"
}

def register():
    bpy.utils.register_module(__name__)

    # Input on toolshelf before execution --------------------------
    #  In Panel subclass, In bpy.types.Operator subclass, reference them by context.scene.~.
    bpy.types.Scene.draw_start_frame = bpy.props.IntProperty(
        name = "Start Frame",
        description = "Set start frame",
        default = 1
    )
    bpy.types.Scene.draw_end_frame = bpy.props.IntProperty(
        name = "End Frame",
        description = "Set end frame",
        default = 100
    )

def unregister():
    # Delete bpy.types.Scene.~.
    del bpy.types.Scene.draw_start_frame
    del bpy.types.Scene.draw_end_frame
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
