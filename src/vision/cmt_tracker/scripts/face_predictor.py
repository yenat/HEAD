#!/usr/bin/env python2

import rospy
import logging
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import message_filters

from cmt_tracker_msgs.msg import Trackers,Tracker,Objects
from cmt_tracker_msgs.srv import TrackerNames
from cmt_tracker_msgs.cfg import RecogntionConfig

from dynamic_reconfigure.server import Server

from openface_wrapper import face_recognizer
from image_scraper import image_scaper
from pi_face_tracker.msg import FaceEvent
class face_predictor:
    def __init__(self):
        rospy.init_node('face_recognizer', anonymous=True)
        self.image_scraper_enable = rospy.get_param('image_scraper')
        if self.image_scraper_enable != 0:
            self.user_agents = rospy.get_param('user_agents')
            self.image_scraper = image_scaper(self.user_agents)

        self.face_event_topic = rospy.get_param('publish_topic_event')
        self.openface_loc = rospy.get_param('openface')
        self.camera_topic = rospy.get_param('recognition_topic')
        self.filtered_face_locations = rospy.get_param('filtered_face_locations')
        self.shape_predictor_file = rospy.get_param("shape_predictor")
        self.image_dir = rospy.get_param("image_locations")
        self.face_recognizer = face_recognizer(self.openface_loc, self.image_dir)
        self.bridge = CvBridge()
        self.event_pub = rospy.Publisher( self.face_event_topic, FaceEvent, queue_size=10 )
        self.image_sub = message_filters.Subscriber(self.camera_topic, Image)
        self.cmt_sub = message_filters.Subscriber('tracker_results',Trackers)
        self.face_sub = message_filters.Subscriber(self.filtered_face_locations, Objects)
        self.temp_sub = message_filters.Subscriber('temporary_trackers',Trackers)
        ts = message_filters.ApproximateTimeSynchronizer([self.image_sub, self.cmt_sub,self.face_sub,self.temp_sub], 1,0.25)
        ts.registerCallback(self.callback)
        self.srv = Server(RecogntionConfig, self.sample_callback)
        self.faces_cmt_overlap = {}
        self.logger = logging.getLogger('hr.cmt_tracker.face_reinforcer_node')
        #This would hold the trackers that the system would hold.
        self.save_tracker_images = []
        #This query x results of this particular tracking instances.
        self.get_tracker_results = []

        self.service_ = rospy.Service('add_to_query', TrackerNames, self.add_to_query)
        self.cmt_state = {}
        # self.confidence = 0.85
        self.states = ['results','save']
        if not self.face_recognizer.get_state():
            print ("No Classifier")
            query_only = rospy.get_param('query_only', True)
            if query_only:
                print("Operating in Query Mode There is Model so No Queries would happen")

        self.state ={'query_save': '00', 'save_only': '01','query_only': '10', 'ignore': '11'}
        #format
        #tracker_name : {state: state in self.state or 'query_save', count: int}
        self.cmt_tracker_instances = {}

        self.overall_state = ''
        self.initial_run = True
        self.google_query = []
        #So the logic goes; if the trainer is called when save_tracker_images has saved enough images.
        #And for get_tracker_results -> returns the

    def add_to_query(self,req):
        pass

    def add_to_db(self,req):
        pass

    def callback(self,data, cmt, face,temp):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            self.logger.error(e)

        ttp = cmt
        for val in temp.tracker_results:
            ttp.tracker_results.append(val)

        not_covered_faces,covered_faces = self.returnOverlapping(face,ttp)

        for face,cmt in covered_faces:
            tupl = []
            for pts in face.feature_point.points:
                x,y = pts.x, pts.y
                tupl.append((x,y))
            key = cmt.tracker_name.data

            #TODO Can we Query state only:
            query_only = rospy.get_param('query_only', True)
            # print("Confidence: %f" % self.confidence)
            if not query_only:
                # This is to avoid adding faces sample size by saving while querying.
                self.cmt_tracker_instances[key] = self.cmt_tracker_instances.get(key,{'count': 0, 'state':self.state['query_save']})
            else:
                self.cmt_tracker_instances[key] = self.cmt_tracker_instances.get(key, {'count': 0, 'state': self.state[
                    'query_only']})
            #print(self.cmt_tracker_instances)
            if self.cmt_tracker_instances[key]['state'] == self.state['query_save']:
                self.queryAddResults(cv_image, tupl, key, self.confidence)
                print(self.face_recognizer.face_results_aggregator[cmt.tracker_name.data]['results'])


            elif not query_only and (self.cmt_tracker_instances[key]['state'] == self.state['save_only'] or self.cmt_tracker_instances[key]['state'] == self.state['query_save']):
                self.face_recognizer.save_faces(cv_image, tupl, key, str(self.cmt_tracker_instances[key]['count']))

            elif self.cmt_tracker_instances[key]['state'] == self.state['query_only']:
                self.queryAddResults(cv_image, tupl, key, self.confidence)
                print(self.face_recognizer.face_results_aggregator[cmt.tracker_name.data]['results'])
                if key not in self.google_query:
                    self.face_recognizer.temp_save_faces(cv_image, tupl, key)
                    self.google_query.append(key)
                    # print "Image Saved"

            elif self.cmt_tracker_instances[key]['state'] == self.state['ignore']:
                pass

            #Change state now;

            if self.cmt_tracker_instances[key]['count'] == self.sample_size:

                if self.cmt_tracker_instances[key]['state'] == self.state['query_save'] or self.cmt_tracker_instances[key]['state'] == self.state['query_only']:
                    max_index = max(self.face_recognizer.face_results_aggregator[cmt.tracker_name.data]['results'], key=self.face_recognizer.face_results_aggregator[cmt.tracker_name.data]['results'].get)
                    print("openface output results: ")
                    print(self.face_recognizer.face_results_aggregator[cmt.tracker_name.data]['results'])
                    if self.face_recognizer.face_results_aggregator[cmt.tracker_name.data]['results'][max_index] > self.num_positive:
                        try:
                            self.upt = rospy.ServiceProxy('recognition', TrackerNames)
                            indication = self.upt(names=str(max_index), index=int(cmt.tracker_name.data))
                            recognized_event = FaceEvent()
                            recognized_event.face_event = "recognized_face"
                            recognized_event.face_id = int(cmt.tracker_name.data)
                            recognized_event.recognized_id = str(max_index)

                            self.event_pub.publish(recognized_event)

                            if not indication:
                                self.logger.info("there was the same id in the id chamber.....")
                            self.cmt_tracker_instances[key]['state'] = self.state['ignore']
                        except rospy.ServiceException, e:
                            self.logger.error("Service call failed: %s" % e)

                    else:
                        recognized_event = FaceEvent()
                        recognized_event.face_event = "recognized_face"
                        recognized_event.face_id = int(cmt.tracker_name.data)
                        recognized_event.recognized_id = str(0)

                        self.event_pub.publish(recognized_event)
                        if not query_only:
                            self.cmt_tracker_instances[key]['state'] = self.state['save_only']
                            self.cmt_tracker_instances[key]['count'] = 0
                        else:
                            self.cmt_tracker_instances[key]['state'] = self.state['ignore']
                            self.cmt_tracker_instances[key]['count'] = 0

                    # Google Scrapper
                    if self.image_scraper_enable != 0:
                        try:
                            print "Upload Imgur and Query Google Scrapper: "
                            results = self.image_scraper.image_scraper("/tmp/" + key + ".png")
                            try:
                                self.gog = rospy.ServiceProxy('google_scraper', TrackerNames)

                                indication = self.gog(names=str(results), index=int(cmt.tracker_name.data))

                                if not indication:
                                    self.logger.info("there was the same id in the id chamber.....")
                            except rospy.ServiceException, e:
                                self.logger.error("Service call failed: %s" % e)

                            print  (results)
                            print "Finished Query of Google Images"
                        except Exception, e:
                            print e
            elif self.cmt_tracker_instances[key]['count'] == self.sample_size + self.image_sample_size:
                if self.cmt_tracker_instances[key]['state'] == self.state['save_only']:
                    self.face_recognizer.train_process(cmt.tracker_name.data)
                    #Now let's change to query state;
                    self.cmt_tracker_instances[key]['state'] = self.state['query_only']


            self.cmt_tracker_instances[key]['count'] += 1


    def sample_callback(self,config, level):
        self.cmt_tracker_instances = {}
        self.image_sample_size = config.image_number
        self.sample_size = config.sample_size
        self.confidence = config.confidence
        self.num_positive = config.num_positive
        return config

    def queryAddResults(self, cv_image, tupl, name,threshold=0.85):
        self.logger.info('getting results')
        self.face_recognizer.results(cv_image, tupl, name,threshold)
        self.logger.info('adding to tally')

    def returnOverlapping(self, face, cmt):
        not_covered_faces = []
        overlaped_faces = []
        cmt.tracker_results.sort(key=lambda tup: tup.object.object.height * tup.object.object.width)
        for j in face.objects:
            overlap = False
            SA = j.object.height * j.object.width
            if j.tool_used_for_detection.data == "opencv":
                #Skip faces which don't have dlib configuraiton. Need to integrate ci2cv and compare results
                continue
            for i in cmt.tracker_results:
                SB = i.object.object.height * i.object.object.width
                SI = max(0, ( max(j.object.x_offset + j.object.width,i.object.object.x_offset + i.object.object.width)- min(j.object.x_offset,i.object.object.x_offset) )
                         * max(0,max(j.object.y_offset,i.object.object.y_offset) - min(j.object.y_offset - j.object.height,i.object.object.y_offset - i.object.object.height)))

                SU = SA + SB - SI
                if SU != 0:
                    overlap_area = float(SI) / float(SU)
                else:
                    overlap_area = 1
                #print overlap_area
                overlap = overlap_area > 0.5
                if (overlap):
                    list = [j,i]
                    overlaped_faces.append(list)
                    break
            if not overlap:
                not_covered_faces.append(j)
        return not_covered_faces, overlaped_faces



if __name__ == '__main__':
    ic = face_predictor()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        logging.warn("Shutting down")


