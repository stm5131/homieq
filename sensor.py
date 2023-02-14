import math
import random
import pandas as pd
import pygame
import time
import time
import colorsys
import os
import sys
import ST7735
from digitalio import DigitalInOut, Direction, Pull
from adafruit_pm25.uart import PM25_UART
import serial
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.25)
try:
    # Transitional fix for breaking change in LTR559
    from ltr559 import LTR559
    #ltr559 = LTR559()
except ImportError:
    import ltr559
import board
import adafruit_scd4x

reset_pin = DigitalInOut(board.G0)
reset_pin.direction = Direction.OUTPUT
reset_pin.value = False
from bme280 import BME280



#Sensor Acquisition object
class Sensor:
    def __init__(self):
        self.t_sen = 25
        self.rh_sen = 55
        self.p_sen = 1000
        self.co2_sen = 450
        self.pm = 2
        self.light = 0
        self.audio = 0
        self.s_data = 0
        self.select = 0
        self.key=False
        self.bme280=BME280()
        self.ltr559 = LTR559()
        self.i2c = board.I2C()  # uses board.SCL and board.SDA
        self.scd4x = adafruit_scd4x.SCD4X(self.i2c)
        self.pm25_uart = PM25_UART(uart, reset_pin)
        #Initialize sensors

    def sensor_read(self):
        self.t_sen = self.bme280.get_temperature()
        self.rh_sen = self.bme280.get_humidity()
        self.p_sen = self.bme280.get_pressure()
        self.co2 = self.scd4x.CO2
        self.light = self.ltr559.get_lux()
        return self.update_df()
    def dummy_sensor_read(self):
        #Collect sensor data
        #Semi Random sensor generation for testing
        #Testing Data
        #time.sleep(1) # Simulate I/O Delay
        self.t_sen += 0.05*random.randrange(-1,1)
        if self.t_sen<18:
            self.t_sen=18
        elif self.t_sen>25:
            self.t_sen=24
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
        return self.update_df()
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
        return self.update_df()
        
        #print(self.s_data)
    def update_df(self):
        self.s_data = pd.DataFrame({
            "Temperature":[self.t_sen],
            "Humidity":[self.rh_sen],
            "Pressure":[self.p_sen],
            "CO2":[self.co2_sen],
            "Light":[self.light],
            "PM25":[self.pm],
            "Audio":[self.audio]
            })
        return self.s_data
