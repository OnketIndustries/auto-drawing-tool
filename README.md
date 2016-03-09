# Auto Drawing Tool
A blender's add-on: Freestyle with build modifier.

## Installation
1. Download the [zip file](https://github.com/squarednob/auto-drawing-tool/raw/master/auto-drawing-tool.zip).
2. In Blender, go to File > Use Preferences > Add-ons, click "Install from file", and select the zip file.
3. Activate "Animation: Auto Drawing Tool" in Animation category.

---

## Basic Usage
1. Select an object.
2. Go to toolshelf on the left of 3D view. In Animation tab, there is "Auto Drawing Tool" box.
3. Set start frame and end frame for the animation, then click on "Set Auto Drawing" button.
4. Render animation.

---

## Options
Option setting panel coms in bottom left of 3D view, after click "Set Auto Drawing" button.

###Enable/Disable process
You can turn on or off each settings for auto drawing.
1. Buld Modifier & Freestyle.
2. Blender Render.
3. Pure White Material.
4. Pure White World.
5. Subsurf Modifier.

### Change Drawing Order
Change order for build modifier by sorting index of face.

* "NONE" = Default index of face for the object.
* "REVERSE" = Reveres the order of default index.
* "CURSOR_DISTANCE" = Sort from nearest face to cursor.
* "CAMERA" = Sort from nearest face to camera.
* "VIEW_ZAXIS" = Sort along with Z axis.
* "VIEW_XAXIS" = Sort along with X axis.
* "SELECTED" = Sort from selected face.
* "MATERIAL" = Sort by material.

### Freestyle Preset
Change the line style by freestyle preset.

* "NONE" = Default setting of freetyle.
* "MARKER PEN" = Bolder line.
* "BRUSH_PEN" = Different thickness line from start to end.
* "SCRIBBLE" = Rough line.
* "FREE_HAND" = Rough line and rough shape.
* "CHILDISH" = More rough like child's drawing.
