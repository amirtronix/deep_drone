#!/home/legatus/parrot/bin/python

import rospy
import olympe
from olympe.messages.ardrone3.Piloting import TakeOff, Landing
from std_msgs.msg import String

import os
import time

DRONE_IP = os.environ.get("DRONE_IP", "10.202.0.1")

def takeoff():
    pub = rospy.Publisher('/parrot/status', String, queue_size=10)
    rospy.init_node('takeoff_node', anonymous=True)
    drone = olympe.Drone(DRONE_IP)
    drone.connect()

    assert drone(TakeOff()).wait().success()
    takeoff_str = "Takeoff successful %s" % rospy.get_time()
    rospy.loginfo(takeoff_str)
    pub.publish(takeoff_str)

    time.sleep(10)
    assert drone(Landing()).wait().success()
    landing_str = "Landing successful %s" % rospy.get_time()
    rospy.loginfo(landing_str)
    pub.publish(landing_str)


    drone.disconnect()


if __name__ == '__main__':
    try:
        takeoff()
    except rospy.ROSInterruptException:
        pass