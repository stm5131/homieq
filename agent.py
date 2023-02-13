import pandas as pd
import math
import random
import pygame
import numpy as np

from plot import *

def parse_to_df(sensor,limits,hours,minutes,response):
	df=pd.DataFrame()
	df = pd.concat([sensor,limits],axis=1)
	#print(df)
	df['response'] = response
	df['hours'] = hours
	df['minutes'] = minutes
	#print(df)
	return df


class Agent:
	def __init__(self):


		#5 Minute Delta
		#1 Hour Temperature Average
		self.temp_trend = 0
		self.temp_avg = 0

		#5 Minute Delta
		#1 Hour Humidity Average
		self.hum_trend = 0
		self.hum_avg = 0

		#1 Hour CO2 Average
		#10 Hour CO2 Average
		self.co2_avg = 0
		self.co2_10avg = 0

		#1 Hour Sound Average
		self.snd_avg = 0

		#1 Hour PM25 Average
		#10 Hour PM25 Average
		self.pm25_avg = 0
		self.pm25_10avg = 0

		#Used for conversation selection
		self.subject = 0

		#Input DataFrame for metrics and recording
		self.sensor_metrics = pd.DataFrame({
			"Temperature":[],
			"Humidity":[],
			"Pressure":[],
			"CO2":[],
			"Light":[],
			"PM25":[],
			"Audio":[]
			})

		#Comfort & Alert Flags DataFrame
		self.flags = pd.DataFrame({
			'ishot':[False],'iscold':[False],
			'ishumid':[False],'isdry':[False],
			'highco2':[False],'dangerco2':[False],
			'isdark':[False],'isloud':[False],
			'highpm':[False],'dangerpm':[False]})

		#Learning limits
		self.limits = pd.DataFrame({
			#Self Adjusting Limits
			'temp_size':[4],'temp_offset':[20],
			'hum_size':[25],'hum_offset':[40],
			'light':[150],
			'sound':[30],
			#Hard Limits
			'co2':[2000],
			'pmlow':[12], 'pmhigh':[35]
			})

		self.is_alerted = False

		self.is_occupied = False #Bool to show occupancy
		self.keep_alive = 0 #Timer for occupancy sensing questions, probably the wrong term
	#Feedback adjustment & learning
	def recieve_feedback(self, Response):
		if is_alerted:
			is_alerted = False
			for i in self.flags:
				if self.flags[i]:
					#print(self.flags.keys()[i])
					self.flags[i] = False

	#Update sensor readings from a constructed array
	def update(self,realtime):
		#Collect sensor data

		self.sensor_metrics=pd.concat([self.sensor_metrics , realtime], ignore_index = True)

		#print("Agent Updated / " + str(5*len(self.sensor_metrics)) + " seconds have passed.")

		for i in self.flags:
			#print(self.flags[i][0])
			if i:
				#print(i)
				self.flags[i] = [False]

	def calc(self):
		#Set Average values for each metrtic.
		self.temp_avg = round(self.sensor_metrics.Temperature.tail(3600).mean(),2)

		self.hum_avg = round(self.sensor_metrics.Humidity.tail(3600).mean(),2)

		self.co2_avg = round(self.sensor_metrics.CO2.tail(3600).mean(),2)
		self.co2_10avg = round(self.sensor_metrics.CO2.tail(36000).mean(),2)

		self.pm25_avg = round(self.sensor_metrics.PM25.tail(3600).mean(),2)
		self.pm25_avg = round(self.sensor_metrics.PM25.tail(36000).mean(),2)

		#print("Rolling Average Temperatures/n")
		#print("Avg. Temperature: " + str(self.temp_avg) + " C " + "Inst. Temperature: " + str(self.sensor_metrics.Temperature.iat[-1]) + " C")
		#print("Lower avg T Limit: " + str(self.limits.temp_offset[0]) + " C   " + "Upper avg T Limit: " + str(self.limits.temp_size[0]+self.limits.temp_offset[0]) + " C")
		#print("Lower T Limit: 21 C    Upper T Limit: 27 C")
		#print("Avg. Humidity: " + str(self.hum_avg) + " % " + "Inst. Humidity: " + str(self.sensor_metrics.Humidity.iat[-1]) + " %")
		#print("Avg. CO2: " + str(self.co2_avg) + " ppm " + "Inst. CO2: " + str(self.sensor_metrics.CO2.iat[-1]) + " ppm")
		#print("Avg. PM2.5: " + str(self.pm25_avg) + " ug/m3 " + "Inst. PM2.5: " + str(self.sensor_metrics.PM25.iat[-1]) + " ug/m3")

	def comfort_check(self):
		#PM2.5 Check
		if self.pm25_avg>self.limits.pmhigh[0] or (self.sensor_metrics.PM25.tail(1)[len(self.sensor_metrics.index)-1]>35):
			self.flags.dangerpm = True
			self.conversation = 5
		elif self.pm25_10avg>self.limits.pmlow[0]:
			self.flags.highpm = True
			self.conversation = 5

		#CO2 Check
		if self.co2_avg>self.limits.co2[0]:
			self.flags.highco2 = True
			self.conversation = 6
		elif self.co2_10avg>self.limits.co2[0]:
			self.flags.dangerco2 = True
			self.conversation = 6

		#Sound Level Check
		#if self.snd_avg>self.limits.sound[0]:
		#	self.flags.isloud = True


		#Temp Check
		if self.temp_avg>(self.limits.temp_size[0]+self.limits.temp_offset[0]) or (self.sensor_metrics.Temperature.tail(1)[len(self.sensor_metrics.index)-1]>27):
			self.flags.ishot = True
			self.conversation = 1
		elif self.temp_avg<(self.limits.temp_offset[0]) or (self.sensor_metrics.Temperature.tail(1)[len(self.sensor_metrics.index)-1]<21):
			self.flags.iscold = True
			self.conversation = 2


		#Humidity Check
		if self.hum_avg>(self.limits.hum_size[0]+self.limits.hum_offset[0]) or (self.sensor_metrics.Humidity.tail(1)[len(self.sensor_metrics.index)-1]>65):
			self.flags.ishumid = True
			self.conversation = 3
		elif self.hum_avg<self.limits.hum_offset[0] or (self.sensor_metrics.Humidity.tail(1)[len(self.sensor_metrics.index)-1]<25):
			self.flags.isdry = True
			self.conversation = 4

		#print("Comfort checked")
		
