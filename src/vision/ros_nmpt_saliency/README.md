### Visual Saliency Detection using NMPT
------------

###Introduction
This package listens to `/cv_camera/image_raw` topic and analyzes the video for saliency. It gives a point output `0..1` for x, `0..1` for y, and the degree of salient point ranging from `1..10`. The messages are pulblished to the topic  `/nmpt_saliency_point`. </br>

1. Package Name: `ros_nmpt_saliency`
2. Node Name:    `ros_nmpt_saliency_node`
3. Topics:       `/nmpt_saliency_point`
4. MessageFiles: `targets.msg` </br>
   4.1 Type 1: `geometry_msgs/Point[] positions` </br>
   4.2 Type 2: `float32 degree` 

###How it works
####Salient Point Detector
TBW
####Degree

The degree calculator accepts three coordinates (x,y, and z) as coordinates of salient point. Given N second turnaround time it calculates the rate of change of a specific salient point. The mimumum possible interval of change for a given salient point (t) is used to normalize degrees of salient points overtime. i.e the maximum interval before change <-> the  minmum increment of the degree of salient point. Furthermore, the degree of each salient point is normalized in range 1 to 10.

###Get the Repo

[HEAD](https://github.com/hansonrobotics/HEAD/blob/master/README.md) </br>

###Running

`cd hansonrobotics && ./scripts/dev.sh` </br>

###Halt the Execution
`cd hansonrobotics && ./scripts/stop.sh` </br>

###Subscription to the Topic
1. Check `sample_nmpt_subscriber` node as a reference. </br> 

###Troubleshooting

  TBW

###FAQ

  TBW
</br>

###Auto-Test
  TBW
###Reference
----------------
 TBW

