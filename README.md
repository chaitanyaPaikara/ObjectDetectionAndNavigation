# ObjectDetectionAndNavigation

Repository for Object detection, Floor Segmentation and Navigation of a Ground robot using Monocular Vision

1. SLIC : Consists of a variation of K-means clustering algortihm to dividethe images into superpixels of pepetual importance. slic_v3.py is the latest vesion.
2. Camera Calibration : Codes for calibratrion of Raspi Cam and generating 3D world coordinates from 2D image coordinates using Inverse perspective transform to get floor obstacle distances.
3. Arduino codes: Codes for low level controller arduino to control the robot's actuators and motion in the x,y plane. Communication protocol works over serial communication.
4. WifiLocalisationCodes: Codes for Wifi based indoor localistion of a robot. Currently consists of 3 algorithms to probe and identify the position of a wifi emmiter in the vicinity.
	a. Perpendicular Probing (Distance probing)
	b. NSEW Probing (Distance probing)
	c. Multiple wifi receivers based probing (Angular probing)