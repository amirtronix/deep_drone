#!/home/username/parrot/bin/python

import sys
import rospy
import rospkg

import os
from loguru import logger

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
        pass



def main(args):

    flight_controller = FlightController()

    while not rospy.is_shutdown():
        pass



if __name__ == "__main__":
    main(sys.argv)
