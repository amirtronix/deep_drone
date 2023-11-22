#!/home/username/parrot/bin/python

import rospy
import tf

from geometry_msgs.msg import Pose


if __name__ == '__main__':

    rospy.init_node('broadcaster_node')

    rate = rospy.Rate(10)

    br = tf.TransformBroadcaster()

    parrot_pose = Pose()

    rospy.loginfo("Broadcasting initiated!")
    
    while not rospy.is_shutdown():

        parrot_pose.position.x = 1
        parrot_pose.position.y = 1
        parrot_pose.position.z = 1

        roll = 0
        pitch = 0
        yaw = 0


        br.sendTransform((parrot_pose.position.x, parrot_pose.position.y, parrot_pose.position.z),
                     tf.transformations.quaternion_from_euler(0, 0, yaw),
                     rospy.Time.now(),
                     "/parrot",
                     "map")
        
        
        rate.sleep()

    rospy.spin()