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

POWER_OFFSET = 90

#RSSI Values
P0 = 0
P1 = 0
P2 = 0

delta_x = 0
delta_y = 0
theta = 0
dist = 0
lamda = 1
dmax = 250
reachedFlag = 0


ser = serial.Serial("/dev/ttyACM0", 38400)

fwd = "0 50\n"
rev = "0 -50\n"
turn90p = "90 0\n"
turn90n = "-90 0\n"
motionCmd = ""
 
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

		#data_to_write =  "wlan0: RSSI = " + str(rssi_dBm) + " dBm"

		#print data_to_write

		sum = sum + rssi_dBm
		time.sleep(0.01)

	rssi_dBm = sum/50
			
	return rssi_dBm

def analyse():
	global delta_x, delta_y, theta, dist, lamda, motionCmd, dmax
	delta_y = P1 - P0
	delta_x = P2 - P0

	#lamda = 10 -15*(math.pow(10, (-3)*(P0+POWER_OFFSET)/(2.5*10)) - 5*math.pow(10, (-2)*(P0+POWER_OFFSET)/(2.5*10)))
	lamda = dmax/(math.pow(delta_x,2), math.pow(delta_y,2))
	
	if(delta_x != 0):
		theta = math.ceil(math.degrees((math.atan2(delta_y, delta_x))))
	else:
		theta = 90
	dist = math.ceil(lamda * math.sqrt(math.pow(delta_x,2), math.pow(delta_y,2)))

	print "Delta_y :" + str(delta_y) + "Delta_x :" + str(delta_x) + "lamda :" + str(lamda) + "Theta :" + str(theta) + "Dist :" + str(dist)

	motionCmd = str(theta) + " " + str(dist) + "\n"
	#print motionCmd

	sendMotionCmd(motionCmd)

def perpProbe():
	global P0, P1, P2
	P0 = getRSSI()
	if(P0 < -40):
		sendMotionCmd(fwd)
		P1 = getRSSI()
		sendMotionCmd(rev)
		sendMotionCmd(turn90p)
		sendMotionCmd(fwd)
		P2 = getRSSI()
		sendMotionCmd(rev) + "dBm  "
		print "P0 :" + str(P0) + " dBm  " + "P1 :" + str(P1) + " dBm  " + "P0 :" + str(P2)  + " dBm"
		analyse()
 

def NSEWProbe():
	P = getRSSI()
	print "P: " + str(P) + " dBm "
	sendMotionCmd("0 80\n")
	PN = getRSSI()
	print "PN: " + str(PN) + " dBm "
	sendMotionCmd("0 -80\n")
	P = P + getRSSI()
	sendMotionCmd("0 -80\n")
	PS = getRSSI()
	print "PS: " + str(PS) + " dBm "
	sendMotionCmd("0 80\n")
	P = P + getRSSI()
	sendMotionCmd("90 0\n")
	sendMotionCmd("0 80\n")
	PE = getRSSI()
	print "PE: " + str(PE) + " dBm "
	sendMotionCmd("0 -80\n")
	P = P + getRSSI()
	sendMotionCmd("0 -80\n")
	PW = getRSSI()
	print "PW: " + str(PW) + " dBm "
	sendMotionCmd("0 80\n")
	P = P + getRSSI()
	sendMotionCmd("-90 0\n")
	P0 = int(P/5)
	print "P0: " + str(P0) + " dBm "

	deltaN = PN - P0
	deltaS = PS - P0
	deltaE = PE - P0
	deltaW = PW - P0

	deltaMax = max(deltaN, deltaS, deltaE, deltaW)
	
	print "deltaMax: " + str(deltaMax)
	#print "P0: " + str(P0) + " dBm " + "PN: " + str(PN) + "  " + "PS: " + str(PS) + "  " + "PE: " + str(PE) + "  " + "PW: " + str(PW) + "  " + "deltaMax :" + str(deltaMax)
	

	if(deltaMax == deltaN):
		pass
	elif(deltaMax == deltaE):
		sendMotionCmd("90 0\n")
	elif(deltaMax == deltaS):
		sendMotionCmd("180 0\n")
	elif(deltaMax == deltaW):
		sendMotionCmd("-90 0\n")
        return P0,deltaMax

def optDist(P, delta):
	global reachedFlag
        moveDist = 200
        while(abs(moveDist) > 40):
		if(delta != 0):
			lamda = dmax/(math.pow(delta,2))
		else:
			lamda = dmax
		#lamda = 10 - 15*(math.pow(10, (-3)*(P+POWER_OFFSET)/(2.5*10)) - 5*math.pow(10, (-2)*(P+POWER_OFFSET)/(2.5*10)))

		moveDist = math.ceil(lamda * delta)	

		dataWrite = "0 " + str(moveDist) + "\n"

		print "optDist :" + " P: " + str(P) + " delta: " + str(delta) + " lamda :" + str(lamda) + "  " + "moveDist :" + str(moveDist)

		sendMotionCmd(dataWrite)

		Pnew = getRSSI()
		#print "Pnew : " + str(Pnew)
		delta = Pnew - P
		P = Pnew
		if(P > -35):
                        reachedFlag == 1
                        break


	if(P > -35):
		return 1
	else:
		return 0

def FBProbe():
	P = getRSSI()
	print "P: " + str(P) + "  dBm" 
	sendMotionCmd("0 80\n")
	PF = getRSSI()
	print "PF: " + str(PF) + "  dBm" 
	sendMotionCmd("0 -80\n")
	P = P + getRSSI()
	sendMotionCmd("0 -80\n")
	PB = getRSSI()
	print "PB: " + str(PB) + "  dBm" 
	sendMotionCmd("0 80\n")
	P = P + getRSSI()
	P = P/3
	print "P: " + str(P) + "  dBm" 

	deltaF = PF - P
	deltaB = PB - P
   
	deltaMax = max(deltaF, deltaB)
	print "deltaMax: " + str(deltaMax) 
	#print "P: " + str(P) + "  dBm" + "PF: " + str(PF) + "  " + "PB: " + str(PB) + "  " + "deltaMax :" + str(deltaMax)

	if(deltaMax == deltaF):
		pass
	elif(deltaMax == deltaB):
		sendMotionCmd("180 0\n")

	return P, deltaMax


time.sleep(1)
P, delta = NSEWProbe()
Out1 = optDist(P, delta)

if (Out1 == 1):
	print "Pahunch gya BC1 !!"
else:
	sendMotionCmd("90 0\n")
	P, delta = FBProbe()
	Out2 = optDist(P, delta)
	if(Out2 == 1):
		print "Pahunch gya BC1 !!"
	else: 
		print "Couldnot optimize!! Go fuck urself"
	
		

