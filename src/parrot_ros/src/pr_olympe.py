#!/home/legatus/parrot/bin/python

import rospy
import olympe
import os
from olympe.messages.ardrone3.Piloting import TakeOff, Landing, PCMD

from geometry_msgs.msg import Twist

DRONE_IP = os.environ.get("DRONE_IP", "10.202.0.1")

class OlympeBridge():
    def __init__(self):
        rospy.init_node("olympe_bridge_node", anonymous=False)
        rospy.Subscriber("/parrot/cmd_vel", Twist, self.cmd_vel_callback)

        self.cmd_vel = Twist()

        self.drone = olympe.Drone(DRONE_IP)
        self.drone.connect()

        self.rate = rospy.Rate(10)

        assert self.drone(TakeOff()).wait().success()
        takeoff_str = "Takeoff successful %s" % rospy.get_time()
        rospy.loginfo(takeoff_str)
    
    def cmd_vel_callback(self, msg: Twist):
        self.cmd_vel.linear.x = msg.linear.x
        self.cmd_vel.linear.y = msg.linear.y
        self.cmd_vel.linear.z = msg.linear.z

        self.cmd_vel.angular.z = msg.angular.z


        print("cmd_vel received")
        print("cmd_vel.z: ", self.cmd_vel.linear.z)

    
    def run(self):
        self.drone(PCMD(
            1,
            int(self.cmd_vel.linear.x),
            int(self.cmd_vel.linear.y),
            int(self.cmd_vel.angular.z),
            int(self.cmd_vel.linear.z),
            timestampAndSeqNum = 0,
        )
        )

        print("cmd_vel sent as PCMD")
        print("x: ", int(self.cmd_vel.linear.x),
              "y: ", int(self.cmd_vel.linear.x),
              "z: ", int(self.cmd_vel.linear.x),
              "psi: ", int(self.cmd_vel.angular.x))


def main():
    olympe_bridge = OlympeBridge()

    while not rospy.is_shutdown():
        olympe_bridge.run()
        olympe_bridge.rate.sleep()

    assert olympe_bridge.drone(Landing()).wait().success()
    landing_str = "Landing successful %s" % rospy.get_time()
    rospy.loginfo(landing_str)

    print("Shutting down")

if __name__ == '__main__':
    main()