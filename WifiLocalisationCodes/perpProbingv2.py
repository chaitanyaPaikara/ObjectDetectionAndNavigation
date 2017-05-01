#front 2
#right 1
import os
import math
import time
import numpy as np
import csv
import matplotlib.pyplot as plt
import serial

# Leap of faith
d0 = 50

flag = 0
ack = 101

#RSSI Values
P0 = 0
P1 = 0
P2 = 0

delta_x = 0
delta_y = 0
theta = 0
dist = 0
lamda = 1

dmax = 400

POWER_OFFSET = 100

ser = serial.Serial("/dev/ttyACM0", 38400)

fwd = "0 80\n"
rev = "0 -80\n"
turn90p = "90 0\n"
turn90n = "-90 0\n"
motionCmd = ""
reachedFlag = 0
 
def sendMotionCmd(data):
	global flag, ack
	while(ser.inWaiting() == 0):
		if(flag == 0): 
			time.sleep(0.5)
			ser.write(data)
			flag = 1

	data_read = ser.readline()
	   
	if(int(data_read) == ack):
		#print data_read
		flag = 0

def getRSSI():
        sum = 0
        for i in range(1, 50):
                cmd = "iwconfig wlan1 | grep -i --color quality | grep -i --color signal"

                data = os.popen(cmd).read()
	
                link_quality = ''
                signal_strength = ''	
                link_quality = data[23:25]
                signal_strength = data[43:46]

                rssi_dBm = int(signal_strength)
                quality = int(link_quality)
                rssi_dB = rssi_dBm - 30

                freq = 2437
		
                #distance = math.pow(10.0, (27.55 - (20*math.log10(freq)) + math.fabs(rssi_dBm))/20.0)

                #data_to_write =  "wlan1: RSSI = " + str(rssi_dBm) + " dBm"

                #print data_to_write

                sum = sum + rssi_dBm
		time.sleep(0.02)

        rssi_dBm = sum/50
			
	return rssi_dBm

def analyse():
	global delta_x, delta_y, theta, dist, lamda, motionCmd, dmax
	delta_y = P1 - P0
	delta_x = P2 - P0
	if(delta_x != 0 or delta_y != 0):
		lamda = (math.sqrt(2)*dmax)/(math.pow(delta_x,2) + math.pow(delta_y,2))
	else:
		lamda = 1
        #lamda = 2 - 10*(math.pow(10, (-3)*(P0+POWER_OFFSET)/(2.5*10)) - 5*math.pow(10, (-2)*(P0+POWER_OFFSET)/(2.5*10)))
	if(delta_x !=0):	
		theta = math.ceil(math.degrees((math.atan2(delta_y, delta_x))))
	elif(delta_y > 0):
		theta = 90
	elif(delta_y <0):
		theta = -90
	else:
		theta = 0
	dist = math.ceil(lamda * math.sqrt(math.pow(delta_x,2) + math.pow(delta_y,2)))

	print "Delta_y :" + str(delta_y) + "  Delta_x :" + str(delta_x) + "  lamda :" + str(lamda) + "  Theta :" + str(theta) + "  Dist :" + str(dist)

	motionCmd = str(theta) + " " + str(dist) + "\n"
	#print motionCmd

	sendMotionCmd(motionCmd)

def probe():
	global P0, P1, P2, reachedFlag, fwd, reev, turn90n, turn90p
	P0 = getRSSI()
	if(P0 < -55):
		print "Probe length : 120"
		fwd = "0 120\n"
		rev = "0 -120\n"
	elif(P0 < -48):
		print "Probe length : 100" 
                fwd = "0 100\n"
                rev = "0 -100\n"
	elif(P0 < -45):
		print "Probe length : 80" 
                fwd = "0 80\n"
                rev = "0 -80\n"
	elif(P0 < -42):
		print "Probe length : 60" 
                fwd = "0 60\n"
                rev = "0 -60\n"
	elif(P0 < -40):
		print "Probe length : 40" 
                fwd = "0 40\n"
                rev = "0 -40\n"
	elif(P0 < -37):
		print "Probe length : 20" 
                fwd = "0 30\n"
                rev = "0 -30\n"
	elif(P0 <= -35):
                print "Probe length : 20"
                fwd = "0 20\n"
                rev = "0 -20\n"
	
	
	print "P0 :" + str(P0) + " dBm   "
	if(P0 < -35):
		sendMotionCmd(fwd)
		P1 = getRSSI()
		print "P1 :" + str(P1) + " dBm   "
		if (P1 < -35):
			sendMotionCmd(rev)
			#P0 = P0 + getRSSI()
			sendMotionCmd(turn90n)
			sendMotionCmd(fwd)
			P2 = getRSSI()
			print "P2 :" + str(P2) + " dBm"
			if (P2 < -35):
				sendMotionCmd(rev)
				#P0 = P0 + getRSSI()
				#P0 = P0/3
				analyse()
			else:
				reachedFlag = 1
		                print "Pahunch gaya bc2!!"
		else:
			reachedFlag = 1
	                print "Pahunch gaya bc1!!"
        else:
		reachedFlag = 1
                print "Pahunch gaya bc0!!"
 
time.sleep(1)
while(reachedFlag ==0):
        probe()
	#sendMotionCmd(fwd)
	#sendMotionCmd(turn90p)
	

