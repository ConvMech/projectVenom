#!/usr/bin/env python

import sys
import rospy
from mavros_msgs.srv import *
import mavros

def mavros_service_set():
    rospy.wait_for_service('/mavros/set_stream_rate')
    try:
        set_stream_rate = rospy.ServiceProxy('/mavros/set_stream_rate', StreamRate)
        set_stream_rate(0,60,1)
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e
    print "Service call success"

if __name__ == "__main__":
    print("try calling mavros_service ... ")
    mavros_service_set()
    
