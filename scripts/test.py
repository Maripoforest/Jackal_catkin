from scipy.spatial.transform import Rotation

rq = [-0.719, 1.876, 3.274, 0.694]
rq[0:1] = 0
print(rq)
r = Rotation.from_quat(rq)
euler = r.as_euler('xyz', degrees=True)
euler[0] = 0
euler[1] = 0
r_changed = Rotation.from_euler('xyz', euler, degrees=True)
quaternion = r_changed.as_quat()
print(quaternion)