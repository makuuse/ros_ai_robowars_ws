#! /usr/bin/python3

import rospy, random, math, message_filters
from nav_msgs import Odometry
import angles
import csv
from tf.transformations import euler_from_quaternion

class Robot_position:

    def __init__(self):

        self.node = rospy.init_node("position_from_ultrasonic")
        self.reset_simulation_call = rospy.ServiceProxy("/gazebo/reset_simulation", Empty)
        self.us1_sub = message_filters.Subscriber('/ultrasonic1', Range) # Mitä topiccia halutaan kuunnella? 
        self.us2_sub = message_filters.Subscriber('/ultrasonic2', Range) # Mitä topiccia halutaan kuunnella? 
        self.us3_sub = message_filters.Subscriber('/ultrasonic3', Range) # Mitä topiccia halutaan kuunnella? 
        self.us4_sub = message_filters.Subscriber('/ultrasonic4', Range) # Mitä topiccia halutaan kuunnella? 
        self.us5_sub = message_filters.Subscriber('/ultrasonic5', Range) # Mitä topiccia halutaan kuunnella? 
        self.us6_sub = message_filters.Subscriber('/ultrasonic6', Range) # Mitä topiccia halutaan kuunnella? 
        self.odom_sub = message_filters.Subscriber('/robot1/odom', Odometry) # Mitä topiccia halutaan kuunnella? 
        self.subs = message_filters.ApproximateTimeSynchronizer([self.us1_sub, self.us2_sub, self.us3_sub, self.us4_sub, self.us5_sub, self.us6_sub, self.odom_sub])
