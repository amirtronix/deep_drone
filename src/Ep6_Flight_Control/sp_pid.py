#!/home/username/parrot/bin/python

import sys
import rospy
import rospkg

import os
from loguru import logger


class FlightController():
    def __init__(self):
        pass



def main(args):

    flight_controller = FlightController()

    while not rospy.is_shutdown():
        pass



if __name__ == "__main__":
    main(sys.argv)
