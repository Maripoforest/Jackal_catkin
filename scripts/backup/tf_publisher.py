import roslib
import rospy
import tf
import geometry_msgs.msg

from vrpn_trans import VRPNtf

object_frame = VRPNtf()

def callBack(msg):
    global object_frame
    rospy.loginfo(msg)
    object_frame.projection(msg)
    

def phantom_generator():
    global object_frame
    br = tf.TransformBroadcaster()
    Or = tf.TransformBroadcaster()
    sub = rospy.Subscriber('/vrpn_client_node/Jackal/pose', geometry_msgs.msg.PoseStamped, callBack)
    rate = rospy.Rate(50)
    print('Start to send Object_link')
    while not rospy.is_shutdown():
        Or.sendTransform((0.0, 0.0, 0.0), 
                        (0.0, 0.0, 0.0, 1.0),
                        rospy.Time.now(),
                        "odom",
                        "odom_link")

        br.sendTransform((object_frame.x, object_frame.y, 0.0), 
                        (object_frame.quat[0], object_frame.quat[1], object_frame.quat[2], object_frame.quat[3]),
                        rospy.Time.now(),
                        "object_link",
                        "odom_link")
        
        # rate.sleep()

if __name__ == '__main__':
    rospy.init_node('vrpn_state_publisher')
    try:
        phantom_generator()
    except rospy.InterruptedError():
        pass
