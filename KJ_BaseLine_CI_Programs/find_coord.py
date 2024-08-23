import numpy as np

def call_find_coord(dist, coord1,coord2):
    p1 = np.array(coord1)
    p2 = np.array(coord2)
    # print(" coordinates given ")
    # print(p1,p2)
    q = np.array(coord2)
    v = p2 - p1
    u = v / np.linalg.norm(v)   
    point_on_line = q + dist * u
    return point_on_line