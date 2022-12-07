import roslib
import rospy
import tf
from copy import deepcopy
import geometry_msgs.msg
import numpy as np
from scipy.spatial.transform import Rotation

class VRPNtf():
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self._quat = [0.0, 0.0, 0.0, 1.0]
        self.quat = [0.0, 0.0, 0.0, 1.0]
    
    def projection(self, msg):

        msg.pose.position.z = 0.0
        self._quat[0] = msg.pose.orientation.x
        self._quat[1] = msg.pose.orientation.y
        self._quat[2] = msg.pose.orientation.z
        self._quat[3] = msg.pose.orientation.w

        _r = Rotation.from_quat(self._quat)
        euler = _r.as_euler('xyz', degrees=True)
        euler[0] = 0.0
        euler[1] = 0.0
        r = Rotation.from_euler('xyz', euler, degrees=True)
        self.quat = r.as_quat()

        msg.pose.orientation.x = self.quat[0]
        msg.pose.orientation.y = self.quat[1]
        msg.pose.orientation.z = self.quat[2]
        msg.pose.orientation.w = self.quat[3]

        return msg

    def inverse(self, msg):

        self.x = msg.pose.position.x
        self.y = msg.pose.position.y
        self.z = msg.pose.position.z
        self._quat[0] = msg.pose.orientation.x
        self._quat[1] = msg.pose.orientation.y
        self._quat[2] = msg.pose.orientation.z
        self._quat[3] = msg.pose.orientation.w
        # Get rotation
        _r = Rotation.from_quat(self._quat)
        mat = _r.as_matrix()
        # Make TF and inverse
        vr = np.array([0, 0, 0])
        hr = np.array([[1], [-1], [0], [1]])
        mat = np.vstack((mat, vr))
        mat = np.hstack((mat, hr))
        inv_mat = np.linalg.inv(mat)
        # From inv TF to rot mat, vec, quat
        rot_mat = inv_mat[0:3, 0:3]
        vec = inv_mat[0:3, 3:4].reshape(3)
        r = Rotation.from_matrix(rot_mat)
        self.quat = r.as_quat()

        return vec, self.quat

    def calibrate(self):
        pass

    
    
default = VRPNtf()
thistime = geometry_msgs.msg.PoseStamped()
thistime.pose.position.x = 62
thistime.pose.position.y = 11.6
thistime.pose.position.z = 9.5
thistime.pose.orientation.x = -0.719
thistime.pose.orientation.y = 1.816
thistime.pose.orientation.z = 3.274
thistime.pose.orientation.w = 0.694
q = default.projection(thistime)
print(q.pose.orientation)
## q should be [0.         0.         0.99728543 0.07363264]
# vec, quat = default.inverse(thistime)
# print(vec)
# print(quat)
