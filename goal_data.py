#!/usr/bin/env python
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Vector3
from math import sqrt,atan2,cos,sin,pi


def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "position x= %s", data.x)
    rospy.loginfo(rospy.get_caller_id() + "position y= %s", data.y)

    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = data.x
    goal.target_pose.pose.position.y = data.y
    goal.target_pose.pose.orientation.w = 1.0
	
    client.send_goal(goal)



def pdr():

    rospy.init_node('pdr', anonymous=True)
    rospy.Subscriber("position", Vector3, callback)
    print "executed "
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    pdr()
