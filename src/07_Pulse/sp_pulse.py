#!/home/accurpress/parrot/bin/python

import sys
import rospy
import rospkg
from geometry_msgs.msg import Pose

import os
from loguru import logger

class PulseGenerator:
    def __init__(self, pulse_width, amplitude, offset = 0):
        
        self._pulse_width = pulse_width
        self._amplitude = amplitude
        self._offset = offset


    def _even_odd(self, num):
        
        if(int(num)%2 == 0):
            return 1.0
        
        else:
            return -1.0
    

    def generate(self, time):
        
        signal = self._even_odd(time/self._pulse_width)*self._amplitude + self._offset
        return signal


class PulseNode():
    def __init__(self):
        rospy.init_node('pulse_generator')

        self.pulse_mode = rospy.get_param("~pulse_mode")
        self.axis = rospy.get_param("~axis")
        self.pulse_amp = rospy.get_param("~pulse_amp")
        self.pulse_width = rospy.get_param("~pulse_width")

        print(self.pulse_width)



def main(args):

    pulse_node = PulseNode()

    while not rospy.is_shutdown():
        pass



if __name__ == "__main__":
    main(sys.argv)
