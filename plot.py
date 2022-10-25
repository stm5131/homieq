import pygame
import pandas as pd
import math



	#Function to plot 'key' in 'data' across in a graph of 'size'----------------
class plot:
	def __init__(self, values,size,key,location,threshold,bg,x_bounds):
		self.values = values
		self.size = size
		self.key = key
		self.location = location
		self.threshold = threshold
		self.bg = bg
		self.x_bounds = x_bounds
	def drawplot(self,screen):

		#Offset Data Values on Graph
		offset = self.size[1]/2
		scale = 3
		#Defining Surfaces-------------------------------------------------------
		graph = pygame.Surface(self.size)
		font = pygame.font.Font('font/Pixeltype.ttf',30)
		text = font.render(self.key, False, (0,255,0))

		array = []
		graph.fill((50,50,50))

		i=self.x_bounds[0]
		y=0
		#Start at the i'th data entry at 'key', create localized array with data-
		while i < self.x_bounds[1]:
			y = self.values[self.key][i]
			array.append((i,y))
			i+=1

		#Create y_bounds for plotting then reset array to nil--------------------

		y_bounds = (max(array)[1],min(array)[1])
		array = []
		if y_bounds[0]<1:
			y_bounds=(1,1)
		i=self.x_bounds[0]
		y=0
		#Restart Loop for i'th entry in 'key' but for scaled coordinates---------
		while i < self.x_bounds[1]:
			x = ((i)-self.x_bounds[0])*(self.size[1]/(self.x_bounds[1]-self.x_bounds[0]))
			if self.values[self.key][i]>0:
				y = (-offset) + ( ( (self.size[1]*(scale/2.25)*scale) - (scale*(self.values[self.key][i]/y_bounds[0])) * self.size[1] ) )
			else:
				y = (-offset) + ( ( (self.size[1]*(scale/2.25)*scale) - (scale) * self.size[1] ) )
			array.append((x,y))
			i+=1
		#print(array)
		color = ( 255, 255, 0 , 0)
		#print(color)
		#Draw plotted lines------------------------------------------------------
		pygame.draw.lines(graph,color,False,array)

		#Draw Threshold----------------------------------------------------------
		rect = pygame.Surface((self.size[0],3))
		rect.fill((200,200,200))
		y=((-offset)+self.size[1]*2)-((self.threshold/y_bounds[0])*self.size[1])
		x=0
		graph.blit(rect,(x,y))
		graph.blit(text,( 20 , self.size[1]-20 ))
		screen.blit(graph,self.location)
