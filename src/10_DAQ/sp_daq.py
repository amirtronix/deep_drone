#!/home/accurpress/parrot/bin/python

import sys
import rospy
import rospkg
from geometry_msgs.msg import Pose, Twist
import tf

import threading
import cv2
import os
from loguru import logger
import yaml

rospack = rospkg.RosPack()
config_path = rospack.get_path('deep_drone') + '/config/param.yaml'

print(config_path)

with open(config_path, 'r') as stream:
    config = yaml.safe_load(stream)

ROS_RATE = config['ros_rate']

class DataAcquisition():
    def __init__(self):
        pass


def main(args):

    data_acquisition = DataAcquisition()
    rate = rospy.Rate(ROS_RATE)

    while not rospy.is_shutdown():
        rate.sleep()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main(sys.argv)
