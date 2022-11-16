import math
import random
import pandas as pd
import pygame

#Sensor Acquisition object
class sensor:
	def __init__(self):
		self.t_sen = 21
		self.rh_sen = 55
		self.p_sen = 1000
		self.co2_sen = 450
		self.pm = 2
		self.light = 0
		self.audio = (0,0,0)
		self.s_data = 0
		self.select = 0
		self.key=False
		#Initialize sensors

	def dummy_sensor_read(self,occupied):
		#Collect sensor data
		#Semi Random sensor generation for testing
		#Testing Data
		self.t_sen += 0.05*random.randrange(-1,1)
		if self.t_sen<22:
			self.t_sen=22
		self.rh_sen += 0.1*random.randrange(-1,1)
		if self.rh_sen<20:
			self.rh_sen=20
		self.p_sen += 0.001*random.randrange(-1,1)
		self.co2_sen += random.randrange(-1,1)
		if self.co2_sen<400:
			self.co2=400
		self.pm += 0.1*random.randrange(-1,1)
		if self.pm<0:
			self.pm=0
		self.light = 0.1*random.randrange(-1,1)
		if self.light<0:
			self.light=0


		self.audio = random.randrange(10,20)
		self.s_data = pd.DataFrame({
			"Temperature":[self.t_sen],
			"Humidity":[self.rh_sen],
			"Pressure":[self.p_sen],
			"CO2":[self.co2_sen],
			"Light":[self.light],
			"PM25":[self.pm],
			"Audio":[self.audio],
			"Occupied":[occupied]
			})
		#print(self.s_data)

	def control_sensor(self,dt,keys):
		#Collect sensor data
		#Semi Random sensor generation for testing
		#Testing Data
		if keys[pygame.K_RIGHT]:
			if self.select<6:
				self.select+=1
			else:
				self.select=0
		if keys[pygame.K_UP]:
			if(self.select==0):
				self.t_sen+=1*dt
			elif(self.select==1):
				self.rh_sen+=1*dt
			elif(self.select==2):
				self.p_sen+=1*dt
			elif(self.select==3):
				self.co2_sen+=10*dt
			elif(self.select==4):
				self.pm+=1*dt
			elif(self.select==5):
				self.light+=1*dt
			else:
				self.audio+=0.1*dt
		elif keys[pygame.K_DOWN]:
			if(self.select==0):
				self.t_sen-=1*dt
			elif(self.select==1):
				self.rh_sen-=1*dt
			elif(self.select==2):
				self.p_sen-=10*dt
			elif(self.select==3):
				self.co2_sen-=2*dt
			elif(self.select==4):
				self.pm-=1*dt
			elif(self.select==5):
				self.light-=1*dt
			else:
				self.audio-=0.1*dt

		self.s_data = pd.DataFrame({
			"Temperature":[self.t_sen],
			"Humidity":[self.rh_sen],
			"Pressure":[self.p_sen],
			"CO2":[self.co2_sen],
			"Light":[self.light],
			"PM25":[self.pm],
			"Audio":[self.audio],
			"Occupied":[]
			})
		#print(self.s_data)