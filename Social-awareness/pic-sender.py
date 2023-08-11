#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

def sender_node():
    rospy.init_node('image_sender', anonymous=True)
    image_pub = rospy.Publisher('image_topic', Image, queue_size=10)
    rate = rospy.Rate(1)  # 10 Hz

    bridge = CvBridge()

    while not rospy.is_shutdown():
        print("I'm publishing")
        image = cv2.imread('Social-awareness/images/face-test.png') 
        if image is not None:
            img_msg = bridge.cv2_to_imgmsg(image, encoding="bgr8")
            image_pub.publish(img_msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        sender_node()
    except rospy.ROSInterruptException:
        pass
