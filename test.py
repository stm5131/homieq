import pygame

import math
import sys
import os
import time

import pandas as pd
import random

from plot import *
from metric import *
from sensor import *


delay = 10 #In Seconds
sample_rate = 0.1 #In hertz




i, read, start_delay = 0,0,0
pygame.init()

res = (800,400)
refresh = 60
screen = pygame.display.set_mode(res)
clock = pygame.time.Clock()

font = pygame.font.Font('font/Pixeltype.ttf',50)
bigfont = pygame.font.Font('font/Pixeltype.ttf',150)
bg = pygame.image.load('graphics/map.png').convert()
splash = pygame.image.load('graphics/splash.png').convert()
desired = 400

dark = pygame.Surface((800,400))
screen.blit(pygame.transform.scale(splash,res),(0,0))
pygame.display.update()
time.sleep(0.5)

dark.set_alpha(255)
dark.fill((0,0,0))
screen.blit(dark,(0,0))
text = bigfont.render("SIMIEQ STARTING", False, (0,255,255))
screen.blit(text,(35,175))
pygame.display.update()
time.sleep(0.5)
clock = pygame.time.Clock()


myagent = agent(delay,sample_rate)
sensors = sensor()
player = actor(400,216)

q_delay = 0
mouse_pos = 0
touch = 0
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		elif event.type == pygame.MOUSEBUTTONDOWN and event.button:
			mouse_pos = pygame.mouse.get_pos()
			touch = True
		elif event.type == pygame.MOUSEBUTTONUP and event.button:
			mouse_pos = (0,0)
			touch = False
	#print(str(i) + " seconds have passed since agent update")
	dt = clock.tick(refresh) * 0.001 * 60

	screen.blit(pygame.transform.scale(bg,res),(0,0))

	if i < 5:
		if i >= read:
			read+=1
			sensors.dummy_sensor_read()
		i+=(1/refresh)*dt
	else:
		sensors.dummy_sensor_read()
		myagent.update(sensors.s_data)
		myagent.comfort_check()
		myagent.calc()

		i=0
		read=0

	if start_delay > 15:
		length = len(myagent.sensor_metrics)
		start = length-10
		if start < 0:
			start = 0
		
		t_graph = plot(myagent.sensor_metrics,(150,115),'Temperature',(0,0),25,(0,0,0),(start,length))
		rh_graph = plot(myagent.sensor_metrics,(150,115),'Humidity',(150,0),60,(0,0,0),(start,length))
		co2_graph = plot(myagent.sensor_metrics,(150,115),'CO2',(300,0),800,(0,0,0),(start,length))
		pm_graph = plot(myagent.sensor_metrics,(150,115),'PM25',(450,0),25,(0,0,0),(start,length))

		t_graph.drawplot(screen)
		rh_graph.drawplot(screen)
		co2_graph.drawplot(screen)
		pm_graph.drawplot(screen)

	else:
		start_delay+=(1/refresh)*dt

	

	
	

	if(player.noevent):
		player.idle_update(dt, screen)
		if(any(myagent.flags)):
			player.noevent=False
	if(q_delay<=0):
		player.ask_event(dt,screen,myagent.flags, mouse_pos, touch)
		if(player.noevent):
			q_delay=20
	pygame.display.update()
	q_delay-=1*(1/60)*dt



