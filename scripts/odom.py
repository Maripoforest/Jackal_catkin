import rospy
import tf
import nav_msgs.msg
import geometry_msgs.msg
import math
import numpy as np
from scipy.spatial.transform import Rotation
from vrpn_trans import VRPNtf


#======================================================================


opti_pose = geometry_msgs.msg.PoseStamped()
last_pose = geometry_msgs.msg.PoseStamped()
opti_twist = geometry_msgs.msg.Twist()
projection_pose = VRPNtf()
i = 0

#======================================================================


def to_quat(msg):
    quat = []
    quat.append(msg.pose.orientation.x)
    quat.append(msg.pose.orientation.y)
    quat.append(msg.pose.orientation.z)
    quat.append(msg.pose.orientation.w)
    return quat


#======================================================================


def callBack(msg):

    global opti_pose, projection_pose, last_pose, opti_twist, i

    i += 1
    

    if (i%5 == 0):
        last_pose = opti_pose
        opti_pose = projection_pose.projection(msg)
        r = Rotation.from_quat(to_quat(opti_pose))
        _r = Rotation.from_quat(to_quat(last_pose))
        m = r.as_matrix()
        _m = _r.as_matrix()
        ca = m[0][0]
        _ca = _m[0][0]
        a = math.acos(ca)
        _a = math.acos(_ca)
        da = a - _a
        dt = (opti_pose.header.stamp.secs - last_pose.header.stamp.secs) + (opti_pose.header.stamp.nsecs - last_pose.header.stamp.nsecs) * (pow(10, -9))
        vx = (opti_pose.pose.position.x - last_pose.pose.position.x)/dt
        vy = (opti_pose.pose.position.y - last_pose.pose.position.y)/dt
        v_m = np.array([vx, vy, 1.0])
        v = np.dot(v_m, m)
        print(v[0])
        opti_twist.linear.x = v[0]
        opti_twist.angular.z = da / dt
        i = 0


#======================================================================


if __name__ == '__main__':

    rospy.init_node('odometry_publisher')
    odom_pub = rospy.Publisher('odom', nav_msgs.msg.Odometry, queue_size=50)
    opti_sub = rospy.Subscriber('/vrpn_client_node/Jackal/pose', geometry_msgs.msg.PoseStamped, callBack)
    odom_broadcaster = tf.TransformBroadcaster()

    rate = rospy.Rate(1.0)
    while not rospy.is_shutdown():

        current_time = rospy.Time.now()
        
        odom_broadcaster.sendTransform(
            (opti_pose.pose.position.x, opti_pose.pose.position.y, 0.0),
            (opti_pose.pose.orientation.x, opti_pose.pose.orientation.y, opti_pose.pose.orientation.z, opti_pose.pose.orientation.w),
            current_time,
            'object_link',
            'odom'
        )  

        odom = nav_msgs.msg.Odometry()
        odom.header.stamp = current_time
        odom.header.frame_id = 'odom'
        odom.child_frame_id = 'base_link'
        odom.pose.pose = opti_pose.pose
        odom.twist.twist = opti_twist

        odom_pub.publish(odom)

        rate.sleep()
        


        

