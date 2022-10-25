import math
import random
import pandas as pd

#Sensor Acquisition object
class sensor:
	def __init__(self):
		self.t_sen = 24
		self.rh_sen = 40
		self.p_sen = 999
		self.co2_sen = 400
		self.pm = 5
		self.light = 0
		self.audio = (0,0,0)
		self.s_data = []
		#Initialize sensors

	def dummy_sensor_read(self):
		#Collect sensor data

		#Testing Data
		self.t_sen += 0.05*random.randrange(-1,2)
		if self.t_sen<22:
			self.t_sen=22
		self.rh_sen += 0.1*random.randrange(-1,2)
		if self.rh_sen<20:
			self.rh_sen=20
		self.p_sen += 0.001*random.randrange(-1,2)
		self.co2_sen += random.randrange(-1,2)
		if self.co2_sen<400:
			self.co2=400
		self.pm += 0.1*random.randrange(-1,2)
		if self.pm<0:
			self.pm=0
		self.light = 0.1*random.randrange(-1,2)
		if self.light<0:
			self.light=0


		self.audio = (random.randrange(10,20),random.randrange(10,20),random.randrange(10,20))
		self.s_data = pd.DataFrame({
			"Temperature":[self.t_sen],
			"Humidity":[self.rh_sen],
			"Pressure":[self.p_sen],
			"CO2":[self.co2_sen],
			"Light":[self.light],
			"PM25":[self.pm],
			"Audio":[self.audio],
			})
		#print(self.s_data)