import rospy
import geometry_msgs.msg
from scipy.spatial.transform import Rotation

default = geometry_msgs.msg.PoseStamped()
default.pose.position.z = 0
default.pose.orientation.x = 0
default.pose.orientation.y = 0
default.header.frame_id = 'odom'

def callBack(msg):
    global default 

    ### position
    default.pose.position.x = msg.pose.position.x
    default.pose.position.y = msg.pose.position.y

    ### orientation
    _q = []
    _q.append(msg.pose.orientation.x)
    _q.append(msg.pose.orientation.y)
    _q.append(msg.pose.orientation.z)
    _q.append(msg.pose.orientation.w)
    # Transfer the quat to euler, erase roll and pitch
    _r = Rotation.from_quat(_q)
    euler = _r.as_euler('xyz', degrees=True)
    euler[0] = 0.0
    euler[1] = 0.0
    r = Rotation.from_euler('xyz', euler, degrees=True)
    quaternion = r.as_quat()
    default.pose.orientation.x = quaternion[0]
    default.pose.orientation.y = quaternion[1]
    default.pose.orientation.z = quaternion[2]
    default.pose.orientation.w = quaternion[3]

    ### TimeStamp
    default.header.stamp.secs = msg.header.stamp.secs
    default.header.stamp.nsecs = msg.header.stamp.nsecs



def run_the_jackal():
    global default

    ### ROS pub and sub, initial node
    pub = rospy.Publisher('/move_base_simple/goal', geometry_msgs.msg.PoseStamped, queue_size=10)
    sub = rospy.Subscriber('/vrpn_client_node/lefthand/pose', geometry_msgs.msg.PoseStamped, callBack)
    rospy.init_node('opti_commander', anonymous = True)
    rate = rospy.Rate(2)

    ### Package
    goal = geometry_msgs.msg.PoseStamped()
    goal = default
    i = 0
    while not rospy.is_shutdown():
        # hello_str = "hello world %s" % rospy.get_time()
        print('seq=', i)
        signal = input()
        if signal == '':
            goal.header.seq = i
            rospy.loginfo(goal)
            pub.publish(goal)
            rate.sleep()
            i += 1
        else:
            continue

if __name__ == '__main__':
    try:
        run_the_jackal()
    except rospy.ROSInterruptException:
        pass     


