cmake_minimum_required(VERSION 2.8.3)
project(person_follow)

find_package(catkin REQUIRED COMPONENTS
  rospy
  geometry_msgs
  move_base_msgs
  tf
)

catkin_package()

catkin_install_python(PROGRAMS
  src/himu_sensor.py
  src/goal_data.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
