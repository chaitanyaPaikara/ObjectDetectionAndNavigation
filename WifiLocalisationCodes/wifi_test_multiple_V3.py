#front 2
#right 1
import os
import math
import time
import numpy as np
import csv
import matplotlib.pyplot as plt
import serial
import time
ser = serial.Serial("/dev/ttyACM0", 38400)
fla = 0
ack = 101

Data = ''
def dis(val):
	global fla,Data,ack
	if val == 1.2:
                Data = '0 120\n'
                print "Move dist : 120cm"
	elif val == 1:
		Data = '0 100\n'
		print "Move dist : 100cm"
	elif val == 0.8:
		Data = '0 80\n'
		print "Move dist : 70cm"
	elif val == 0.6:
                Data = '0 100\n'
                print "Move dist : 60cm"
	elif val == 0.4:
		Data = '0 40\n'
		print "Move dist : 40cm"
	elif val == 0.2:
		Data = '0 20\n'
		print "Move dist : 20cm"
	elif val == 0.1:
                Data = '0 10\n'
                print "Move dist : 10cm"
	elif val == 0:
		Data = '0 0\n'
		print "No Motion"
	ser.write(Data)
	time.sleep(1)

	while (fla == 0):
		if(ser.inWaiting() > 0):
        		data_read = ser.readline()
       			#print int(data_read)
        		if(int(data_read) == ack):
        		    fla = 1
	fla = 0
def biggest(a, b, c, d):
  	Max = a
    	if b > Max:
        	Max = b    
    	if c > Max:
        	Max = c
    	if d > Max:
        	Max = d
    	return Max

def quadrant(val):
	global fla,Data,ack
	if val == 1:
		Data = '-90 0\n'
	elif val == 2:
		Data = '0 0\n'
	elif val == 3:
		Data = '90 0\n'
	elif val == 4:
		Data = '180 0\n'
	
	#print Data
	ser.write(Data)
	time.sleep(1)

	while (fla == 0):
		if(ser.inWaiting() > 0):
        		data_read = ser.readline()
       			#print int(data_read)
        		if(int(data_read) == ack):
        		    fla = 1
	fla = 0
	#move distance

	
def main0():
	
	cmd = "iwconfig wlan0 | grep -i --color quality | grep -i --color signal"

	data = os.popen(cmd).read()

	
	link_quality = ''
	signal_strength = ''	
	link_quality = data[23:25]
	signal_strength = data[43:46]

	rssi_dBm = int(signal_strength)
	quality = int(link_quality)
	rssi_dB = rssi_dBm - 30

	freq = 2437
		
	distance = math.pow(10.0, (27.55 - (20*math.log10(freq)) + math.fabs(rssi_dBm))/20.0)

	data_to_write =  "wlan0: RSSI = " + str(rssi_dBm) + " dBm  |  Quality = " + str(quality) + "/70" + "  |  Distance = " + str(distance) + " m" + "\n"
	print data_to_write
	return rssi_dBm
	#time.sleep(0.05)

def main1():
	sum = 0
        for i in range(1, 20):
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

                distance = math.pow(10.0, (27.55 - (20*math.log10(freq)) + math.fabs(rssi_dBm))/20.0)

                sum = sum + rssi_dBm
		time.sleep(0.001)

        rssi_dBm = sum/20
	data_to_write =  "wlan1: RSSI = " + str(rssi_dBm) + " dBm  |  Quality = " + str(quality) + "/70" + "  |  Distance = " + str(distance) + " m" + "\n"
	print data_to_write
        return rssi_dBm
        #time.sleep(0.05)


def main2():
	sum = 0
        for i in range(1, 20):
		cmd = "iwconfig wlan2 | grep -i --color quality | grep -i --color signal"

		data = os.popen(cmd).read()

	
		link_quality = ''
		signal_strength = ''	
		link_quality = data[23:25]
		signal_strength = data[43:46]

		rssi_dBm = int(signal_strength)
		quality = int(link_quality)
		rssi_dB = rssi_dBm - 30

		freq = 2437
		
		distance = math.pow(10.0, (27.55 - (20*math.log10(freq)) + math.fabs(rssi_dBm))/20.0)
			
		sum = sum + rssi_dBm
		time.sleep(0.001)
	
	rssi_dBm = sum/20
	data_to_write =  "wlan2: RSSI = " + str(rssi_dBm) + " dBm  |  Quality = " + str(quality) + "/70" + "  |  Distance = " + str(distance) + " m" + "\n"
	print data_to_write

	return rssi_dBm
	#time.sleep(0.05)

def main3():
	sum = 0
        for i in range(1, 20):
                cmd = "iwconfig wlan3 | grep -i --color quality | grep -i --color signal"

                data = os.popen(cmd).read()


                link_quality = ''
                signal_strength = ''
                link_quality = data[23:25]
                signal_strength = data[43:46]

                rssi_dBm = int(signal_strength)
                quality = int(link_quality)
                rssi_dB = rssi_dBm - 30

                freq = 2437

                distance = math.pow(10.0, (27.55 - (20*math.log10(freq)) + math.fabs(rssi_dBm))/20.0)

                sum = sum + rssi_dBm
                time.sleep(0.001)

        rssi_dBm = sum/20
	data_to_write =  "wlan3: RSSI = " + str(rssi_dBm) + " dBm  |  Quality = " + str(quality) + "/70" + "  |  Distance = " + str(distance) + " m" + "\n"
	print data_to_write

        return rssi_dBm


def main4():
	sum = 0
	for i in range(1, 20):
		cmd = "iwconfig wlan4 | grep -i --color quality | grep -i --color signal"

		data = os.popen(cmd).read()

	
		link_quality = ''
		signal_strength = ''	
		link_quality = data[23:25]
		signal_strength = data[43:46]

		rssi_dBm = int(signal_strength)
		quality = int(link_quality)
		rssi_dB = rssi_dBm - 30

		freq = 2437
		
		distance = math.pow(10.0, (27.55 - (20*math.log10(freq)) + math.fabs(rssi_dBm))/20.0)

		sum = sum + rssi_dBm
		time.sleep(0.001)

	rssi_dBm = sum/20 
	data_to_write =  "wlan4: RSSI = " + str(rssi_dBm) + " dBm  |  Quality = " + str(quality) + "/70" + "  |  Distance = " + str(distance) + " m" + "\n"
	print data_to_write
		
	return rssi_dBm
	#ime.sleep(0.05)
cnt = 0
reachedFlag = 0
time.sleep(1)

while (reachedFlag == 0):
	fla = 0
	#r = main0()
	r00 = main1()
	r01 = main2()
	r02 = main3()
	r03 = main4()
	
	#Data = '45 0\n'			
	#print Data
	#ser.write(Data)
	#time.sleep(1)

	#while(fla == 0):
	#	if(ser.inWaiting() > 0):
	#		data_read = ser.readline()
	#		print int(data_read)
	#		if( int(data_read) == ack):
	#			fla = 1
    
	#fla = 0
	#r10 = main1()
	#r11 = main2()
	#r12 = main3()
	#r13 = main4()
	m1 = max(r00,r01,r02,r03)

	if (m1 == r00):
		print "Max Strength at : wlan1"
		quadrant(1)
	elif (m1 == r01):
		print "Max Strength at : wlan2"
		quadrant(2)
	elif (m1 == r02):
		print "Max Strength at : wlan3"
		quadrant(3)
	elif (m1 == r03):
		quadrant(4)
		print "Max Strength at : wlan4"
	

	#r00 = main1()
	#r01 = main2()
	#r02 = main3()
	#r03 = main4()
	#m1 = biggest(r00,r01,r02,r03)
	#if (m1 == r01):
	m1 = abs(m1)
	if (m1>=55):
		#print '1m'
		dis(1.2)
	elif (m1>=45):
		#print '0.7m'
		dis(1)
	elif (m1 >= 40):
		#print '0.4m'
		dis(0.8)
	elif(m1 >= 36):
		#print '0.1m'
		dis(0.6)
	elif (m1 >= 33):
                #print '0.7m'
                dis(0.4)
	elif (m1>= 28):
                #print '0.7m'
                dis(0.2)
	elif (m1>=25):
		cnt = cnt +1
		print cnt
                dis(0.1)
	else:	
		#print 'stop'
		dis(0)
		reachedFlag = 1 
        if(cnt>10):
                dis(0)
                reachedFlag = 1
