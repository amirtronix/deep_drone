#!/home/legatus/parrot/bin/python

import sys
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from loguru import logger
import os
import olympe
from olympe.messages.ardrone3.Piloting import TakeOff, Landing, PCMD

DRONE_IP = os.environ.get("DRONE_IP", "10.202.0.1")

class OlympeBridge():
    def __init__(self):
        rospy.init_node('olympe_node', anonymous=False)
        self.cmd_sub = rospy.Subscriber("/parrot/status_cmd", String, self.cmd_callback)
        self.cmd_vel_sub = rospy.Subscriber("/parrot/cmd_vel", Twist, self.cmd_vel_callback)
        self.isDroneConnected = False
        self.cmd_vel = Twist()

        self.rate = rospy.Rate(10)
        
        self.drone = olympe.Drone(DRONE_IP)
        self.drone.connect()

        if self.drone.connection_state():
            self.isDroneConnected = True
            logger.success("Drone is connected and ready to takeoff!")
        else:
            logger.error("Drone disconnected!")
            self.isDroneConnected = False
            exit(0)

        
    def cmd_vel_callback(self, msg: Twist):
        self.cmd_vel.linear.x = msg.linear.x
        self.cmd_vel.linear.y = msg.linear.y
        self.cmd_vel.linear.z = msg.linear.z

        self.cmd_vel.angular.x = msg.angular.x

        print("cmd_vel received")
        self.run()


    def cmd_callback(self, msg: String):
        logger.info(msg.data)

        if msg.data == "takeoff" or msg.data == "Takeoff" and self.isDroneConnected:
            assert self.drone(TakeOff()).wait().success()

        if msg.data == "land" or msg.data == "Land" and self.isDroneConnected:
            assert self.drone(Landing()).wait().success()


    def run(self):
        self.drone(PCMD(
            1,
            int(self.cmd_vel.linear.y),
            int(self.cmd_vel.linear.x),
            int(self.cmd_vel.angular.z),
            int(self.cmd_vel.linear.z),
            timestampAndSeqNum = 0
        ))

        logger.info("PCMD \nx: {}\ny: {}\nz: {}\nyaw: {}".format(self.cmd_vel.linear.x,
                                                                 self.cmd_vel.linear.y,
                                                                 self.cmd_vel.linear.z,
                                                                 self.cmd_vel.angular.z))

    def __del__(self):
        self.drone.disconnect()
        self.isDroneConnected = False


def main(args):
    olympe_bridge = OlympeBridge()
    rospy.spin()


if __name__ == "__main__":
    main(sys.argv)