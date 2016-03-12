import bpy

# Main function.
def autoDraw(frame_range=None, basic=None, bl_render=None,
             material=None, world=None, modifier=None,
             sort=None, freestyle_preset=None, line_thick=None):
    
    # Loop through selected objects.
    selected_objects = bpy.context.selected_objects
    for selected_object in selected_objects:
        
        bpy.ops.object.select_all(action='DESELECT')
        selected_object.select = True
        bpy.context.scene.objects.active = selected_object
        
        # Only work for mesh, curve, or text.
        if bpy.context.object.type in ['MESH','CURVE','FONT']:
            # Default value is [1,100].
            if frame_range == None:
                frame_range = [1, 100]
            else:
                frame_range = frame_range
    
            # Turn on/off each step--------------------
            if basic == True:
                addBuildFreestyle(frame_range)
    
            if bl_render == True:
                goBlRender()

            if material == True:
                makeMaterial()

            if world == True:
                makeWorld()

            if modifier == True:
                addModifiers()
    
            # Sort faces for order of build modifier.
            if sort == 'CAMERA':
                cameraViewSort()
            elif sort in ['VIEW_ZAXIS', 'VIEW_XAXIS', 'MATERIAL', 'CURSOR_DISTANCE', 'SELECTED', 'RANDOMIZE', 'REVERSE']:
                changeSort(sort)
            elif sort == 'NONE':
                pass
            else:
                pass
    
            # Apply a freestyle setting.
            if freestyle_preset != None:
                setFreestylePreset(freestyle_preset)
    
            # Change line thickness.
            if line_thick == None:
                line_thick = 2
            bpy.context.scene.render.line_thickness = line_thick

# Activate build modifier and freestyle.
def addBuildFreestyle(frame_range):
    # if Build modifier is absent, add it.
    if 'Build_auto-drawing' not in bpy.context.object.modifiers.keys():
        bpy.ops.object.modifier_add(type='BUILD')
        bpy.context.object.modifiers[-1].name = 'Build_auto-drawing'

    # Frame duration is end frame - start frame.
    bpy.context.object.modifiers['Build_auto-drawing'].frame_start = frame_range[0]
    bpy.context.object.modifiers['Build_auto-drawing'].frame_duration = frame_range[1] - frame_range[0]
    changeEndFrame(frame_range)
    
    # Activate freestyle.
    bpy.context.scene.render.use_freestyle = True

# Set length of animation frame as end frame of build modifier.
def changeEndFrame(frame_range):
    if frame_range[1] > bpy.context.scene.frame_end:
        bpy.context.scene.frame_end = frame_range[1]

# Change rendering engine into Blender render.
def goBlRender():
    bpy.context.scene.render.engine = 'BLENDER_RENDER'

# Add pure white material on object.
def makeMaterial():
    # Make material.
    bpy.ops.material.new()
    mat = bpy.data.materials[-1]

    # Remove all in material slot and append the new material.
    for m in bpy.context.object.data.materials:
        bpy.ops.object.material_slot_remove()
    bpy.context.object.data.materials.append(mat)

    # White and shadeless.
    mat.diffuse_color = (1, 1, 1)
    mat.use_shadeless = True

# Set pure white world for Blender render.
def makeWorld():
    # Pure white.
    bpy.context.scene.world.horizon_color = (1, 1, 1)

# Apply preset modifier.
def addModifiers():
    # if subsurf modifier already exists, remove it.
    if 'Subsurf_auto-drawing' in bpy.context.object.modifiers.keys():
        bpy.ops.object.modifier_remove(modifier='Subsurf_auto-drawing')
    
    # Already add it at the end of modifeir stack.
    bpy.ops.object.modifier_add(type='SUBSURF')
    bpy.context.object.modifiers[-1].name = 'Subsurf_auto-drawing'

# Sort order of faces for build modifier.
def changeSort(sort_type=None):
    sort_type_values = ['VIEW_ZAXIS', 'VIEW_XAXIS', 'MATERIAL', 'CURSOR_DISTANCE', 'SELECTED', 'RANDOMIZE', 'REVERSE']
    if bpy.context.object.type == 'MESH':
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.sort_elements(type=sort_type, elements={'FACE'})
        bpy.ops.object.mode_set(mode='OBJECT')
    else:
        print("Cannot sort except MESH object!")

# Sort method by distance from camera.
def cameraViewSort():
    # Change cursor to the location of camera.
    cam = bpy.data.objects[bpy.data.cameras[0].name]
    bpy.context.scene.cursor_location = cam.location
    changeSort(sort_type='CURSOR_DISTANCE')

# Set a freestyle preset.
def setFreestylePreset(freestyle_preset):
    linestyle = bpy.data.linestyles["LineStyle"]
    
    # NONE.
    if freestyle_preset == 'NONE':
        disableFreestyleModifiers()

    # MERKER_PEN.
    if freestyle_preset == 'MARKER_PEN':
        disableFreestyleModifiers()
        
        if 'Along Stroke' not in linestyle.color_modifiers.keys():
            bpy.ops.scene.freestyle_color_modifier_add(type='ALONG_STROKE')
        linestyle.color_modifiers['Along Stroke'].use = True
        linestyle.color_modifiers['Along Stroke'].color_ramp.elements[0].position = 0.752
        linestyle.color_modifiers['Along Stroke'].color_ramp.elements[1].color = (0.156, 0.156, 0.156, 1)
    
    # BRUSH_PEN.
    if freestyle_preset == 'BRUSH_PEN':
        disableFreestyleModifiers()
        
        if 'Along Stroke' not in linestyle.thickness_modifiers.keys():
            bpy.ops.scene.freestyle_thickness_modifier_add(type='ALONG_STROKE')
        linestyle.thickness_modifiers['Along Stroke'].use = True
        linestyle.thickness_modifiers['Along Stroke'].value_min = 0.7
        linestyle.thickness_modifiers['Along Stroke'].value_max = 3
    
    # SCRIBBLE.
    if freestyle_preset == 'SCRIBBLE':
        disableFreestyleModifiers()
        
        if 'Along Stroke' not in linestyle.thickness_modifiers.keys():
            bpy.ops.scene.freestyle_thickness_modifier_add(type='ALONG_STROKE')
        linestyle.thickness_modifiers['Along Stroke'].use = True
        linestyle.thickness_modifiers['Along Stroke'].value_min = 0.7
        linestyle.thickness_modifiers['Along Stroke'].value_max = 3
        
        if '2D Offset' not in linestyle.geometry_modifiers.keys():
            bpy.ops.scene.freestyle_geometry_modifier_add(type='2D_OFFSET')
        linestyle.geometry_modifiers['2D Offset'].use = True
        linestyle.geometry_modifiers['2D Offset'].end = 4
    
    # FREE_HAND.
    if freestyle_preset == 'FREE_HAND':
        disableFreestyleModifiers()
        
        if 'Calligraphy' not in linestyle.thickness_modifiers.keys():
            bpy.ops.scene.freestyle_thickness_modifier_add(type='CALLIGRAPHY')
        linestyle.thickness_modifiers['Calligraphy'].use = True
        linestyle.thickness_modifiers['Calligraphy'].thickness_max = 7
        
        if 'Polygonalization' not in linestyle.geometry_modifiers.keys():
            bpy.ops.scene.freestyle_geometry_modifier_add(type='POLYGONIZATION')
        linestyle.geometry_modifiers['Polygonalization'].use = True
        linestyle.geometry_modifiers['Polygonalization'].error = 3
    
    # CHILDISH.
    if freestyle_preset == 'CHILDISH':
        disableFreestyleModifiers()
        
        if 'Calligraphy' not in linestyle.thickness_modifiers.keys():
            bpy.ops.scene.freestyle_thickness_modifier_add(type='CALLIGRAPHY')
        linestyle.thickness_modifiers['Calligraphy'].use = True
        linestyle.thickness_modifiers['Calligraphy'].thickness_max = 10
        
        if 'Along Stroke' not in linestyle.color_modifiers.keys():
            bpy.ops.scene.freestyle_color_modifier_add(type='ALONG_STROKE')
        linestyle.color_modifiers['Along Stroke'].use = True
        linestyle.color_modifiers['Along Stroke'].color_ramp.elements[1].color = (0.128, 0.128, 0.128, 1)
        
        if 'Polygonalization' not in linestyle.geometry_modifiers.keys():
            bpy.ops.scene.freestyle_geometry_modifier_add(type='POLYGONIZATION')
        linestyle.geometry_modifiers['Polygonalization'].use = True
        linestyle.geometry_modifiers['Polygonalization'].error = 5
        
        if 'Backbone Stretcher' not in linestyle.geometry_modifiers.keys():
            bpy.ops.scene.freestyle_geometry_modifier_add(type='BACKBONE_STRETCHER')
        linestyle.geometry_modifiers['Backbone Stretcher'].use = True
        linestyle.geometry_modifiers['Backbone Stretcher'].backbone_length = 3

# Turn off Freestyle Modifiers.
def disableFreestyleModifiers():
    for modifier in bpy.data.linestyles["LineStyle"].thickness_modifiers:
        modifier.use = False
    for modifier in bpy.data.linestyles["LineStyle"].geometry_modifiers:
        modifier.use = False
    for modifier in bpy.data.linestyles["LineStyle"].color_modifiers:
        modifier.use = False