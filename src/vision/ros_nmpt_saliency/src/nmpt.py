#!/usr/bin/env python
from collections import deque
import rospy
import math
import time
from std_msgs.msg import String
from blender_api_msgs.msg import Target
from ros_nmpt_saliency.msg import targets
from pi_face_tracker.msg import FaceEvent, Faces

'''
    This is a sample subscriber written to get sudden change msgs from /opencog/suddenchange topic.
 '''
class suddenChange:

  def __init__(self):
    self.GLOBAL_FLAG = 0
    self.TOPIC_FACE_TARGET = "/blender_api/set_face_target"
    self.TOPIC_FACE_EVENT = "/camera/face_event"
    self.EVENT_NEW_FACE = "new_face"
    self.EVENT_LOST_FACE = "lost_face"
    # Overrides current face being tracked by WebUI
    self.EVENT_TRACK_FACE = "track_face"

    self.audoSub = rospy.Subscriber("/nmpt_saliency_point", targets, self.GetAudioClass)
    self.look_pub = rospy.Publisher(self.TOPIC_FACE_TARGET, Target, queue_size=10)
    rospy.Subscriber(self.TOPIC_FACE_EVENT, FaceEvent, self.face_event_cb)


  # Callback function
  def GetAudioClass(self, data):
    loc = []
    loc = data.positions[0]
    degree = data.degree 
    t = Target()
    
    t.x = loc.z + 0.5
    if loc.x <= 0.5:
    	loc.x =(0.5-loc.x) *2
    else:
        loc.x =(loc.x -0.5) * -2
    t.y = loc.x
    if loc.y <= 0.5:
    	loc.y =(0.5-loc.y)*2
    else:
        loc.y =(loc.y -0.5) * -2

    t.z = loc.y

    if self.GLOBAL_FLAG and degree >=8:
        self.look_pub.publish(t)
    print(t)

  def face_event_cb(self, data):
    if data.face_event == self.EVENT_NEW_FACE:
	self.GLOBAL_FLAG = 0
    elif data.face_event == self.EVENT_LOST_FACE:
	self.GLOBAL_FLAG = 1
    elif data.face_event == self.EVENT_TRACK_FACE:
	pass



if __name__ == '__main__':
    global d

    try:
        rospy.init_node('suddenChange', anonymous=True)
        suddenChange()
        rospy.spin()
    except rospy.ROSInterruptException as e:
        print(e)
