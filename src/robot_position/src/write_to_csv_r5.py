#! /usr/bin/python3

import rospy, random, math, message_filters
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from sensor_msgs.msg import Range
from std_srvs.srv import Empty
import angles
import csv
from tf.transformations import euler_from_quaternion

class Robot_position:

    def __init__(self):

        self.node = rospy.init_node("positions_from_lidar")
        self.reset_simulation_call = rospy.ServiceProxy("/gazebo/reset_simulation", Empty)
        self.lidar1_sub = message_filters.Subscriber('/robot5/lidar', LaserScan) # Lidar topic...
        self.odom_sub = message_filters.Subscriber('/robot5/odom', Odometry)
        self.subs = message_filters.ApproximateTimeSynchronizer([self.lidar1_sub, self.odom_sub], queue_size = 1, slop = 0.9, allow_headerless=True)
        self.subs.registerCallback(self.sensor_cb)
        self.positions_file = open('robot5_positions.csv', mode = 'w')
        self.positions_writer = csv.writer(self.positions_file, delimiter=',')
        self.reset_counter = 0
        self.write_to_csv_counter = 0

    def sensor_cb(self, lidar1_sub, odom_sub):

        self.reset_counter += 1
        self.write_to_csv_counter += 1

        lidar1_ranges = lidar1_sub.ranges
        print(lidar1_ranges)

        # Kerätään asematieto Odom-viestin Quanterion-tiedosta...
        orientation_in_quaterions = (
            odom_sub.pose.pose.orientation.x,
            odom_sub.pose.pose.orientation.y,
            odom_sub.pose.pose.orientation.z,
            odom_sub.pose.pose.orientation.w
        )

        orientation_in_euler = euler_from_quaternion(orientation_in_quaterions)

        roll = orientation_in_euler[0]
        pitch = orientation_in_euler[1]
        yaw = orientation_in_euler[2]

        yaw_radians = angles.normalize_angle_positive(yaw)
        #ground_truth_x = odom_sub.pose.pose.position.x
        ground_truth_x = odom_sub.pose.pose.orientation.x 
        #ground_truth_y = odom_sub.pose.pose.position.y
        ground_truth_y = odom_sub.pose.pose.orientation.y

        if self.write_to_csv_counter > 19:
            self.positions_writer.writerow([yaw_radians, lidar1_ranges, ground_truth_x, ground_truth_y])
            self.write_to_csv_counter = 0
        
        if self.reset_counter > 10000:
            self.reset_simulation_call()
            self.reset_counter = 0

if __name__ == '__main__':

    print("start")
    Robot_position()
    rospy.spin()


