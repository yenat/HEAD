#ifndef FACE_LOCATOR_H
#define FACE_LOCATOR_H
#include <ros/ros.h>

#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.h>
#include <tf/transform_broadcaster.h>
#include <tf/transform_datatypes.h>
#include <image_geometry/pinhole_camera_model.h>

#include <opencv2/objdetect/objdetect.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/calib3d/calib3d.hpp>
//CMT_TRACKER name structure;
#include <cmt_tracker_msgs/Object.h>
#include <cmt_tracker_msgs/Objects.h>
#include <cmt_tracker_msgs/Trackers.h>
#include <cmt_tracker_msgs/FaceConfig.h>

#include <dynamic_reconfigure/server.h>

#include <geometry_msgs/Point.h>
#include <std_msgs/Bool.h>
#include <std_msgs/String.h>

#include <opencv_apps/Point2DArray.h>
#include <opencv_apps/Point2D.h>

#include <dlib/image_processing/frontal_face_detector.h>
#include <dlib/image_processing/render_face_detections.h>
#include <dlib/image_processing.h>
#include <dlib/gui_widgets.h>
#include <dlib/image_io.h>
#include <dlib/opencv.h>
#include <boost/thread.hpp>
#include <iostream>
#include <sstream>

//Include Gaze Now from the gazr;
#include "pupils.hpp"

#define SSTR( x ) dynamic_cast< std::ostringstream & >(( std::ostringstream() << std::dec << x ) ).str()

namespace face_detect {
struct merged_message{
   cmt_tracker_msgs::Objects message;
   std::vector<int> overlapedDlibCV;
};
// Anthropometric for male adult
// Relative position of various facial feature relative to sellion
// Values taken from https://en.wikipedia.org/wiki/Human_head
// X points forward
const static cv::Point3f P3D_SELLION(0., 0.,0.);
const static cv::Point3f P3D_RIGHT_EYE(-20., -65.5,-5.);
const static cv::Point3f P3D_LEFT_EYE(-20., 65.5,-5.);
const static cv::Point3f P3D_RIGHT_EAR(-100., -77.5,-6.);
const static cv::Point3f P3D_LEFT_EAR(-100., 77.5,-6.);
const static cv::Point3f P3D_NOSE(21.0, 0., -48.0);
const static cv::Point3f P3D_STOMMION(10.0, 0., -75.0);
const static cv::Point3f P3D_MENTON(0., 0.,-133.0);


// Interesting facial features with their landmark index
enum FACIAL_FEATURE {
    NOSE=30,
    RIGHT_EYE=36,
    LEFT_EYE=45,
    RIGHT_SIDE=0,
    LEFT_SIDE=16,
    EYEBROW_RIGHT=21,
    EYEBROW_LEFT=22,
    MOUTH_UP=51,
    MOUTH_DOWN=57,
    MOUTH_RIGHT=48,
    MOUTH_LEFT=54,
    SELLION=27,
    MOUTH_CENTER_TOP=62,
    MOUTH_CENTER_BOTTOM=66,
    MENTON=8
};

typedef cv::Matx44d head_pose;


class Face_Detection {

public:
  Face_Detection();
  //~Face_Detection();

  void imageCb(const sensor_msgs::ImageConstPtr& msg, const sensor_msgs::CameraInfoConstPtr& camerainfo);
  void callback(cmt_tracker_msgs::FaceConfig &config, uint32_t level);
  //The dlib is the one that has the authority to create a face while for the reinforcement process one can use both the elements to create the better rules.
  void dlib_detector(cv::Mat dlib_image);
  void opencv_detector(cv::Mat ocv_image);
private:

  dynamic_reconfigure::Server<cmt_tracker_msgs::FaceConfig> server;
  dynamic_reconfigure::Server<cmt_tracker_msgs::FaceConfig>::CallbackType f;

  std::vector<cv::Rect> dlib_faces;
  std::vector<cv::Rect> opencv_faces;

  image_geometry::PinholeCameraModel cameramodel;
  cv::Mat cameraMatrix, distCoeffs;

  int scale_factor;

  cv::Mat conversion_mat_;
  int counter;
  geometry_msgs::Point face_points;
  int center;
  cv::CascadeClassifier face_cascade;
  cv::CascadeClassifier eyes_cascade;
  std::string cascade_file_face;
  std::string cascade_file_eyes;
  dlib::pyramid_down<2> pyd;
  dlib::frontal_face_detector detector;

//  dlib::image_window win;

  dlib::shape_predictor sp;
  std::string shape_predictor_dat;
  ros::NodeHandle nh_;
  image_transport::ImageTransport it_;
//  image_transport::Subscriber image_sub_;
  image_transport::CameraSubscriber image_sub_;
  image_transport::Publisher image_pub_;

  //List of face values in space.
  ros::Publisher faces_locations;
  std::vector<cv::Rect> faces;
  std::vector<cv::Rect> eyes;
  cmt_tracker_msgs::Objects cmt_face_locations;
  cmt_tracker_msgs::Objects cv_face_locations;
  std::string subscribe_topic;
  std::string publish_topic;
  int time_sec;
  std_msgs::String tracking_method;
  std::string face_detection_method;
  bool setup;
  cv::Mat _debug;

  head_pose facepose(cmt_tracker_msgs::Object face_description);

  cv::Point2f coordsOf(size_t face_idx, FACIAL_FEATURE feature) const;

    /** Returns true if the lines intersect (and set r to the intersection
     *  coordinates), false otherwise.
     */
  bool intersection(cv::Point2f o1, cv::Point2f p1,
                      cv::Point2f o2, cv::Point2f p2,
                      cv::Point2f &r) const;

  Pupils pupils_detector;


  float focalLength;
  float opticalCenterX;
  float opticalCenterY;



};
//static class that may be called by implementing class. 
namespace {
  std::vector<cv::Rect> facedetect(cv::Mat frame_gray);
  cmt_tracker_msgs::Objects convert(std::vector<cv::Rect> faces, std::string tool_used);
  merged_message returnNoneOverlappingCV(std::vector<cv::Rect> dlib_locations, std::vector<cv::Rect> opencv_locs);
}
}
#endif // FACE_LOCATOR_H