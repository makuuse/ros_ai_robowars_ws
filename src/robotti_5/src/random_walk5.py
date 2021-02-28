#!/usr/bin/python3

import rospy, random, math, time
from nav_msgs.msg import Odometry
from std_msgs.msg import Float64

def callback(data):

    vel_bl_msg = Float64()
    vel_br_msg = Float64()
    vel_fl_msg = Float64()
    vel_fr_msg = Float64()
    position_x = data.pose.pose.position.x 
    position_y = data.pose.pose.position.y 

    print(position_x, ":", position_y)
    
    velocity_bl = 0
    velocity_br = 0

    if position_x < 0.65:
        velocity_bl = 0
        velocity_br = 0
        time.sleep(1)
        velocity_bl = 4
        velocity_br = 4
        time.sleep(0.1)
        velocity_bl = -8
        velocity_br = -3
    
    elif position_y < 0.35:
        velocity_bl = 0
        velocity_br = 0
        time.sleep(1)
        velocity_bl = 4
        velocity_br = 4
        time.sleep(0.1)
        velocity_bl = -8
        velocity_br = -3

    elif position_x > 2.4:
        velocity_bl = 0
        velocity_br = 0
        time.sleep(1)
        velocity_bl = 4
        velocity_br = 4
        time.sleep(0.1)
        velocity_bl = -3
        velocity_br = -8

    elif position_y > 2.2:
        velocity_bl = 0
        velocity_br = 0
        time.sleep(1)
        velocity_bl = 4
        velocity_br = 4
        time.sleep(0.1)
        velocity_bl = -3
        velocity_br = -8

    else:
        velocity_bl = random.uniform(-0.1, -10)
        velocity_br = random.uniform(-0.1, -10)
        time.sleep(0.5)

    velocity_fl = velocity_bl-1.0
    velocity_fr = velocity_br-1.0

    vel_bl_msg.data = velocity_bl
    vel_br_msg.data = velocity_br
    vel_fl_msg.data = velocity_fl
    vel_fr_msg.data = velocity_fr

    velocity_bl_publisher.publish(vel_fl_msg)
    velocity_br_publisher.publish(vel_fr_msg)
    velocity_fl_publisher.publish(vel_fl_msg)
    velocity_fr_publisher.publish(vel_fr_msg)


if __name__ == "__main__":

    while not rospy.is_shutdown():
        
        rospy.init_node("random_walk_robot5")

        velocity_bl_publisher = rospy.Publisher('/robot5/wheel_bl_velocity_controller/command', Float64, queue_size = 1)
        velocity_br_publisher = rospy.Publisher('/robot5/wheel_br_velocity_controller/command', Float64, queue_size = 1)
        velocity_fl_publisher = rospy.Publisher('/robot5/wheel_fl_velocity_controller/command', Float64, queue_size = 1)
        velocity_fr_publisher = rospy.Publisher('/robot5/wheel_fr_velocity_controller/command', Float64, queue_size = 1)

        rospy.Subscriber("/robot5/odom", Odometry, callback)
        rospy.spin()

