#!/home/username/parrot/bin/python

import os
import sys
import rospy
from geometry_msgs.msg import Twist
import time

import olympe
from olympe.messages.ardrone3.Piloting import TakeOff, Landing, PCMD


DRONE_IP = os.environ.get("DRONE_IP", "10.202.0.1")
DRONE_RTSP_PORT = os.environ.get("DRONE_RTSP_PORT")


class OlympeBridge():

    def __init__(self):
        rospy.init_node('olympe_bridge_node', anonymous=False)
        rospy.Subscriber('/drone/cmd_vel', Twist, self.cmd_vel_callback)

        self.rate = rospy.Rate(10)

        self.drone = olympe.Drone(DRONE_IP)
        self.drone.connect()

        assert self.drone(TakeOff()).wait().success()

        self.cmd_vel = Twist()
        self.control = False

        # rospy.spin()

    def cmd_vel_callback(self, msg):
        self.cmd_vel.linear.x, self.cmd_vel.linear.y, self.cmd_vel.linear.z = [msg.linear.x, msg.linear.y, msg.linear.z]
        self.cmd_vel.angular.x, self.cmd_vel.angular.y, self.cmd_vel.angular.z = [msg.angular.x, msg.angular.y, msg.angular.z]

    def run(self):
        self.drone(
            PCMD(
                1,
                int(self.cmd_vel.linear.x),
                int(self.cmd_vel.linear.y),
                int(-self.cmd_vel.angular.z),
                int(self.cmd_vel.linear.z),
                timestampAndSeqNum=0,
            )
        )
        self.control  = False

        print("x_cmd = ", int(self.cmd_vel.linear.x), end = ' ')
        print("y_cmd = ", int(self.cmd_vel.linear.y), end = ' ')
        print("z_cmd = ", int(self.cmd_vel.linear.z), end = ' ')
        print("Yaw_cmd = ", -int(self.cmd_vel.angular.z))

        time.sleep(0.05)



def main(args):
    olympe_bridge = OlympeBridge()

    while not rospy.is_shutdown():

        olympe_bridge.run()
        olympe_bridge.rate.sleep()

    assert olympe_bridge.drone(Landing()).wait().success()
    olympe_bridge.drone.disconnect()

    print("Shutting down")


if __name__ == "__main__":
    main(sys.argv)

