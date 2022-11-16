import pygame

import math
import sys
import os
import time

import pandas as pd
import random
import numpy as np

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
player = actor(400,216,screen)

q_delay = 0
mouse_pos = 0
touch = 0


player.state=1
occupied_time = 0

while player.state>0:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		elif event.type == pygame.MOUSEBUTTONDOWN and event.button:
			mouse_pos = pygame.mouse.get_pos()
			touch = False
		elif event.type == pygame.MOUSEBUTTONUP and event.button:
			touch = True
		keys = pygame.key.get_pressed()
	#print(str(i) + " seconds have passed since agent update")
	dt = clock.tick(refresh) * 0.001 * 60

	screen.blit(pygame.transform.scale(bg,res),(0,0))

	player.initial_convo(dt,mouse_pos,touch)
	pygame.display.update()
	if player.is_occupied:
		player.is_occupied=False
		occupied_time=120

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		elif event.type == pygame.MOUSEBUTTONDOWN and event.button:
			mouse_pos = pygame.mouse.get_pos()
			touch = False
		elif event.type == pygame.MOUSEBUTTONUP and event.button:
			touch = True
		keys = pygame.key.get_pressed()
	#print(str(i) + " seconds have passed since agent update")
	dt = clock.tick(refresh) * 0.001 * 60

	screen.blit(pygame.transform.scale(bg,res),(0,0))

	if i < 120:
		if i >= read:
			read+=1
			#sensors.dummy_sensor_read()
			#sensors.control_sensor(dt,keys)
		i+=(1/refresh)*dt
	else:
		sensors.dummy_sensor_read(occupied_time)
		#sensors.control_sensor(dt,keys)
		myagent.update(sensors.s_data)
		myagent.comfort_check()
		myagent.calc()

		i=0
		read=0

	if start_delay >= 7:
		length = len(myagent.sensor_metrics)
		start = length-60
		if start < 0:
			start = 0

		if i < 20:
			if i >= read:
				read+=1
				#sensors.dummy_sensor_read()
				#sensors.control_sensor(dt,keys)
			i+=(1/refresh)*dt
		else:
			sensors.dummy_sensor_read(occupied_time)
			#sensors.control_sensor(dt,keys)
			myagent.update(sensors.s_data)
			myagent.comfort_check()
			myagent.calc()
			i=0
			read=0

		t_graph = plot(myagent.sensor_metrics,(133,115),'Temperature',(0,0),myagent.limits.temp_offset[0],myagent.limits.temp_size[0],(0,0,0),(start,length)," C")
		rh_graph = plot(myagent.sensor_metrics,(133,115),'Humidity',(133,0),myagent.limits.hum_offset[0],myagent.limits.hum_size[0],(0,0,0),(start,length)," %")
		co2_graph = plot(myagent.sensor_metrics,(134,115),'CO2',(266,0),myagent.limits.co2[0],0,(0,0,0),(start,length)," ppm")
		pm_graph = plot(myagent.sensor_metrics,(133,115),'PM25',(400,0),myagent.limits.pmhigh[0],0,(0,0,0),(start,length)," ug/m3")
		sound_graph = plot(myagent.sensor_metrics,(133,115),'Audio',(533,0),myagent.limits.sound[0],0,(0,0,0),(start,length)," dB")
		light_graph = plot(myagent.sensor_metrics,(134,115),'Light',(666,0),myagent.limits.light[0],0,(0,0,0),(start,length)," lux")

		if(player.state == 0):
			t_graph.drawplot(screen)
			rh_graph.drawplot(screen)
			co2_graph.drawplot(screen)
			pm_graph.drawplot(screen)
			sound_graph.drawplot(screen)
			light_graph.drawplot(screen)
		if start_delay < 120:
			start_delay+=(1/refresh)*dt
		else:
			start_delay=10

	else:
		if i < 2:
			if i >= read:
				read+=1
				#sensors.dummy_sensor_read()
				#sensors.control_sensor(dt,keys)
			i+=(1/refresh)*dt
		else:
			sensors.dummy_sensor_read(occupied_time)
			#sensors.control_sensor(dt,keys)
			myagent.update(sensors.s_data)
			myagent.comfort_check()
			myagent.calc()

			i=0
			read=0		
		start_delay+=(1/refresh)*dt
		load = pygame.Surface((460,70))
		load.fill((50,50,50))
		screen.blit(load,(20,30))

		load = pygame.Surface((start_delay*65,60))
		load.fill((100,100,150))
		screen.blit(load,(25,35))
		screen.blit(font.render("Initializing Sensors",False,(100,255,100)),(50,50))
	#screen.blit(font.render("Selected "+str(sensors.select),False,(100,255,100)),(50,350) )
	#print(player.noevent)
	if(player.state<1):
		player.idle_update(dt, screen)
		if(start_delay >= 7):
			#print("Delay Ready")
			#print(myagent.flags)
			if (np.any(myagent.flags)):
				player.state=1
				#print("Question State Thrown")
		#sensors.s_data.Answer = " "
		#sensors.s_data.Trigger = False
		if(player.is_occupied):
			occupied_time=120
			player.is_occupied=False
		else:
			if(occupied_time>0):
				occupied_time-=(1/60)*dt
			else:
				player.state=1
	elif(occupied_time<=0):
		#First Occupancy Check
				player.occupancy_check(dt, mouse_pos, touch)
				print("Checking Occupancy")


	if(occupied_time>0):
		#myagent.sensor_metrics.realtime.trigger = True
		player.ask_event(dt,myagent.flags, mouse_pos, touch)
		if(player.state==3):
			#sensors.s_data.realtime.answer = "Yes"
			if(np.any(myagent.flags.highco2) or np.any(myagent.flags.dangerco2)):
				co2_graph = plot(myagent.sensor_metrics,(400,175),'CO2',(50,0),myagent.limits.co2[0],1,(0,0,0),(start,length)," ppm")
				co2_graph.drawplot(screen)

			elif(np.any(myagent.flags.highpm) or np.any(myagent.flags.dangerpm)):
				pm_graph = plot(myagent.sensor_metrics,(400,175),'PM25',(50,0),myagent.limits.pmhigh[0],1,(0,0,0),(start,length)," ug/m3")
				pm_graph.drawplot(screen)

			elif(np.any(myagent.flags.ishot) or np.any(myagent.flags.iscold)):
				t_graph = plot(myagent.sensor_metrics,(400,175),'Temperature',(50,0),myagent.limits.temp_offset[0],myagent.limits.temp_size[0],(0,0,0),(start,length)," C")
				t_graph.drawplot(screen)

			elif(np.any(myagent.flags.ishumid) or np.any(myagent.flags.isdry)):
				rh_graph = plot(myagent.sensor_metrics,(400,175),'Humidity',(50,0),myagent.limits.hum_offset[0],myagent.limits.hum_size[0],(0,0,0),(start,length)," %")
				rh_graph.drawplot(screen)
		elif(player.state==2):
				if(player.npressed):
					if np.any(myagent.flags.ishot):
						myagent.limits.temp_size[0]+=0.1
					elif np.any(myagent.flags.iscold):
						myagent.limits.temp_size[0]+=0.1
						myagent.limits.temp_offset[0]-=0.1
					#sensors.s_data.realtime.answer = "No"
		#elif(player.state==1):
				#if(player.npressed):
					#sensors.s_data.Answer = "No"
	
	#screen.blit(font.render("Occupied Time " + str(round(occupied_time,2)) + ", Is Occupied " + str(player.is_occupied),False,(100,255,100)),(50,350))
	pygame.display.update()



