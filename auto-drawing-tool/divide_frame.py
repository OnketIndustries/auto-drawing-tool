import bpy
import math
import mathutils

# kd-treeのベース関数：
def kdFind(data, point):
    # サイズを入力：
    size = len(data)
    kd = mathutils.kdtree.KDTree(size)
    
    for i, d in enumerate(data):
        kd.insert(d, i)
    # 分割したデータ数を均等にするために、かならずfindの前に必要：
    kd.balance()
    # ある点に距離が近いものを挙げる：
    co, index, dist = kd.find(point)
    return [co, index, dist]

# オブジェクトのvertexをworld座標に変換してkd-tree実行：
def kdFindNearestPoint(obj, point=(0,0,0)):
    world_verts = [obj.matrix_world * v.co for v in obj.data.vertices]
    result = kdFind(world_verts, point)
    # 指標のために、オブジェクトをリストの最後に加えてreturn。
    result.append(obj)
    # return [座標, vertex番号, 距離,　オブジェクト]：
    return result

def addNearestObject(objects, point):
    nearest = {'distance': 10000, 'data':[], 'object': None}
    for obj in objects:
        # curveの0点に近いオブジェクトのvertexを挙げる。[座標, vertex番号, 距離,　オブジェクト]が出る。
        near_result = kdFindNearestPoint(obj=obj, point=point)
        if near_result[2] < nearest['distance']:
            nearest['distance'] = near_result[2]
            nearest['object'] = near_result[3]
            nearest['coordinate'] = near_result[0]
            nearest['vertex_index'] = near_result[1]
    # return {'distance': n, 'object': obj, 'coordinate': 座標, 'vertex_index': vertex番号}
    return nearest

def sortObjectAlongCurve(objects, bezier_points):
        # curveの各pointに、いくつのオブジェクトを割り当てるかのリスト生成：
        step = len(bezier_points) / len(objects)
        bezier_points_index = [math.floor(step*i) for i in range(len(objects))]
        
        sorted_objects = []
        sorted_objects_info = []
        
        # curveのポイントの分だけ、最も近いオブジェクトをリストに入れる：
        for i in bezier_points_index:
            point_co = bezier_points[i].co
            
            # active_curveの0点と最も近いvertexを持つオブジェクト：
            nearest_object = addNearestObject(objects=objects, point=point_co)
            
            # ターゲットリストから削除する：
            objects.remove(nearest_object['object'])
            # 新しいオブジェクトリストに近い方から追加する：
            sorted_objects.append(nearest_object['object'])
            sorted_objects_info.append(nearest_object)
            
        return sorted_objects, sorted_objects_info

# 選択オブジェクトの数でbuildのフレームを分割：
def divideFrame(objects, frame_range):
    frame_duration = (frame_range[1] + 1) - frame_range[0]
    frame_step = math.floor(frame_duration / len(objects))
    return frame_step
