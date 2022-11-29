import roslib
import rospy
import tf2_ros
import geometry_msgs.msg
from copy import deepcopy

from scipy.spatial.transform import Rotation
from vrpn_trans import VRPNtf

flag = False
jackal_origin = geometry_msgs.msg.TransformStamped()
jackal_origin.header.frame_id = 'odom'
jackal_origin.child_frame_id = 'calibrated_origin'
inverter = VRPNtf()

def callBack(msg):
    global jackal_origin

    jackal_origin.header.stamp = rospy.Time.now()
    jackal_origin.header.frame_id = 'odom'
    jackal_origin.child_frame_id = 'calibrated_origin'
    vec, rot = inverter.inverse(msg)
    jackal_origin.transform.translation.x = vec[0]
    jackal_origin.transform.translation.x = vec[1]
    jackal_origin.transform.translation.x = vec[2]
    jackal_origin.transform.rotation.x = rot[0]
    jackal_origin.transform.rotation.y = rot[1]
    jackal_origin.transform.rotation.z = rot[2]
    jackal_origin.transform.rotation.w = rot[3]
    
def start_calibration():
    sub = rospy.Subscriber('/vrpn_client_node/Jackal/pose', geometry_msgs.msg.PoseStamped, callBack)
    s = input('calibrating starts\n')
    while not rospy.is_shutdown():
        if(s == ''):
            goal = deepcopy(jackal_origin)
            rospy.loginfo(goal)
            per = input('Take this sample? (yes/no) \n')
            if (per == '' or per == 'yes'):
                rospy.loginfo('static_tf_send')
                bc = tf2_ros.StaticTransformBroadcaster()
                bc.sendTransform(goal)
                break
            else:
                continue
        else:
            s = input('Take another sample\n')
    

if __name__ == '__main__':
    rospy.init_node('calibration')
    try:
        start_calibration()
    except rospy.ROSInterruptException():
        pass