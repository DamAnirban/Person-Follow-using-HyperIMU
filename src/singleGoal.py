#!/usr/bin/env python
# license removed for brevity

import rospy
import actionlib
from geometry_msgs.msg import Vector3
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

def movebase_client():

    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = data.x
    goal.target_pose.pose.position.y = data.y
    goal.target_pose.pose.orientation.w = 1.0

    client.send_goal(goal)
    wait = client.wait_for_result()
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()

def callback(data):

    rospy.loginfo(rospy.get_caller_id() + "position x= %s", data.x)
    rospy.loginfo(rospy.get_caller_id() + "position y= %s", data.y)

if __name__ == '__main__':
    try:
	rospy.Subscriber("position", Vector3, callback)
        rospy.init_node('movebase_client_py')
        result = movebase_client()
        if result:
            rospy.loginfo("Goal execution done!")
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")

