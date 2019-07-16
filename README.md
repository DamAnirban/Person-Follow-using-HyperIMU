# Person following using HyperIMU

This is a person following or path following algorithm for a mobile robot that uses data recieved from cellphone IMU which is mounted on the foot of the user.

## Requirements
1. ROS kinetic with turtlebot (or similar) installed.
2. Cellphone with HyperIMU app from playstore.

## Setup

1. Start by selecting the packets for linear acceleration and orientation in HyperIMU
|col1|col2|col3|
|----|----|----|
|<img src="https://github.com/DamAnirban/Person-Follow-using-HyperIMU/blob/master/img/hyp2.png">|<img src="https://github.com/DamAnirban/Person-Follow-using-HyperIMU/blob/master/img/hyp3.jpg">|<img src="https://github.com/DamAnirban/Person-Follow-using-HyperIMU/blob/master/img/hyp4.png">|

2. mounting the cellphone on the foot of the user for better veloity updates from the IMU
