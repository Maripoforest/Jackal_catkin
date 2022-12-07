
import socket
import rospy
from geometry_msgs.msg import Twist
mess = None
flag = False

def callback(msg):
    global mess, flag
    vel = str(msg.linear.x)
    ang = str(msg.angular.z)
    mess = vel + '+' + ang
    flag = True

if __name__ == '__main__':
    rospy.init_node('leader_listener')
    sub = rospy.Subscriber('/twist_marker_server/cmd_vel', Twist, callback)
    while not rospy.is_shutdown():
        if flag:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            client_socket.settimeout(1.0)
            message = str.encode(mess)
            addr = ("192.168.3.5", 52001)
            print(message)
            client_socket.sendto(message, addr)