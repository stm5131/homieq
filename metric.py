import pandas as pd
import math
import random
import pygame
import numpy as np

from plot import *

# draw some text into an area of a surface
# automatically wraps words
# returns any text that didn't get blitted
def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word      
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text





def initial_question(flags):
	#print(flags)
	if (np.any(flags.dangerco2)):
		text = "You should open a window or step outside. Your CO2 level is higher than average."
	elif(np.any(flags.dangerpm)):
		text = "Hey! There is an abnormally high level of dust or smoke in your room!"
	elif(np.any(flags.highpm)):
		text = "Did you just vacuum? Your dust levels are rising."
	elif (np.any(flags.highco2)):
		text = "Do you have time to take a break? Your rooms CO2 is higher than average."
	elif (np.any(flags.isloud)):
		text = "Ouch! Is it really loud in here?? You should protect your hearing!"
	else:
		if (np.any(flags.ishot)):
			text = "Are you feeling warm? I noticed it got a little warmer in here."
		elif(np.any(flags.iscold)):
			text = "Brrr! Are you cold? I noticed it cooled off in here."
		elif(np.any(flags.isdark)):
			text = "Pretty Dark in here right? Can you turn on some lights?"
		elif(np.any(flags.ishumid)):
			text = "Blegh. Do you feel like it's humid? I noticed the humidity has risen in here."
		elif(np.any(flags.isdry)):
			text = "My skin feels dry, do you feel the same? The humidity has dropped in this room."
		else:
			text = "No idea how this happened but I am talking without a reason!"
	return text

def explain(flags):
	#print(flags)
	if (np.any(flags.dangerco2)):
		text = "Average outside CO2 concentration is ~400ppm, yours is much higher, it can cause headaches and drowsiness."
	elif(np.any(flags.dangerpm)):
		text = "Safe short term exposure for PM2.5 concentration is 35 ug/m3, you have reached that limit."
	elif(np.any(flags.highpm)):
		text = "Safe long term exposure for PM2.5 concentration is 12 ug/m3, you have reached that limit."
	elif (np.any(flags.highco2)):
		text = "Average outside CO2 concentration is ~400ppm, yours is higher, you might feel drowsy."
	elif (np.any(flags.isloud)):
		text = "Hearing loss can occur at SPL (sound pressure levels) of 70dB, you have reached that limit."
	else:
		if (np.any(flags.ishot)):
			text = "I check to see if there are ways to save energy or give solutions for comfort, my simulation says I should feel hot. I will adapt based on your responses."
		elif(np.any(flags.iscold)):
			text = "I check to see if there are ways to save energy or give solutions for comfort, my simulation says I should feel cold. I will adapt based on your responses."
		elif(np.any(flags.isdark)):
			text = "Studys show that having more than the minimum amount of light improves your focus."
		elif(np.any(flags.ishumid)):
			text = "I check to see if there are ways to save energy or give solutions for comfort, my simulation says I should feel humid. I will adapt based on your responses."
		elif(np.any(flags.isdry)):
			text = "I check to see if there are ways to save energy or give solutions for comfort, my simulation says I should feel dry. I will adapt based on your responses."
		else:
			text = "No idea how this happened but I am talking without a reason!"
	return text

class text_box:
	def __init__(self,screen):
		#Box location, size, state flags and font
		self.location = ()
		self.size = ()
		self.start = False
		self.closing = False
		self.waiting = False
		self.newtext = False
		self.font = pygame.font.Font('font/Pixeltype.ttf',35)
		self.screen = screen
		self.i = 0

	def draw_box(self,text,location,size,dt):
		if not self.start:
			if not self.closing:
				if not self.waiting:
					self.start = True
					self.i=0
		if self.start:
			if self.i < 1:
				self.i+=0.1*dt
			else:
				self.start = False
				self.waiting = True
				self.i=0
			box = pygame.Surface((size[0]*(self.i),size[1]))
			box.fill((0,0,0))
			box.set_alpha(200)
			self.screen.blit(box,location)
		elif self.closing:
			if self.i < 1:
				self.i+=0.25*dt
			else:
				self.closing = False
				self.i=0
			box = pygame.Surface((size[0]*(1-self.i),size[1]))
			box.fill((0,0,0))
			box.set_alpha(200)
			self.screen.blit(self.box,location)

		elif self.waiting:
			box = pygame.Surface(size)
			box.fill((0,0,0))
			box.set_alpha(255)
			drawText(box,text[0:round(self.i)],(255,255,255),box.get_rect(),self.font)
			self.screen.blit(box,location)

			if round(self.i)<len(text):
				self.i+=0.25*dt
			if self.newtext:
				self.newtext=False
				self.i=0

class button:
	def __init__(self,screen,size):
		#Box location, size, state flags and font
		self.location = ()
		self.size = ()
		self.font = pygame.font.Font('font/Pixeltype.ttf',35)
		self.box = pygame.Surface(size)
		self.box_rect = self.box.get_rect()
		self.size = size
		self.screen = screen
	def draw_box(self,location,text):
		if self.is_clicked():
			self.box.fill((100,100,100))
		else:
			self.box.fill((0,0,0))

		self.box.set_alpha(120)

		button_text = self.font.render(text, False, (255,255,255))
		self.box_rect = self.box.get_rect()
		text_rect = button_text.get_rect(center = self.box_rect.center)

		self.box.blit(button_text, text_rect)
		self.screen.blit(self.box,location)

		self.box_rect = self.box.get_rect(topleft = location)

	def is_clicked(self):
		return pygame.mouse.get_pressed()[0] and self.box_rect.collidepoint(pygame.mouse.get_pos())






#Sensor Acquisition object
class actor:
	def __init__(self , x , y, canvas):
		self.wait=0
		self.x = x
		self.y = y
		self.desired = 0
		self.p1 = pygame.image.load('graphics/player/player/s1.png').convert_alpha()
		self.p2 = pygame.image.load('graphics/player/player/w1.png').convert_alpha()
		self.p3 = pygame.image.load('graphics/player/player/w2.png').convert_alpha()

		self.p4 = pygame.image.load('graphics/player/player/portrait1.png').convert_alpha()
		self.p5 = pygame.image.load('graphics/player/player/portrait2.png').convert_alpha()

		self.isTimeout = False

		self.delay = 60

		self.length = 0
		self.explain = False
		self.canvas = canvas

		self.t_box = text_box(self.canvas)
		self.button1 = button(self.canvas,(150,50))
		self.button2 = button(self.canvas,(150,50))
		self.ypressed = False
		self.npressed = False
		self.state = 0
		self.is_occupied = False
		self.keep_alive = 3600
	
	def occupancy_check(self, delta, mouse, touch):
		#Time in seconds to wait for question response
		font = pygame.font.Font('font/Pixeltype.ttf',35)
		self.delay -= (1/60)*delta
		#Check if no response after 60 seconds
		if self.delay<=0:
			self.is_occupied = False
			self.state = 0
			self.delay=60

		#Darken background, draw scaled character, text box and response boxes.

		
		if(self.state>0):
			bg = pygame.Surface((800,400))
			bg.fill((0,0,0))
			bg.set_alpha(120)
			self.canvas.blit(bg,(0,0))
			if(round(self.t_box.i/2)%2):
				self.canvas.blit(pygame.transform.scale(self.p4  , (400,450)), (400, 0) )
			else:
				self.canvas.blit(pygame.transform.scale(self.p5  , (400,450)), (400, 0) )
			#Conversation states
			if(self.state==1):
				event_text ="Just checking, are you still here?"
				self.t_box.draw_box(event_text, (100,75), (300,200), delta)
				self.button1.draw_box((100,300),"Yes")

			if(self.button1.is_clicked()):
				self.ypressed=True
			elif(self.ypressed):
				self.state=0
				self.ypressed = False
				self.is_occupied = True
				self.t_box.newtext = True
				self.t_box.start = True
				self.t_box.i = 0
				self.delay=60
	def initial_convo(self, delta, mouse, touch):
		#Time in seconds to wait for question response
		font = pygame.font.Font('font/Pixeltype.ttf',35)
		self.delay -= (1/60)*delta
		#Check if no response after 60 seconds
		if self.delay<=0:
			self.isTimeout = True
			self.state = 0

		#Darken background, draw scaled character, text box and response boxes.

		
		if(self.state>0):
			bg = pygame.Surface((800,400))
			bg.fill((0,0,0))
			bg.set_alpha(120)
			self.canvas.blit(bg,(0,0))
			if(round(self.t_box.i/2)%2):
				self.canvas.blit(pygame.transform.scale(self.p4  , (400,450)), (400, 0) )
			else:
				self.canvas.blit(pygame.transform.scale(self.p5  , (400,450)), (400, 0) )

			#Conversation states
			if(self.state==1):
				event_text ="Howdy! Would you like me to be active for today?"
				self.t_box.draw_box(event_text, (100,75), (300,200), delta)
				self.button1.draw_box((100,300),"Yes")
				self.button2.draw_box((250,300),"Skip")
			elif(self.state==2):
				event_text ="Do you want me to explain want I will be doing?"
				self.t_box.draw_box(event_text, (100,75), (300,200), delta)
				self.button1.draw_box((100,300),"Yes, Explain")
				self.button2.draw_box((250,300),"I'm ok")
				self.is_occupied=True
			elif(self.state==3):
				event_text ="I am a virtual assistant that will learn based on your feedback and will provide helpful advice for your indoor comfort."
				self.t_box.draw_box(event_text, (50,175), (400,115), delta)
				self.button1.draw_box((100,300),"Anything else?")
				self.button2.draw_box((250,300),"Okay.")
				self.is_occupied=True
			elif(self.state==4):
				event_text ="Not yet but I plan to help give you control of your home back!"
				self.t_box.draw_box(event_text, (100,75), (300,200), delta)
				self.button1.draw_box((100,300),"Thank you")
				self.button2.draw_box((250,300),"Okay.")
			else:
				self.state=0
				self.delay=60
				self.is_occupied=True


			#If yes Button is clicked, throw button flag
			#If flag is thrown and mouse button is lifted (click finished)
			#Check to see if yes or no, if Yes, increase to next conversation
			#if no, close conversation
			if(self.button1.is_clicked()):
				self.ypressed=True
			elif(self.button2.is_clicked()):
				self.npressed=True
			elif(self.ypressed):
				self.state+=1
				self.ypressed = False
				self.t_box.newtext = True
				
			elif(self.npressed):
				self.state=0
				self.npressed = False



	def ask_event(self, delta, flag, mouse, touch):
		#Time in seconds to wait for question response
		font = pygame.font.Font('font/Pixeltype.ttf',35)
		self.delay -= (1/60)*delta
		#Check if no response after 60 seconds
		if self.delay<=0:
			self.isTimeout = True
			self.state = 0

		#Darken background, draw scaled character, text box and response boxes.

		
		if(self.state>0):
			bg = pygame.Surface((800,400))
			bg.fill((0,0,0))
			bg.set_alpha(120)
			self.canvas.blit(bg,(0,0))
			if(round(self.t_box.i/2)%2):
				self.canvas.blit(pygame.transform.scale(self.p4  , (400,450)), (400, 0) )
			else:
				self.canvas.blit(pygame.transform.scale(self.p5  , (400,450)), (400, 0) )

			#Conversation states
			if(self.state==1):
				event_text ="Got a moment?"
				self.t_box.draw_box(event_text, (100,75), (300,200), delta)
				self.button1.draw_box((100,300),"Yes")
				self.button2.draw_box((250,300),"Not Now")
			elif(self.state==2):
				event_text =initial_question(flag)
				self.t_box.draw_box(event_text, (100,75), (300,200), delta)
				self.button1.draw_box((100,300),"Yes, Explain")
				self.button2.draw_box((250,300),"I'm ok")
			elif(self.state==3):
				event_text =explain(flag)
				self.t_box.draw_box(event_text, (50,175), (400,115), delta)
				self.button1.draw_box((100,300),"Thanks.")
				self.button2.draw_box((250,300),"Okay.")
			elif(self.state==4):
				event_text ="Thank you for listening!"
				self.t_box.draw_box(event_text, (100,75), (300,200), delta)
				self.button1.draw_box((100,300),"Sure!")
				self.button2.draw_box((250,300),"Okay.")
			else:
				self.state=0
				self.delay=60


			#If yes Button is clicked, throw button flag
			#If flag is thrown and mouse button is lifted (click finished)
			#Check to see if yes or no, if Yes, increase to next conversation
			#if no, close conversation
			if(self.button1.is_clicked()):
				self.ypressed=True
			elif(self.button2.is_clicked()):
				self.npressed=True
			elif(self.ypressed):
				self.state+=1
				self.ypressed = False
				self.t_box.newtext = True
				
			elif(self.npressed):
				self.state=0
				self.npressed = False


	def idle_update(self, delta, canvas):

		if self.wait>0:
			self.canvas.blit(pygame.transform.scale(self.p1,(64,128)),(self.x,self.y))
			self.wait-=1*delta
			self.wait = math.ceil(self.wait)
			if self.wait<0:
				self.wait=0
		else:
			if math.fabs(self.x-self.desired)<0.5:
				self.x = self.desired
				self.desired = random.randint(100,700)
				self.canvas.blit(pygame.transform.scale(self.p1,(64,128)),(self.x,self.y))
				self.wait = random.randint(50,100)
			elif self.x>self.desired:
				self.x-=1*delta
				self.x=math.floor(self.x)
				if self.x%40<12:
					self.canvas.blit(pygame.transform.scale(pygame.transform.flip(self.p2,True,False),(64,128)),(self.x,self.y))
				elif self.x%40>=12 and self.x%40<20:
					self.canvas.blit(pygame.transform.scale(pygame.transform.flip(self.p1,True,False),(64,128)),(self.x,self.y))
				elif self.x%40>=20 and self.x%40<32:
					self.canvas.blit(pygame.transform.scale(pygame.transform.flip(self.p3,True,False),(64,128)),(self.x,self.y))
				elif self.x%40>=32 and self.x%40<40:
					self.canvas.blit(pygame.transform.scale(pygame.transform.flip(self.p1,True,False),(64,128)),(self.x,self.y))
			elif self.x<self.desired:
				self.x+=1*delta
				self.x=math.ceil(self.x)
				if self.x%40<12:
					self.canvas.blit(pygame.transform.scale(self.p2,(64,128)),(self.x,self.y))
				elif self.x%40>=12 and self.x%40<20:
					self.canvas.blit(pygame.transform.scale(self.p1,(64,128)),(self.x,self.y))
				elif self.x%40>=20 and self.x%40<32:
					self.canvas.blit(pygame.transform.scale(self.p3,(64,128)),(self.x,self.y))
				elif self.x%40>=32 and self.x%40<40:
					self.canvas.blit(pygame.transform.scale(self.p1,(64,128)),(self.x,self.y))



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
			"Occupied":[]
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
		print(self.sensor_metrics)
		for i in self.flags:
			#print(self.flags[i][0])
			if self.flags[i][0]:
				print(i)
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
		print("Avg. Temperature: " + str(self.temp_avg) + " C " + "Inst. Temperature: " + str(self.sensor_metrics.Temperature.iat[-1]) + " C")
		print("Lower avg T Limit: " + str(self.limits.temp_offset[0]) + " C   " + "Upper avg T Limit: " + str(self.limits.temp_size[0]+self.limits.temp_offset[0]) + " C")
		print("Lower T Limit: 21 C    Upper T Limit: 27 C")
		#print("Avg. Humidity: " + str(self.hum_avg) + " % " + "Inst. Humidity: " + str(self.sensor_metrics.Humidity.iat[-1]) + " %")
		#print("Avg. CO2: " + str(self.co2_avg) + " ppm " + "Inst. CO2: " + str(self.sensor_metrics.CO2.iat[-1]) + " ppm")
		#print("Avg. PM2.5: " + str(self.pm25_avg) + " ug/m3 " + "Inst. PM2.5: " + str(self.sensor_metrics.PM25.iat[-1]) + " ug/m3")

	def comfort_check(self):
		#PM2.5 Check
		if self.pm25_avg>self.limits.pmhigh[0] or (self.sensor_metrics.PM25.tail(1)[len(self.sensor_metrics.index)-1]>35):
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
		if self.temp_avg>(self.limits.temp_size[0]+self.limits.temp_offset[0]) or (self.sensor_metrics.Temperature.tail(1)[len(self.sensor_metrics.index)-1]>27):
			self.flags.ishot = True
		elif self.temp_avg<(self.limits.temp_offset[0]) or (self.sensor_metrics.Temperature.tail(1)[len(self.sensor_metrics.index)-1]<21):
			self.flags.iscold = True


		#Humidity Check
		if self.hum_avg>(self.limits.hum_size[0]+self.limits.hum_offset[0]) or (self.sensor_metrics.Humidity.tail(1)[len(self.sensor_metrics.index)-1]>65):
			self.flags.ishumid = True
		elif self.hum_avg<self.limits.hum_offset[0] or (self.sensor_metrics.Humidity.tail(1)[len(self.sensor_metrics.index)-1]<25):
			self.flags.isdry = True
		#print("Comfort checked")
		
