#!/home/username/parrot/bin/python

import rospy
from cv_bridge import CvBridge, CvBridgeError
import cv2
from sensor_msgs.msg import Image
import rospkg
import yaml
import cv2
import os

rospack = rospkg.RosPack()
config_path = rospack.get_path('deep_ros') + '/config/param.yaml'

print(config_path)

with open(config_path, 'r') as stream:
    config = yaml.safe_load(stream)

IMAGE_WIDTH = config['image_width']
IMAGE_HEIGHT = config['image_height']
ROS_RATE = config['ros_rate']
CAMERA_TOPIC = config['camera_topic']


if __name__ == "__main__":
    rospy.init_node('image_pub_node')

    image_pub = rospy.Publisher(CAMERA_TOPIC, Image, queue_size=10)
   

    rospack = rospkg.RosPack()
    workspace_dir = rospack.get_path('deep_drone')

    rate=rospy.Rate(ROS_RATE)

    bridge = CvBridge()

    frame_path = workspace_dir + "/repo/frames/"

    frame_list = os.listdir(frame_path)
    frame_list.sort()
    i = 0

    while not rospy.is_shutdown():

        img = cv2.imread(os.path.join(frame_path, "img_sphinx.jpg"))
        image_pub.publish(bridge.cv2_to_imgmsg(img, "bgr8"))
        print(img.shape)

        rate.sleep()

        
    rospy.loginfo("Node has been stopped")