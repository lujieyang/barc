#!/usr/bin/env python

import rospy
import time
from barc.msg import ECU
from geometry_msgs.msg import Twist

acc = 0.0
d_f = 0.0    

    
# ecu command update
def measurements_callback(data):
    global acc,d_f
    acc = data.linear.x
    d_f = data.angular.z
    
        

    
# ==========end of the controller==============#
    
# controller node
def teleop():
    # initialize node
    rospy.init_node('teleop', anonymous=True)
    
    # topic subscriptions / publications
    #global msg
    #msg = Twist()
    #teleopnode = rospy.Publisher('keyboard/keyup',Twist, queue_size = 16)
    relay_node = rospy.Subscriber('keyboard/keyup',Twist, measurements_callback)
    state_pub = rospy.Publisher('ecu', ECU, queue_size = 10)
    
    # set node rate
    loop_rate = 50
    rate = rospy.Rate(loop_rate)
    
    
    while not rospy.is_shutdown():
        global acc,d_f
    
        # publish information
        state_pub.publish( ECU(acc, d_f) )
    
        # wait
        rate.sleep()
    
if __name__ == '__main__':
    try:
        teleop()
    except rospy.ROSInterruptException:
        pass
