#!/usr/bin/env python
#-----------------------------------------------------------------------------
# qwiic_twist_ex1.py
#
# Simple Example for the Qwiic Twist Device
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, May 2019
# 
# This python library supports the SparkFun Electroncis qwiic 
# qwiic sensor/board ecosystem on a Raspberry Pi (and compatable) single
# board computers. 
#
# More information on qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#
#==================================================================================
# Copyright (c) 2019 SparkFun Electronics
#
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal 
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
# SOFTWARE.
#==================================================================================
# Example 1
#

from __future__ import print_function
import qwiic_dual_encoder_reader
import time
import sys
import qwiic_scmd

L_MTR = 0
L_FWD = 1
L_BWD = 0

R_MTR = 1
R_FWD = 1
R_BWD = 0

DIRECTION_FWD = 1
DIRECTION_BWD = 0

def runExample():

	print("\nSparkFun Qwiic Dual Encoder Reader   Example 1\n")
	myEncoders = qwiic_dual_encoder_reader.QwiicDualEncoderReader()

	if myEncoders.connected == False:
		print("The Qwiic Dual Encoder Reader device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	myEncoders.begin()
	myEncoders.count1 = 0
	myEncoders.count2 = 0
	myMotors = qwiic_scmd.QwiicScmd()
	myMotors.begin()

	direction = DIRECTION_FWD
	motor_speed_target = 70
	left_motor_speed = 53
	right_motor_speed = motor_speed_target
	motor_speed_correction = 0
	count12_delta = 0
	prev_count12_delta = 0
	error_change = 0
	P_gain = 0.2
	D_gain = 1
	myMotors.enable()
	myMotors.set_drive(L_MTR,L_FWD,left_motor_speed)
	myMotors.set_drive(R_MTR,R_FWD,right_motor_speed)
	for i in range(0,100):
		time.sleep(.03)
		count12_delta = myEncoders.count1 - (-myEncoders.count2)
		error_change = count12_delta - prev_count12_delta
		if myEncoders.count1 != (-myEncoders.count2):
			motor_speed_correction = count12_delta
			motor_speed_correction *= P_gain #proportional adjustment
			motor_speed_correction += (D_gain * error_change) #derivative adjustment, looks at the change in error, if it gets smaller, than slow down the correction
		left_motor_speed -= motor_speed_correction
		myMotors.set_drive(L_MTR, L_FWD, (left_motor_speed))
		print("Count1: %d, Count2: %d, LMspd: %d, RMspd: %d, cntdelta: %d, error_change: %d" % \
                      (myEncoders.count1, -myEncoders.count2, left_motor_speed, right_motor_speed, count12_delta, error_change))
		prev_count12_delta = count12_delta
		
	myMotors.disable()
	
	time.sleep(1)
	
	#myMotors.enable()	
	#myMotors.set_drive(L_MTR,L_BWD,50)
	#myMotors.set_drive(R_MTR,R_BWD,50)
	#for i in range(0,40):
	#	print("Count1: %d, Count2: %s" % (myEncoders.count1, -myEncoders.count2))
	#	time.sleep(.1)
	#myMotors.disable()

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 1")
		sys.exit(0)



