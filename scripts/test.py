# from scipy.spatial.transform import Rotation
# import numpy as np
# # rq = [-0.719, 1.876, 3.274, 0.694]

# # print(rq)
# # r = Rotation.from_quat(rq)
# # euler = r.as_euler('xyz', degrees=True)
# # euler[0] = 0
# # euler[1] = 0
# # r_changed = Rotation.from_euler('xyz', euler, degrees=True)
# # quaternion = r_changed.as_quat()
# # print(quaternion)

# arr = [[-0.86699143, -0.47655464, -0.14567612, 1],
#         [0.128727,   -0.4965889,   0.85838734, -1],
#         [-0.48140961,  0.72546202,  0.49188377, 0],
#         [0, 0, 0, 1]]

# inv_arr = np.linalg.inv(arr)
# print(inv_arr)


# class Test():
#         def __init__(self):
#                 self.x = 0
#                 self.y = 20
        
#         def project(self, best):
#                 self.x = best.x
#                 best.x = self.x * self.y
#                 return best
                
# b = Test()
# b.x = 10
# t = Test()
# b = t.project(b)
# print(b.x)


# import rospy
# import geometry_msgs.msg
# import nav_msgs.msg

# o = nav_msgs.msg.Odometry()
# p = geometry_msgs.msg.PoseStamped()

# p.pose.position.x = 25
# p.pose.orientation.x = 25
# o.pose.pose = p.pose
# print(o)

# from scipy.spatial.transform import Rotation
# import numpy as np
# import math
# x = [0, 0, 30]
# r = Rotation.from_euler('xyz',x, degrees=True)
# m = r.as_matrix()
# print(m)

# import rospy
# import tf

# tl = tf.Transformer()
# while not rospy.is_shutdown():
#     tw = tl.lookupTwist('base_link', 'odom', rospy.Time(0.0), rospy.Duration(4.001))
#     rospy.loginfo(tw)

# print(pow(10, -9))
import numpy as np
x = np.array([3.0, 5.0, 1.0]).reshape(1, 3)
print(x)
y = np.array([[0.707, 0.707, 0.0], [0.707, 0.707, 0], [0.0, 0.0, 1.0]]).reshape(3, 3)
print(y.shape)
z = np.dot(x, y)
print(z[0])

