import sys
import os

top_path = os.path.dirname(os.path.abspath(''))
if not top_path in sys.path:
    sys.path.append(top_path)

import rospy
import numpy as np
import tf2_ros
import geometry_msgs.msg

# from tools.obj_manager import ObjGround, ObjDrill, ObjJaw
# from tools.pose_and_trans import build_T, build_trans, T_2_trans

def build_trans(rot, vec, frame_id, child_frame_id):
    # Process quaternion
    if rot.size == 9:
        qua = R.from_matrix(rot)
        qua = qua.as_quat()
    # Process rotation matrix
    elif rot.size == 4:
        qua = rot
    else:
        print("The size of rotation matrix is invalid!")
        return None
   
    transform_stamped = geometry_msgs.msg.TransformStamped()
    transform_stamped.header.stamp = rospy.Time.now()
    transform_stamped.header.frame_id = frame_id
    transform_stamped.child_frame_id = child_frame_id
    transform_stamped.transform.translation.x = vec[0]
    transform_stamped.transform.translation.y = vec[1]
    transform_stamped.transform.translation.z = vec[2]
    transform_stamped.transform.rotation.x = qua[0]
    transform_stamped.transform.rotation.y = qua[1]
    transform_stamped.transform.rotation.z = qua[2]
    transform_stamped.transform.rotation.w = qua[3]
   
    return transform_stamped

# T_e_tip
rospy.init_node('phantomodom')
rot_e_tip = np.array([0, 0, 0, 1])
vec_e_tip = np.array([0, 0, 0])
ts_e_tip = build_trans(rot_e_tip, vec_e_tip, 'odom', 'zero_link')
broad_e_tip = tf2_ros.StaticTransformBroadcaster()
broad_e_tip.sendTransform(ts_e_tip)