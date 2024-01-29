#!/home/accurpress/parrot/bin/python

import sys
import rospy
import rospkg
from geometry_msgs.msg import Pose, Twist

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

        rospy.Subscriber('/drone/cmd_pos', Pose, self._cmd_pos_callback)
        self.cmd_pub = rospy.Publisher("/drone/cmd_vel",Twist, queue_size=10)

        self.sample_time = 1/ROS_RATE

        self.gui_param = GuiThread()
        self.gui_param.start()

        self.cmd_zero = Twist()
        self.cmd_vel = Twist()
        self.cmd_pos = Pose()

        self.gains = [[0,0,0], [0,0,0], [0,0,0], [0,0,0]]

        self.pid_x = PidController(self.gains[0], self.sample_time)
        self.pid_y = PidController(self.gains[1], self.sample_time)
        self.pid_z = PidController(self.gains[2], self.sample_time)
        self.pid_yaw = PidController(self.gains[3], self.sample_time)

    def generate_cmd(self):
        if self._is_topic("/drone/cmd_pos"):
            errors = self._get_error(1, 2)

            self.cmd_vel.linear.x = self.pid_x.compute(errors[0])
            self.cmd_vel.linear.y = self.pid_x.compute(errors[1])
            self.cmd_vel.linear.z = self.pid_x.compute(errors[2])
            self.cmd_vel.angular.z = self.pid_x.compute(errors[3])

            self.cmd_pub.publish()

        else:
            self.cmd_pub.publish(self.cmd_zero)

    def _cmd_pos_callback(self, msg: Pose):
        self.cmd_pos.position = msg.position
        self.cmd_pos.orientation = msg.orientation

    def _get_error(self, setpoint, pose):
        #TODO Adding /tf listener
        return [5, 5, 5, 5]

    def _is_topic(slef, topic_name):
        # Get the list of published topics
        topics = rospy.get_published_topics()

        # Check if the specified topic exists in the list
        for topic, topic_type in topics:
            if topic == topic_name:
                return True

        return False

class GuiThread(threading.Thread):
    def __init__(self, title = "PID GUI", max = 100):
        super(GuiThread, self).__init__()

        self.title_window = title
        self.max = max

        self.row_titles= ["kp (x)  ", "ki (x)  ", "kd (x)  ",
                          "kp (y)  ", "ki (y)  ", "kd (y)  ",
                          "kp (z)  ", "ki (z)  ", "kd (z)  ",
                          "kp (yaw)", "ki (yaw)", "kd (yaw)"]
        1
        self.row_max = [100, 100, 100,
                        100, 100, 100,
                        100, 100, 100,
                        100, 100, 100]


    def update_gains(self):
        #TODO Update PID gains
        pass

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
        flight_controller.generate_cmd()

        rospy.loginfo("Command published!")
        rate.sleep()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main(sys.argv)
