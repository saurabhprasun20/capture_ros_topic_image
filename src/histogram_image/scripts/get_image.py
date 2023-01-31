#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from datetime import datetime

def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)

def callback(data):
    current_datetime = datetime.now()
    str_current_datetime = str(current_datetime)
    bridge = CvBridge()
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data)
    rospy.loginfo(type(data.data))
    cv_image = bridge.imgmsg_to_cv2(data)
    rospy.loginfo(type(cv_image))
    # ims = cv2.resize(cv_image,(960,540))
    ims = ResizeWithAspectRatio(cv_image,width=1200)
    cv2.imwrite("/home/prasun/histogram_image/hist_image_"+str_current_datetime+".png",ims)
    # with open("./msg.txt") as f:
    #     f.write(data.data)

    
def listener():
    rospy.init_node('histogram_image_listener', anonymous=True)

    rospy.Subscriber("/histogram_image", Image, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()