#HomIEQ Visual Engine Version 0.1
#Steven Tanner McCullough
#Code to manage and run the visual aspects of this device.
#Library Import
import pygame

#Internal Library import
from sensor import *
from agent import *
from gui import *
from player import *
from plot import *



#Custom Functions
#Define timer object to keep time-----------------------------------------------
class Timer:
	def __init__(self,length):
		self.i=0
		self.length=length
		self.lapsed=False
		self.time = [0,0,0] #To record Runtime to data, [seconds,minutes,hours]
		self.logic = [0,0,0] #To be used for logic timing, [ticks,seconds,minutes]
	def update_time(self,dt):
		if(self.lapsed):
			self.lapsed=False
			print("Timer has reset")
			#60ticks/s
		#Count Ticks
		if(self.logic[0]<60):
			self.logic[0]+=dt
			#60ticks/s
		else:
			#Increase second count every 60 ticks
			#Reset Tick counter
			self.logic[0]=0
			#Increase second count
			if(self.logic[1]<60):
				self.logic[1]+=1 #Increase second count
				self.time[0]+=1 #Increase second count
			else:
				self.logic[1]=0 #Reset second count at 1 minute
				self.time[0]=0 #Reset second count at 1 minute

				#If logic timer is less than set tigger time than increase
				#Once trigger time is met, bool is triggered
				if(self.logic[2]<self.length):
					
					self.logic[2]+=1 #Increase minute count
					#print(self.logic[2])
				else:
					self.logic[2]=0 #Reset minute count at specified length
					self.lapsed=True
					print("Timer has lapsed")

				if(self.time[1]<60):
					self.time[1]+=1 #Increase minute count
				else:
					self.time[1]=0 #Reset minute count at 1 hour


					self.time[2]+=1 #Increase Hour count every 60 Minutes

#-------------------------------------------------------------------------------
#Defining Variables and Objects
timer =  Timer(1)
clock = pygame.time.Clock()
pygame.init()
res=(800,400)
screen = pygame.display.set_mode(res)

splash = pygame.image.load('graphics/splash.png').convert()
screen.blit(pygame.transform.scale(splash,res),(0,0))
pygame.display.update()

bg = pygame.transform.scale(pygame.image.load('graphics/map.png').convert(),res)

dark = pygame.Surface(res)
screen.blit(pygame.transform.scale(splash,res),(0,0))
time.sleep(0.5)
pygame.display.update()
dark.set_alpha(255)
dark.fill((0,0,0))
screen.blit(dark,(0,0))
bigfont = pygame.font.Font('font/Pixeltype.ttf',75)
text = bigfont.render("HomIEQ initializing...", False, (255,255,255))
screen.blit(text,(25,300))

pygame.display.update()

player = Player(screen)
sensor = Sensor()
agent = Agent()
player.state=1
player.subject=0

i=0
while(i<200):
	#Run Ingame Clock for event capture and visual logic
	dt = clock.tick(60) * 0.001 * 60

	#Run logical and Datakeeping clock for time
	timer.update_time(dt)

	agent.update(sensor.sensor_read())
	agent.comfort_check()
	agent.calc()
	i+=dt
	#print(sensor.s_data)
	dark.fill((255,255,255))
	screen.blit(pygame.transform.scale(dark,(int(i*1.5),50)),(500,300))
	pygame.display.update()
#print(agent.sensor_metrics)

compiled_df=pd.DataFrame()

while(True):
	#Run Ingame Clock for event capture and visual logic
	dt = clock.tick(60) * 0.001 * 60

	#Run logical and Datakeeping clock for time
	timer.update_time(dt)

	#Send Background pixels to screen
	screen.blit(pygame.transform.scale(bg,res),(0,0))

	#If timer lapses, then logic performs its tasks once
	if(timer.lapsed):
		agent.update(sensor.sensor_read())
		time.sleep(0.25)
		print("sleepy")
		agent.calc()
		agent.comfort_check()
		
		compiled_df = pd.concat([compiled_df , parse_to_df(sensor.s_data,agent.limits,
			timer.time[2],timer.time[1],player.response_given)] , ignore_index=True)
		#print(compiled_df)
		compiled_df.to_csv("output.csv")
		player.response_given=0
		#print(agent.conversation)
		if player.state==1:
			player.state=0
		if agent.conversation>0:
			player.subject=agent.conversation
			print(player.subject)
			agent.conversation=0
			player.state=1

		

	#For loop used to search through events for keyboard presses
	#Also works to grab mouse and touch clicks and presses
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

	length = len(agent.sensor_metrics)
	#print(length)
	start = length-60
	if start < 0:
		start = 0

	t_graph = plot(agent.sensor_metrics,(133,115),'Temperature',(0,0),agent.limits.temp_offset[0],agent.limits.temp_size[0],(0,0,0),(start,length)," C")
	rh_graph = plot(agent.sensor_metrics,(133,115),'Humidity',(133,0),agent.limits.hum_offset[0],agent.limits.hum_size[0],(0,0,0),(start,length)," %")
	co2_graph = plot(agent.sensor_metrics,(134,115),'CO2',(266,0),agent.limits.co2[0],0,(0,0,0),(start,length)," ppm")
	pm_graph = plot(agent.sensor_metrics,(133,115),'PM25',(400,0),agent.limits.pmhigh[0],0,(0,0,0),(start,length)," ug/m3")
	sound_graph = plot(agent.sensor_metrics,(133,115),'Audio',(533,0),agent.limits.sound[0],0,(0,0,0),(start,length)," dB")
	light_graph = plot(agent.sensor_metrics,(134,115),'Light',(666,0),agent.limits.light[0],0,(0,0,0),(start,length)," lux")
	if(player.state == 0):
		t_graph.drawplot(screen)
		rh_graph.drawplot(screen)
		co2_graph.drawplot(screen)
		pm_graph.drawplot(screen)
		sound_graph.drawplot(screen)
		light_graph.drawplot(screen)

	player.update(dt)
	pygame.display.update()
