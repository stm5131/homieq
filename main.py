import pygame
from sys import exit
import math
import pandas as pd
import random
import time
from plot import *


pygame.init()

res = (800,400)
refresh = 30
screen = pygame.display.set_mode(res, pygame.FULLSCREEN)
clock = pygame.time.Clock()

font = pygame.font.Font('font/Pixeltype.ttf',50)

bigfont = pygame.font.Font('font/Pixeltype.ttf',150)

bg = pygame.image.load('graphics/map.png').convert()
p1 = pygame.image.load('graphics/player/player/s1.png').convert_alpha()
p2 = pygame.image.load('graphics/player/player/w1.png').convert_alpha()
p3 = pygame.image.load('graphics/player/player/w2.png').convert_alpha()
splash = pygame.image.load('graphics/splash.png').convert()

desired = 400
x , y = 400, 216
dark = pygame.Surface((800,400))
screen.blit(pygame.transform.scale(splash,res),(0,0))
pygame.display.update()
data = pd.read_csv('data/out.csv')
#time.sleep(0.5)

dark.set_alpha(255)
dark.fill((0,0,0))
screen.blit(dark,(0,0))
text = bigfont.render("SIMIEQ STARTING", False, (0,0,255))
screen.blit(text,(35,175))
pygame.display.update()
#time.sleep(0.5)


#Counting Variables
t=0
count = 0

#Refresh Clocl object
clock = pygame.time.Clock()

#Input Variables
wait = 1
warning= 0
touch = 0
accept = 0

#Feedback Variables
yes = 0
no = 0



while True:

	dt = clock.tick(refresh) * 0.001 * 60

	y = 216-(abs((dt*math.sin((count*1.5)))*(math.floor(warning/30))*15))
	if(count<len(data)-3):
		count+=0.05*dt
	else:
		count=1
		t=1
	t=math.floor(count)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		elif event.type == pygame.MOUSEBUTTONDOWN and event.button:
			touch = 1

	screen.blit(pygame.transform.scale(bg,res),(0,0))

	if wait>0:
		screen.blit(pygame.transform.scale(p1,(64,128)),(x,y))
		wait-=1*dt
		wait = math.ceil(wait)
		if wait<0:
			wait=0
	elif warning<30:
		text = font.render("Walking", False, (0,255,0))
		screen.blit(text,(625,60))
		if math.fabs(x-desired)<0.4:
			x=desired
			desired = random.randint(100,700)
			screen.blit(pygame.transform.scale(p1,(64,128)),(x,y))
			wait = random.randint(50,100)
		elif x>desired:
			x-=1*dt
			x=math.floor(x)
			if x%40<12:
				screen.blit(pygame.transform.scale(pygame.transform.flip(p2,True,False),(64,128)),(x,y))
			elif x%40>=12 and x%40<20:
				screen.blit(pygame.transform.scale(pygame.transform.flip(p1,True,False),(64,128)),(x,y))
			elif x%40>=20 and x%40<32:
				screen.blit(pygame.transform.scale(pygame.transform.flip(p3,True,False),(64,128)),(x,y))
			elif x%40>=32 and x%40<40:
				screen.blit(pygame.transform.scale(pygame.transform.flip(p1,True,False),(64,128)),(x,y))
		elif x<desired:
			x+=1*dt
			x=math.ceil(x)
			if x%40<12:
				screen.blit(pygame.transform.scale(p2,(64,128)),(x,y))
			elif x%40>=12 and x%40<20:
				screen.blit(pygame.transform.scale(p1,(64,128)),(x,y))
			elif x%40>=20 and x%40<32:
				screen.blit(pygame.transform.scale(p3,(64,128)),(x,y))
			elif x%40>=32 and x%40<40:
				screen.blit(pygame.transform.scale(p1,(64,128)),(x,y))
	else:
		screen.blit(pygame.transform.scale(pygame.transform.flip(p1,True,False),(64,128)),(x,y))
	

	dark.set_alpha((1/20)*math.floor(data.co2[t]))
	dark.fill((0,155,0))
	screen.blit(dark,(0,0))

	dark.set_alpha(200-(3/4)*math.floor(data.light[t]))
	dark.fill((0,0,0))
	screen.blit(dark,(0,0))
	t_graph = plot(data,(150,115),'temperature',(0,0),25,(0,0,0),(round(count),round(count+10)))
	rh_graph = plot(data,(150,115),'humidity',(150,0),60,(0,0,0),(round(count),round(count+10)))
	co2_graph = plot(data,(150,115),'co2',(300,0),800,(0,0,0),(round(count),round(count+10)))
	l_graph = plot(data,(150,115),'light',(450,0),25,(0,0,0),(round(count),round(count+10)))

	#text = font.render("Iteration "+str(t), False, (0,255,0))
	#screen.blit(text,(50,25))
	#text = font.render("CO2 "+str(math.floor(data.co2[t]))+ " ppm", False, (0,255,0))
	#screen.blit(text,(275,25))
	#text = font.render("Temp "+str(math.floor(data.temperature[t]))+" C", False, (0,255,0))
	#screen.blit(text,(525,25))

	#text = font.render("RH "+str(math.floor(data.humidity[t]))+" %", False, (0,255,0))
	#screen.blit(text,(50,60))
	#text = font.render("Light "+str(math.floor(data.light[t]))+" lux", False, (0,255,0))
	#screen.blit(text,(275,60))
	#text = font.render(data.time[t], False, (0,255,0))
	#screen.blit(text,(50,100))
	if warning>30:
		if touch:
			warning = 0
			touch=0
			accept = 15
			yes+=1
		else:
			text = font.render("Do you have a moment? YES | NO", False, (0,0,255))
			screen.blit(text,(150,200))
	else:
		if accept>0:
			accept-=0.1*dt
			text = bigfont.render("Ok!", False, (0,0,255))
			screen.blit(text,(400,200))
		if accept<0.1:
			warning+=0.01*dt
			if(data.light[t]<5):
				#text = bigfont.render("! Low light !", False, 'Red')
				#screen.blit(text,(175,200))
				warning+=0.01*dt
			elif(data.temperature[t]>26):
				#text = bigfont.render("! High Temp !", False, 'Red')
				#screen.blit(text,(175,200))
				warning+=0.01*dt
			elif(data.co2[t]>500):
				#text = bigfont.render("! High CO2 !", False, 'Red')
				#screen.blit(text,(175,200))
				warning+=0.01*dt
				
			elif warning>0:
				warning-=0.01*dt

			elif warning<0:
				warning=0
	text = font.render("Warning " + str(math.floor(warning)), False, (0,255,0))
	screen.blit(text,(50,360))

	text = font.render("Accepted "+str(yes), False, (0,255,0))
	screen.blit(text,(250,360))

	#text = font.render("y "+str(y), False, (0,255,0))
	#screen.blit(text,(450,360))
	

	
	t_graph.drawplot(screen)
	rh_graph.drawplot(screen)
	co2_graph.drawplot(screen)
	l_graph.drawplot(screen)

	pygame.display.update()