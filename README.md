# Person following using HyperIMU

This is a person following or path following algorithm for a mobile robot.
1. It uses data recieved from cellphone IMU which is mounted on the foot of the user.
2. It performs pedestrian dead reckoning on it.
3. It uses the pose estimate of person as goal data for the mobile robot.

## Requirements
1. ROS kinetic with turtlebot (or similar) installed.
2. Cellphone with HyperIMU app from playstore.

## Setup

1. Start by selecting the packets for linear acceleration and orientation in HyperIMU, with timestamp.

| App | Orientation | Linear Acceleration |
| ---- | ---- | ---- |
| <img src="https://github.com/DamAnirban/Person-Follow-using-HyperIMU/blob/master/img/hyp2.png"> | <img src="https://github.com/DamAnirban/Person-Follow-using-HyperIMU/blob/master/img/hyp3.jpg"> | <img src="https://github.com/DamAnirban/Person-Follow-using-HyperIMU/blob/master/img/hyp4.png"> |

2. Set host and port of robot.
3. Mount the cellphone on the foot of the user for better veloity updates from the IMU.
4. Run himu_sensor.py and goal_data.py
5. Start turtlebot or similar (simulation also works for visualisation).
6. Move around and see the robot follow the path taken by you.
