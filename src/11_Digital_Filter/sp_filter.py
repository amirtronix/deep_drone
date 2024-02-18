#!/home/username/parrot/bin/python

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
import random

rospack = rospkg.RosPack()
config_path = rospack.get_path('deep_drone') + '/config/param.yaml'

print(config_path)

with open(config_path, 'r') as stream:
    config = yaml.safe_load(stream)

ROS_RATE = config['ros_rate']

class Gains:
    def __init__(self):
        self.kp = 0
        self.ki = 0
        self.kd = 0

class Filter:
    def __init__(self, _filter_order, _num_list: list,_denom_list: list):
        
        self.n = _filter_order
        self._a = _num_list
        self._b = _denom_list

        self.x = []
        self.y = []

        for i in range(self.n+1):
            self.x.append(0.0)
            self.y.append(0.0)


    def filter(self, sample):
        self.x = self._shift_array(sample, self.x)
        self.y = self._shift_array(0.0, self.y)

        sum = 0.0

        for i in range(1, self.n+1):
            sum += self._b[i]*self.x[i] - self._a[i]*self.y[i]

        sum += self._b[0]*self.x[0]

        self.y[0] = sum
        return self.y[0]

    def _shift_array(self, val, list):
        return [val] + list[:-1]




def main(args):

    rospy.init_node('signal_processing')

    vel_pub = rospy.Publisher("/drone/vel",Twist, queue_size=10)
    vel_filt_pub = rospy.Publisher("/drone/vel_filt",Twist, queue_size=10)

    vel = Twist()
    vel_filt = Twist()

    dt = 1/ROS_RATE


    listener = tf.TransformListener()

    b_x = [0.0055,    0.0111,    0.0055]
    a_x = [1.0000,   -1.7786,    0.8008]

    pos_x = 1.0


    filter_x = Filter(2, a_x, b_x)

    rate = rospy.Rate(ROS_RATE)

    while not rospy.is_shutdown():
        try:
            (trans,rot) = listener.lookupTransform('map', '/vicon/parrot/parrot', rospy.Time(0))
            t = rospy.get_time()

            vel.linear.x = (trans[0] - pos_x)/dt + random.random()*0.05
            pos_x = trans[0] 

            vel_filt.linear.x = filter_x.filter(vel.linear.x)

            vel_pub.publish(vel)
            vel_filt_pub.publish(vel_filt)
            print(vel_filt.linear.x)

            rospy.loginfo("Command published!")
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            # rospy.logerr("No transform found!")
            continue



        rate.sleep()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main(sys.argv)
