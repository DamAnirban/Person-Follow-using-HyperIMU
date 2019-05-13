#!/usr/bin/env python
import rospy
import socket
import tf
from geometry_msgs.msg import Vector3, Quaternion
from math import sqrt,atan2,cos,sin,pi


def himu_sensor(sock):
    host="192.168.43.230"
    port=2055
    sock.bind((host,port))
    debug1 = False
    debug2 = True
    linAccArr = [0];
    orientArr = [0];
    thetaZero = 0
    flag = True
    netDist = 0.0
    pubFreq = 10
    d = 0
    netposX = 0
    netposY = 0
    totalDist = 0
    deviation = 0
    delta = 0

    linAcc_pub = rospy.Publisher('linAcc',Vector3,queue_size=50)
    orient_pub = rospy.Publisher('orient',Vector3,queue_size=50)
    position_pub = rospy.Publisher('position',Vector3,queue_size=50)
    angle_pub = rospy.Publisher('angle',Quaternion,queue_size=50)
    rospy.init_node('himu_sensor', anonymous=True)

    last_time = rospy.Time.now()
    if rospy.has_param('~host'):
        host = rospy.get_param('~host')

    rate = rospy.Rate(pubFreq)
    rospy.loginfo("waiting for device...")
	   
    while not rospy.is_shutdown():
	data,addr = sock.recvfrom(1024)
        line = data.split(',')
        if len(line) == 7:         
            linAcc_x = float(line[1])
            linAcc_y = float(line[2])
	    linAcc_z = float(line[3])
            orient_x = float(line[4]) - 180
            orient_y = float(line[5]) - 180
	    orient_z = 0
	    
	    if debug1:
		rospy.loginfo('Ax=%s Ay=%s Az=%s Ox=%s Oy=%s Oz=%s', linAcc_x, linAcc_y, linAcc_z, orient_x, orient_y, orient_z)
  	    linAcc_msg = Vector3()
            linAcc_msg.x = linAcc_x
            linAcc_msg.y = linAcc_y
            linAcc_msg.z = linAcc_z
            linAcc_pub.publish(linAcc_msg)

	    orient_msg = Vector3()
            orient_msg.x = orient_x
            orient_msg.y = orient_y
            orient_msg.z = orient_z
            orient_pub.publish(orient_msg)
#********************************************************************************************************************************
	        
	    maxLinAcc = 0
	    step_dist = 0
	    positionX = 0
	    positionY = 0
	    interval = rospy.Duration(secs=1)
	    current_time = rospy.Time.now()
	            
	    if flag and orient_x != -180:#initialising thetaZero to orient_x
		thetaZero = orient_x
		flag = False
	    
	    if ((current_time-last_time)<interval):#creating a list of acc and orient values over 1 sec 
		if(linAcc_x > 1):
			linAccArr.append(linAcc_x)
		else:
			linAccArr.append(0)

		orientArr.append(orient_x)
		print linAccArr
   	    else:
		maxLinAcc = max(linAccArr)
		
		print " Acceleration MAX =%r" %maxLinAcc
		if (maxLinAcc<12 and maxLinAcc>=4.0):
		    step_dist = step_dist+0.7 
		elif (maxLinAcc<15 and maxLinAcc>=12.0):
		    step_dist = step_dist+0.9  
		elif (maxLinAcc<25.0 and maxLinAcc>=15.0):
		    step_dist = step_dist+1.0  
		elif (maxLinAcc>=25):
		    step_dist = step_dist+1.5
		#orientation
		
		if (step_dist>0):
			newOrient = orientArr[len(orientArr)-1]
			delta = thetaZero - newOrient
			if delta>=180:
		 	   delta = delta - 360
			deviation = 90 + delta   

			#print " thetazero=%r neworient=%r delta=%r" %(delta, thetaZero, newOrient)
			q = tf.transformations.quaternion_from_euler(0.0, 0.0, abs(delta))
			angle_msg = Quaternion()
			angle_msg.x = q[0]
			angle_msg.y = q[1]
			angle_msg.z = q[2]
			angle_msg.w = q[3]
			angle_pub.publish(angle_msg)
			#print "maxlinacc=%r initOrient=%r avgOrient=%r  deviation=%r" %(maxLinAcc, initOrient, avgOrient,deviation)
		#print thetaZero		
		#print delta
		#print deviation
		print " Step dist = %r" %step_dist
		positionY = step_dist * (cos(0.01744*deviation))
		positionX = step_dist * (sin(0.01744*deviation))
		netposX += positionX
		netposY += positionY
		totalDist += step_dist
		position_msg = Vector3()
		position_msg.x = netposX
		position_msg.y = -(netposY)
		position_msg.z = 0
		position_pub.publish(position_msg)
		
		#print "step_dist =%r  posX=%r  posY=%r    " %(step_dist,positionX,positionY)
		if debug2:
		    rospy.loginfo(' Px = %s    Py = %s', position_msg.x,position_msg.y)

		last_time = current_time
		linAccArr = []
	        orientArr = []
	    
#*********************************************************************************************************************************
	    rate.sleep()

	else:
            rospy.loginfo("received incomplete UDP packet from android IMU")
	    continue

        
if __name__ == '__main__':
    try:
        sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        himu_sensor(sock)
    except rospy.ROSInterruptException:
        pass
