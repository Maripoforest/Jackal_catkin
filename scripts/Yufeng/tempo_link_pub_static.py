#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 17:29:09 2022

@author: eidos
"""

import sys
import rospy
import tf2_ros

# import tf

import geometry_msgs.msg

if __name__ == '__main__':
    rospy.init_node('odom_phantom')
    # Broadcaster
    broadcaster = tf2_ros.StaticTransformBroadcaster()
    
    camera_link_transformStamped = geometry_msgs.msg.TransformStamped()
    camera_link_transformStamped.header.stamp = rospy.Time.now()
    camera_link_transformStamped.header.frame_id = "odom"
    camera_link_transformStamped.child_frame_id = "odom_link"
    camera_link_transformStamped.transform.rotation.w = 1.0
    
    broadcaster.sendTransform(camera_link_transformStamped)
    
    # try:
    #     rospy.spin()
    # except:
    #     pass
    