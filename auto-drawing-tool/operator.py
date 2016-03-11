import bpy
from . import auto_drawing_tool

# Operation class.
class AutoDrawOperation(bpy.types.Operator):
    bl_idname = "scene.auto_drawing" # Access by bpy.ops.scene.auto_drawing.
    bl_label = "Set Auto drawing"
    bl_description = "Make auto drawing settings."
    bl_options = {'REGISTER', 'UNDO'}
    
    # Input after execution------------------------
    #  Reference by self.~ in execute().
    basic_check = bpy.props.BoolProperty(
        name = "1.Build Modifier & Freestyle",
        description = "Activate build modifier and freestyle.",
        default = True
    )
    blrender_check = bpy.props.BoolProperty(
        name = "2.Blender Render",
        description = "Go to Blender render engine.",
        default = True
    )
    world_check = bpy.props.BoolProperty(
        name = "3.Apply White World",
        description = "Set white world for Blender render",
        default = True
    )
    material_check = bpy.props.BoolProperty(
        name = "4.Apply White Shadeless Material",
        description = "Set shadeless white material.",
        default = True
    )
    modifier_check = bpy.props.BoolProperty(
        name = "5.Subsurf Modifier",
        description = "Apply subdivision surface.",
        default = False
    )
    line_thick_float = bpy.props.FloatProperty(
        name = "Line Thickness",
        description = "Set line thickness.",
        default = 2
    )
    freestyle_select = bpy.props.EnumProperty(
        name = "Freestyle Preset",
        description = "Set Freestyle Preset",
        items = [('NONE', 'NONE', "Locate on 3D cursor"),
                ('MARKER_PEN', 'MARKER_PEN', "Locate on 3D cursor"),
                ('BRUSH_PEN', 'BRUSH_PEN', "Locate on 3D cursor"),
                ('SCRIBBLE', 'SCRIBBLE', "Locate on 3D cursor"),
                ('FREE_HAND', 'FREE_HAND', "Locate on 3D cursor"),
                ('CHILDISH', 'CHILDISH', "Locate on 3D cursor")]
    )
    sort_select = bpy.props.EnumProperty(
        name = "Change Drawing Order(Only for MESH)",
        description = "Sort faces of mesh for build modifier.",
        items = [('NONE', 'NONE', "Locate on 3D cursor"),
                ('REVERSE', 'REVERSE', "Locate on 3D cursor"),
                ('CURSOR_DISTANCE', 'CURSOR_DISTANCE', "Locate on 3D cursor"),
                ('CAMERA', 'CAMERA', "Locate on 3D cursor"),
                ('VIEW_ZAXIS', 'VIEW_ZAXIS', "Locate on 3D cursor"),
                ('VIEW_XAXIS', 'VIEW_XAXIS', "Locate on 3D cursor"),
                ('SELECTED', 'SELECTED', "Locate on 3D cursor"),
                ('MATERIAL', 'MATERIAL', "Locate on 3D cursor")]
    )
    # -----------------------------------------

    '''
    @classmethod
    def poll(cls, context):
     return (context.object is not None)
    '''
    
    # Execute main function.
    def execute(self, context):
        sce = context.scene
        auto_drawing_tool.autoDraw(frame_range=[sce.draw_start_frame, sce.draw_end_frame],
             basic=self.basic_check, bl_render=self.blrender_check,
             material=self.material_check, world=self.world_check, modifier=self.modifier_check,
             sort=self.sort_select, freestyle_preset=self.freestyle_select, line_thick=self.line_thick_float)
        
        # Finish at end frame.
        bpy.context.scene.frame_current = sce.draw_end_frame
        # Finish with cursor at center.
        bpy.context.scene.cursor_location = [0,0,0]

        return {'FINISHED'}

# Menu and input settings.
class AutoDrawingPanel(bpy.types.Panel):
    bl_label = "Auto Drawing Tool"
    bl_idname = "auto_drawing_tool"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS" # Menu in toolsheld.
    bl_category = "Animation" # Menu on Tools tab.
    bl_context = (("objectmode")) # In object mode.
    
    # Input on Menu.
    def draw(self, context):
         sce = context.scene
         layout = self.layout
         
         row1 = layout.row()
         row1.prop(sce, "draw_start_frame") # bpy.types.Scene.draw_start_frame.
         row1.prop(sce, "draw_end_frame") # bpy.types.Scene.draw_end_frame.
         # Execute button for operator class.
         layout.operator(AutoDrawOperation.bl_idname)
