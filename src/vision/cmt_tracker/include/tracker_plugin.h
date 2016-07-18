#ifndef TRACKER_PLUGIN_H
#define TRACKER_PLUGIN_H
#include <QStandardItem>
#include <QWidget>
#include <rqt_gui_cpp/plugin.h>
#include <ros/macros.h>

#include <opencv2/core/core.hpp>
#include <opencv2/objdetect/objdetect.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>

#include <image_transport/image_transport.h>
#include <sensor_msgs/Image.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.h>
#include <QDebug>
#include <QList>
#include <QImage>
#include <QPixmap>

#include <pluginlib/class_list_macros.h>
#include <ros/master.h>
#include <ros/ros.h>
#include <ros/console.h>

#include <iostream>
#include <sstream>

#include <cmt_tracker_msgs/Object.h>
#include <cmt_tracker_msgs/Objects.h>
#include <cmt_tracker_msgs/Tracker.h>
#include <cmt_tracker_msgs/Trackers.h>
#include <cmt_tracker_msgs/Clear.h>
#include <cmt_tracker_msgs/Update.h>

#include <cmt_tracker_msgs/TrackedImages.h>
#include <cmt_tracker_msgs/TrackerNames.h>

#include <cmt_tracker_msgs/TrackerConfig.h>
#include <dynamic_reconfigure/server.h>

#include <dynamic_reconfigure/DoubleParameter.h>
#include <dynamic_reconfigure/Reconfigure.h>
#include <dynamic_reconfigure/Config.h>

#include <vector>
//The Ui Element Definition
#include "ui_tracker_plugin.h"



namespace rqt_tracker_view {
class tracker_plugin
    : public rqt_gui_cpp::Plugin
{
    Q_OBJECT

public:
    //To hold last value of face_locs;
    cmt_tracker_msgs::Objects face_locs;
    cmt_tracker_msgs::Tracker track_location;
    cmt_tracker_msgs::Tracker track_published;
    cmt_tracker_msgs::Trackers tracking_results;
    cmt_tracker_msgs::Trackers temp_tracking_results;

    ros::Publisher tracker_locations_pub;
    ros::Subscriber tracker_locations_sub;
    ros::Subscriber face_subscriber;
    ros::Subscriber tracked_locations;
    ros::Subscriber temp_tracked_locations;
    ros::ServiceClient client;
    ros::ServiceClient image_client;
    ros::ServiceClient check_update;
    image_transport::Subscriber image_subscriber;


    ros::NodeHandle nh;
    image_transport::ImageTransport it;

    tracker_plugin();


    virtual void initPlugin(qt_gui_cpp::PluginContext& context);

    virtual void shutdownPlugin();
    

signals:
    void updatefacelist();
protected slots:

    void on_MethodChanged(int index);

    void on_ParamChanged(int index);

    void on_addItems_clicked();

    void updateVisibleFaces();

    void on_addToTrack_clicked(QListWidgetItem * item);

    void on_removeAllTracked_clicked();

    void on_removeTracked_clicked();

    void on_updateTracked();

    void on_removeAllElements_clicked();

    void list_of_faces_update(const cmt_tracker_msgs::Objects& faces_info);

    void imageCb(const sensor_msgs::ImageConstPtr& msg);

    void trackerCb(const cmt_tracker_msgs::Tracker& tracker_locs);

    void tracker_resultsCb(const cmt_tracker_msgs::Trackers& tracker_results); 

    void temp_tracker_resultsCb(const cmt_tracker_msgs::Trackers& tracker_results);

    bool updateTrackerNames(cmt_tracker_msgs::TrackerNames::Request &req, cmt_tracker_msgs::TrackerNames::Response &res);
protected:
    ros::ServiceServer viewupdate_service;
    std::vector<QImage> face_images;
    std::vector<QImage> tracked_faces;

    std::vector<QImage> tracked_image_results;
    std::vector<QImage> temp_tracked_image_results;

    std::vector<std::string> faces_image_information;
    std::vector<std::string> tracked_image_information;
    std::vector<std::string> temp_tracked_image_information;

    std::vector<std::string> emotion;

    std::vector<cv::Mat> tracked_image_mats;
    std::vector<cv::Mat> temp_tracked_image_mats;

    std::vector<cv::Mat> mat_images;
    std::vector<cv::Mat> tracked_images;

    bool disable;
    std::string subscribe_topic;
    cv::Mat conversion_mat_;
    cv::Mat img;

    Ui::tracker_plugin ui;
    QWidget* widget_;
    
    std::vector<std::string> tracked_images_names; 
    int tracker_updated_num; 
    std::string tracking_method;
    std::string subscribe_face;
    bool firstrun; 


};
}
#endif // TRACKER_PLUGIN_H
