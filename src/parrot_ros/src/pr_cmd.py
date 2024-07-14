#!/home/legatus/parrot/bin/python

import sys

import rospy
from std_msgs.msg import String

from loguru import logger

class Cmd():
    def __init__(self):
        rospy.init_node('cmd_node', anonymous=False)
        self.cmd_pub = rospy.Publisher('/parrot/status_cmd', String, queue_size=10)

        self.cmd_msg = String()

        self.cmd_list = ["takeoff", "land"]


    def user_prompt(self):
        logger.info("Enter flight command [takeoff] or [land]")
        input_msg = input()

        if input_msg == "exit":
            exit(0)
        
        elif not input_msg in str(self.cmd_list):
            logger.error("Invalid input, try again!")
            self.user_prompt()
            


        else:
            self.publish(input_msg)


    def publish(self, input_msg):
        self.cmd_msg = input_msg
        self.cmd_pub.publish(self.cmd_msg)
        logger.success("{} command published".format(self.cmd_msg))

def main(args):
    cmd_node = Cmd()

    while not rospy.is_shutdown():
        cmd_node.user_prompt()



if __name__ == "__main__":
    main(sys.argv)
