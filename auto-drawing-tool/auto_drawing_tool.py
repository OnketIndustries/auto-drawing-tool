import bpy

# Main function.
def autoDraw(frame_range=None, basic=None, bl_render=None,
             material=None, world=None, modifier=None,
             sort=None, freestyle_preset=None, line_thick=None):
    
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
    if freestyle_preset != None or 'NONE':
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
    if freestyle_preset == 'MARKER_PEN':
        bpy.context.scene.render.line_thickness = 2 
        bpy.ops.scene.freestyle_color_modifier_add(type='ALONG_STROKE')
        bpy.data.linestyles['LineStyle'].color_modifiers['Along Stroke'].color_ramp.elements[0].position = 0.752
        bpy.data.linestyles['LineStyle'].color_modifiers['Along Stroke'].color_ramp.elements[1].color = (0.156, 0.156, 0.156, 1)

    if freestyle_preset == 'BRUSH_PEN':
        bpy.context.scene.render.line_thickness = 2
        bpy.ops.scene.freestyle_thickness_modifier_add(type='ALONG_STROKE')
        bpy.data.linestyles['LineStyle'].thickness_modifiers['Along Stroke'].value_min = 0.7
        bpy.data.linestyles['LineStyle'].thickness_modifiers['Along Stroke'].value_max = 3
    
    if freestyle_preset == 'SCRIBBLE':
        bpy.context.scene.render.line_thickness = 2
        bpy.ops.scene.freestyle_thickness_modifier_add(type='ALONG_STROKE')
        bpy.data.linestyles['LineStyle'].thickness_modifiers['Along Stroke'].value_min = 0.7
        bpy.data.linestyles['LineStyle'].thickness_modifiers['Along Stroke'].value_max = 3
        bpy.ops.scene.freestyle_geometry_modifier_add(type='2D_OFFSET')
        bpy.data.linestyles['LineStyle'].geometry_modifiers['2D Offset'].end = 4

    if freestyle_preset == 'FREE_HAND':
        bpy.ops.scene.freestyle_thickness_modifier_add(type='CALLIGRAPHY')
        bpy.data.linestyles['LineStyle'].thickness_modifiers['Calligraphy'].thickness_max = 7
        bpy.ops.scene.freestyle_geometry_modifier_add(type='POLYGONIZATION')
        bpy.data.linestyles['LineStyle'].geometry_modifiers['Polygonalization'].error = 3
    
    if freestyle_preset == 'CHILDISH':
        bpy.ops.scene.freestyle_thickness_modifier_add(type='CALLIGRAPHY')
        bpy.data.linestyles['LineStyle'].thickness_modifiers['Calligraphy'].thickness_max = 10
        bpy.ops.scene.freestyle_color_modifier_add(type='ALONG_STROKE')
        bpy.data.linestyles['LineStyle'].color_modifiers['Along Stroke'].color_ramp.elements[1].color = (0.128, 0.128, 0.128, 1)
        bpy.ops.scene.freestyle_geometry_modifier_add(type='POLYGONIZATION')
        bpy.data.linestyles['LineStyle'].geometry_modifiers['Polygonalization'].error = 5
        bpy.ops.scene.freestyle_geometry_modifier_add(type='BACKBONE_STRETCHER')
        bpy.data.linestyles['LineStyle'].geometry_modifiers['Backbone Stretcher'].backbone_length = 3