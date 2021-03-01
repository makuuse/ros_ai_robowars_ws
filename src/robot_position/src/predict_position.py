#!/usr/bin/python3

import rospy, message_filters
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Range
import angles
from tf.transformations import euler_from_quaternion
import numpy as np
from tensorflow import keras

model = keras.models.load_model("./saved_model/robot1_model70epochs")

predict_data = np.zeros((1,7))
print(predict_data.shape)
test_predictions = model.predict(predict_data)
print(test_predictions)

class Robot_position:

    def __init__(self)
        self.node = rospy.init_node("robot1_position_node")

        self.us1_sub = message_filters.Subscriber('/ultrasonic1', Range)
        self.us2_sub = message_filters.Subscriber('/ultrasonic2', Range)
        self.us3_sub = message_filters.Subscriber('/ultrasonic3', Range)
        self.us4_sub = message_filters.Subscriber('/ultrasonic4', Range)
        self.us5_sub = message_filters.Subscriber('/ultrasonic5', Range)
        self.us6_sub = message_filters.Subscriber('/ultrasonic6', Range)


