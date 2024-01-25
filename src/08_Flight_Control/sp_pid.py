#!/home/accurpress/parrot/bin/python

import sys
import rospy
import rospkg
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

class Gains:
    def __init__(self):
        self.kp = 0
        self.ki = 0
        self.kd = 0

class PidController:
    def __init__(self, _gains, _sample_time, _anti_windup=None):
        
        self.gains = Gains()
        self._setGains(_gains)
        self._ts = _sample_time
        self._sum = 0
        self._prev_error = 0


    def _setGains(self, _gains_list):
        self.gains.kp = _gains_list[0]
        self.gains.ki = _gains_list[1]
        self.gains.kd = _gains_list[2]

    def _antiWindup(self):
        pass

    def _cmd_sat(self):
        pass

    def _integral(self, error):
        self._sum = self._sum + error*self._ts
        return self._sum

    def _derivateive(self, error):
        derivative = (error*self._prev_error)/self._ts
        self._prev_error = error
        return derivative
    
    def compute(self, error):
        _contorlSignal = self.gains.kp*error + \
            self.gains.ki*self._integral(error) + \
            self.gains.kd*self._derivateive(error)
        
        return _contorlSignal

class FlightController():
    def __init__(self):
        rospy.init_node('flight_controller')

        self.gui_param = GuiThread()
        self.gui_param.start()

class GuiThread(threading.Thread):
    def __init__(self, title = "PID GUI", max = 100):
        super(GuiThread, self).__init__()

        self.title_window = title
        self.max = max

        self.row_titles= ["kp", "ki", "kd"]
        self.row_max = [100, 100, 100]


    def run(self):
        cv2.namedWindow(self.title_window)

        for trackbar_name, trackbar_max in zip(self.row_titles, self.row_max):
            cv2.createTrackbar(trackbar_name, self.title_window , 0, trackbar_max, self.on_trackbar)

        while not rospy.is_shutdown():
            cv2.waitKey(3)
            
    def on_trackbar(self, value):
        pass


def main(args):

    flight_controller = FlightController()
    
    rate = rospy.Rate(ROS_RATE)

    while not rospy.is_shutdown():

        t = rospy.get_time()

        rospy.loginfo("Command published!")
        rate.sleep()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main(sys.argv)
