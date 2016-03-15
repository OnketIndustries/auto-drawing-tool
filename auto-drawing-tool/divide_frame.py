import bpy
import math
import mathutils

# Caltulate kd-tree.
def _kdFind(data, point):
    size = len(data)
    kd = mathutils.kdtree.KDTree(size)
    
    for i, d in enumerate(data):
        kd.insert(d, i)

    kd.balance()
    
    co, index, dist = kd.find(point)
    
    return [co, index, dist]

# kd-tree for vertex and curve's point.
def _kdFindNearestPoint(obj, point=(0,0,0)):
    # Change into world coordinate.
    world_verts = [obj.matrix_world * v.co for v in obj.data.vertices]
    result = _kdFind(world_verts, point)
    result.append(obj)
    # return [coordinate, vertex index, distance, object].
    return result

# kd-tree looping through objects and curve's point.
def _addNearestObject(objects, point):
    nearest = {'distance': 10000, 'data':[], 'object': None}
    for obj in objects:
        near_result = _kdFindNearestPoint(obj=obj, point=point)
        if near_result[2] < nearest['distance']:
            nearest['distance'] = near_result[2]
            nearest['object'] = near_result[3]
            nearest['coordinate'] = near_result[0]
            nearest['vertex_index'] = near_result[1]
    # return {'distance': n, 'object': obj, 'coordinate': vec, 'vertex_index': n}
    return nearest

# Sort object by nearer vertex to curve's point.
def sortObjectAlongCurve(objects, bezier_points):
        # Forloop index for correspoinding curve to each point.
        step = len(bezier_points) / len(objects)
        bezier_points_index = [math.floor(step*i) for i in range(len(objects))]
        
        sorted_objects = []
        sorted_objects_info = []
        
        # Make list in order of nearest object to a curve's point.curve.
        for i in bezier_points_index:
            point_co = bezier_points[i].co
            
            # Nearest object to the curve's point.
            nearest_object = _addNearestObject(objects=objects, point=point_co)
            
            objects.remove(nearest_object['object'])

            sorted_objects.append(nearest_object['object'])
            sorted_objects_info.append(nearest_object)
            
        return sorted_objects, sorted_objects_info

# Divide frame by the number of selected objects.
def divideFrame(objects, frame_range):
    frame_duration = (frame_range[1] + 1) - frame_range[0]
    frame_step = math.floor(frame_duration / len(objects))
    return frame_step
