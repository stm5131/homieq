import pygame
import os
from gui import *
import pandas as pd
import math
import random

class Player:
	def __init__(self,screen):
		#Create Sprite lists to be able to iterate through
		directories = ['/graphics/player/portrait/faces','/graphics/player/portrait/mouth','/graphics/player/sprite']
		self.face,self.mouth,self.sprite = [],[],[]
		#print("Starting graphics import")
		for directory in directories:
			i=0
			if directory == '/graphics/player/portrait/faces':
				#print("Importing Faces")
				for filename in os.scandir(os.getcwd()+directory):
					self.face.append(pygame.transform.scale(pygame.image.load(filename.path).convert_alpha(),(384,384)))
					i+=1
			elif directory == '/graphics/player/portrait/mouth':
				#print("Importing Mouths")
				for filename in os.scandir(os.getcwd()+directory):
					self.mouth.append(pygame.transform.scale(pygame.image.load(filename.path).convert_alpha(),(384,384)))
					i+=1
			elif directory == '/graphics/player/sprite':
				#print("Importing Sprites")
				for filename in os.scandir(os.getcwd()+directory):
					self.sprite.append(pygame.transform.scale(pygame.image.load(filename.path).convert_alpha(),(64,128)))
					i+=1
		#Create internal variables to use
		self.desired, self.x, self.wait, self.talk, self.i, self.k = 0,0,0,0,0,0 #Values used for sprite movement, waiting and portrait movement
		self.canvas = screen
		self.y = 216
		self.state = 0 #State 0 is for walking/idle animations, State 1 is engagement/portrait mode.

		self.text_box = Text_box(screen) #Text box object to be stored for conversation use

		self.buttons = [Button(screen,(225,50)),Button(screen,(225,50))] #Yes and No buttons
		#Button Locations and sizes
		self.box_location , self.size = (25,25),(400,250)
		self.b1_location , self.b2_location = (25,325),(275,325)
		self.text = []
		self.name = "HomIEQ"
		self.subject = 0 #Subjects range from 0-9 for each potential subject
		self.conversation = 0
		self.subconversation = 0
		self.pressed_down = 0
		self.response_given = 0
		#Subjects are [0-startup,1-occupancy,2-hot,3-cold,4-humid,5-dry,6-co2,7-pm,8-light,9-audio]
		#Subject is set by the agent model
#--------------------------------------------------------------------------------------------------
		i=1
		#print("Importing Text")
		while (i <= 10):
			if (i < 10):
				directory=os.getcwd()+'/text/0'+str(i)
			else:
				directory=os.getcwd()+'/text/'+str(i)
			i+=1
#--------------------------------------------------------------------------------------------------
			for filename in os.scandir(directory):
				#print(filename.path)
				df = pd.read_csv(filename.path)
				self.text.append(df.values.tolist())
		#print("Done")



	def update(self,dt):
		if(self.state):
			self.conversate(dt)
		else:
			self.walk(dt)

	def conversate(self,dt):
		#First find initial conversation text on basis of subject matter
		if(self.subject>0):
			subject_text = self.name + " : "+self.text[self.subject][0][0]
			response_1 = "Yes"
			#print(response_1)
			response_2 = "No"
		else:
			subject_text = self.name + " : "+self.text[self.subject][self.conversation][self.subconversation]

			#Get Responses
			response_1 = self.text[9][self.conversation][2]
			#print(response_1)
			response_2 = self.text[9][self.conversation][4]

		
		#print(response_2)
		#Then draw text box with iterative text
		self.text_box.draw_box(subject_text,self.box_location,self.size,dt)
		#Create Buttons
		self.buttons[0].draw_box(self.b1_location,response_1)
		self.buttons[1].draw_box(self.b2_location,response_2)
		#Draw Portrait
		
		#Blink Time is last XXX seconds of self.talk timer
		#Find Face
		if(self.talk<0):
			self.talk=random.randint(125,300)
			#print("blinking")
		else:
			self.talk-=dt

		if(self.talk>1):
			if(self.i<1):
				self.i=random.randint(1,3)
		else:
			self.i=0

		if self.text_box.start:
			y_loc = 400-self.text_box.i*330
		else:
			y_loc=50

		self.canvas.blit(self.face[self.i],(475,y_loc))

		if(self.text_box.done):
			self.canvas.blit(self.mouth[0],(475,y_loc))
		else:
			if (math.ceil(self.text_box.i)%4)<1:
				self.k=random.randint(0,3)
			self.canvas.blit(self.mouth[self.k],(475,y_loc))
		if(self.buttons[0].is_clicked()):
			self.pressed_down=1
		elif(self.buttons[1].is_clicked()):
			self.pressed_down=2
		else:
			if(self.pressed_down>1):
				self.pressed_down=0
				if(self.subject>0):
					self.state=0
				if(self.conversation<len(self.text[self.subject])):


					self.conversation+=int(self.text[9][self.conversation][3])

					self.response_given = 2

					self.text_box.i=0
					self.text_box.done=False
					if(self.conversation>=len(self.text[self.subject])):
						self.state=0
					

			elif(self.pressed_down>0):
				self.pressed_down=0
				if(self.subject>0):
					self.state=0
				if(self.conversation<len(self.text[self.subject])):

					self.conversation+=int(self.text[9][self.conversation][1])

					self.response_given = 1

					self.text_box.i=0
					self.text_box.done=False
					if(self.conversation>=len(self.text[self.subject])):
						self.state=0
					



		


	def walk(self,dt):
		if self.wait<0:
			self.wait=0
		elif self.wait>0:
			self.wait-=1*dt
			self.wait = math.ceil(self.wait)
			self.canvas.blit(self.sprite[0],(self.x,self.y))
		else:
			if math.fabs(self.x-self.desired)<5:
				self.x = self.desired
				self.desired = random.randint(100,700)
				self.wait = random.randint(50,100)
			if self.x>self.desired:
				self.x-=dt
				self.canvas.blit(pygame.transform.flip(self.sprite[math.ceil(self.x/13)%4],True,False),(self.x,self.y))
			elif self.x<self.desired:
				self.x+=dt
				self.canvas.blit(self.sprite[math.ceil(self.x/13)%4],(self.x,self.y))
				


