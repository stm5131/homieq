import pandas as pd
import math
import random
import pygame

#Sensor Acquisition object
class actor:
	def __init__(self , x , y):
		self.wait=0
		self.x = x
		self.y = y
		self.desired = 0
		self.p1 = pygame.image.load('graphics/player/player/s1.png').convert_alpha()
		self.p2 = pygame.image.load('graphics/player/player/w1.png').convert_alpha()
		self.p3 = pygame.image.load('graphics/player/player/w2.png').convert_alpha()

		self.isYes = False
		self.isNo = False
		self.isTimeout = False
		self.noevent = True
		self.box = pygame.Surface((800,400))
		self.delay = 60
		
	def ask_event(self, delta, canvas, flag, mouse, touch):
		 #Time in seconds to wait for question response

		font = pygame.font.Font('font/Pixeltype.ttf',50)

		self.delay -= (1/60)*delta
		#Check if no response after 60 seconds
		if self.delay<=0:
			self.noevent = True
			self.isTimeout = True
		#Darken background, draw scaled character, text box and response boxes.
		self.box = pygame.Surface((800,400))
		self.box.fill((0,0,0))
		self.box.set_alpha(120)

		canvas.blit(self.box,(0,0))
		canvas.blit(pygame.transform.scale( self.p1, (256, 512) ) , (600, 450) )
		if( not self.isYes and not self.isNo):
			self.box = pygame.Surface((300,200))
			self.box.fill((50,50,50))
			event_text = font.render("Got a moment?", False, (255,255,255))
			self.box.blit(event_text,(0,0))
			canvas.blit(self.box,(100,50))
			

			self.box = pygame.Surface((125,75))
			self.box.fill((20,50,20))
			event_text = font.render("Yes!!", False, (255,255,255))
			self.box.blit(event_text,(0,0))
			canvas.blit(self.box,(100,300))

			self.box = pygame.Surface((125,75))
			self.box.fill((50,20,20))
			event_text = font.render("No..", False, (255,255,255))
			self.box.blit(event_text,(0,0))
			canvas.blit(self.box,(300,300))
			if(touch):
				if(mouse[0]<225 and mouse[0]>100):
					if(mouse[1]>300 and mouse[1]<375):
						self.isYes=True
						self.touch=False
						mouse=(0,0)
				elif(mouse[0]<425 and mouse[0]>300):
					if(mouse[1]>300 and mouse[1]<375):
						self.isNo=True
						self.touch=False
						mouse=(0,0)

		elif(self.isYes):
			self.box = pygame.Surface((300,200))
			self.box.fill((50,50,50))
			event_text = font.render("You should take a break,", False, (255,255,255))
			self.box.blit(event_text,(0,0))
			event_text = font.render("your CO2 is high.", False, (255,255,255))
			self.box.blit(event_text,(0,50))
			canvas.blit(self.box,(100,50))
			

			self.box = pygame.Surface((125,75))
			self.box.fill((20,50,20))
			event_text = font.render("Ok!", False, (255,255,255))
			self.box.blit(event_text,(0,0))
			canvas.blit(self.box,(100,300))
			self.box = pygame.Surface((125,75))
			self.box.fill((50,20,20))
			event_text = font.render("I can't", False, (255,255,255))
			self.box.blit(event_text,(0,0))
			canvas.blit(self.box,(300,300))
			if(touch):
				if(mouse[0]<225 and mouse[0]>100):
					if(mouse[1]>300 and mouse[1]<375):
						self.noevent=True
						self.touch=False
						mouse=(0,0)
				elif(mouse[0]<425 and mouse[0]>300):
					if(mouse[1]>300 and mouse[1]<375):
						self.noevent=True
						self.touch=False
						mouse=(0,0)

		elif(self.isNo):
			self.box = pygame.Surface((300,200))
			self.box.fill((50,50,50))
			event_text = font.render("Alright...", False, (255,255,255))
			self.box.blit(event_text,(0,0))
			canvas.blit(self.box,(100,50))
			self.box = pygame.Surface((125,75))
			self.box.fill((50,20,20))
			event_text = font.render("Ok", False, (255,255,255))
			self.box.blit(event_text,(0,0))
			canvas.blit(self.box,(300,300))
			if(touch):
				if(mouse[0]<425 and mouse[0]>300):
					if(mouse[1]>300 and mouse[1]<375):
						self.noevent=True
						self.touch=False
						mouse=(0,0)
		if(self.noevent):
			delay = 60

	def idle_update(self, delta, canvas):
		if self.wait>0:
			canvas.blit(pygame.transform.scale(self.p1,(64,128)),(self.x,self.y))
			self.wait-=1*delta
			self.wait = math.ceil(self.wait)
			if self.wait<0:
				self.wait=0
		else:
			if math.fabs(self.x-self.desired)<0.5:
				self.x = self.desired
				self.desired = random.randint(100,700)
				canvas.blit(pygame.transform.scale(self.p1,(64,128)),(self.x,self.y))
				self.wait = random.randint(50,100)
			elif self.x>self.desired:
				self.x-=1*delta
				self.x=math.floor(self.x)
				if self.x%40<12:
					canvas.blit(pygame.transform.scale(pygame.transform.flip(self.p2,True,False),(64,128)),(self.x,self.y))
				elif self.x%40>=12 and self.x%40<20:
					canvas.blit(pygame.transform.scale(pygame.transform.flip(self.p1,True,False),(64,128)),(self.x,self.y))
				elif self.x%40>=20 and self.x%40<32:
					canvas.blit(pygame.transform.scale(pygame.transform.flip(self.p3,True,False),(64,128)),(self.x,self.y))
				elif self.x%40>=32 and self.x%40<40:
					canvas.blit(pygame.transform.scale(pygame.transform.flip(self.p1,True,False),(64,128)),(self.x,self.y))
			elif self.x<self.desired:
				self.x+=1*delta
				self.x=math.ceil(self.x)
				if self.x%40<12:
					canvas.blit(pygame.transform.scale(self.p2,(64,128)),(self.x,self.y))
				elif self.x%40>=12 and self.x%40<20:
					canvas.blit(pygame.transform.scale(self.p1,(64,128)),(self.x,self.y))
				elif self.x%40>=20 and self.x%40<32:
					canvas.blit(pygame.transform.scale(self.p3,(64,128)),(self.x,self.y))
				elif self.x%40>=32 and self.x%40<40:
					canvas.blit(pygame.transform.scale(self.p1,(64,128)),(self.x,self.y))



class agent:
	def __init__(self, sample, delay):
		#Sampling rate
		self.sample = sample
		#Delay time in seconds
		self.delay = delay

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

		#Input DataFrame for metrics and recording
		self.sensor_metrics = pd.DataFrame({
			"Temperature":[],
			"Humidity":[],
			"Pressure":[],
			"CO2":[],
			"Light":[],
			"PM25":[],
			"Audio":[],
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
			'hum_size':[20],'hum_offset':[30],
			'light':[150],
			'sound':[30],
			#Hard Limits
			'co2':[2000],
			'pmlow':[12], 'pmhigh':[35]
			})

		self.is_alerted = False
	#Feedback adjustment & learning
	def recieve_feedback(self, Response):
		if is_alerted:
			is_alerted = False
			for i in self.flags:
				if self.flags[i]:
					print(self.flags.keys()[i])
					self.flags[i] = False

	#Update sensor readings from a constructed array
	def update(self,realtime):
		#Collect sensor data

		self.sensor_metrics=pd.concat([self.sensor_metrics , realtime], ignore_index = True)

		print("Agent Updated / " + str(5*len(self.sensor_metrics)) + " seconds have passed.")

	def calc(self):
		self.temp_avg = round(self.sensor_metrics.Temperature.tail(3600).mean(),2)

		self.hum_avg = round(self.sensor_metrics.Humidity.tail(3600).mean(),2)

		self.co2_avg = round(self.sensor_metrics.CO2.tail(3600).mean(),2)

		self.pm25_avg = round(self.sensor_metrics.PM25.tail(3600).mean(),2)

		#print("Rolling Average Temperatures/n")
		#print("Avg. Temperature: " + str(self.temp_avg) + " C " + "Inst. Temperature: " + str(self.sensor_metrics.Temperature.iat[-1]) + " C")
		#print("Avg. Humidity: " + str(self.hum_avg) + " % " + "Inst. Humidity: " + str(self.sensor_metrics.Humidity.iat[-1]) + " %")
		#print("Avg. CO2: " + str(self.co2_avg) + " ppm " + "Inst. CO2: " + str(self.sensor_metrics.CO2.iat[-1]) + " ppm")
		#print("Avg. PM2.5: " + str(self.pm25_avg) + " ug/m3 " + "Inst. PM2.5: " + str(self.sensor_metrics.PM25.iat[-1]) + " ug/m3")

	def comfort_check(self):
		#PM2.5 Check
		if self.pm25_avg>self.limits.pmhigh[0]:
			self.flags.dangerpm = True
		elif self.pm25_10avg>self.limits.pmlow[0]:
			self.flags.highpm = True

		#CO2 Check
		if self.co2_avg>self.limits.co2[0]:
			self.flags.highco2 = True
		elif self.co2_10avg>self.limits.co2[0]:
			self.flags.dangerco2 = True

		#Sound Level Check
		if self.snd_avg>self.limits.sound[0]:
			self.flags.isloud = True

		#Temp Check
		if self.temp_avg>(self.limits.temp_size[0]+self.limits.hum_offset[0]):
			self.flags.ishot = True
		elif self.temp_avg<self.limits.hum_offset[0]:
			self.flags.iscold = True

		#Humidity Check
		if self.hum_avg>(self.limits.hum_size[0]+self.limits.hum_offset[0]):
			self.flags.highco2 = True
		elif self.hum_avg>self.limits.hum_offset[0]:
			self.flags.dangerco2 = True
		print("Comfort checked")
		for i in self.flags:
			#print(self.flags[i][0])
			if self.flags[i][0]:
				print(i)
				self.flags[i] = False