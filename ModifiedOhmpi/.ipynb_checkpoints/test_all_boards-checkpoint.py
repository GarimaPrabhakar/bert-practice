"""
Created on Tue Dec  7 06:39:33 2021 
Code for testing switch MUX for ohmpi 2 
@author: remi.clement 
"""

import time , board, busio,adafruit_tca9548a 
from adafruit_mcp230xx.mcp23017 import MCP23017 
import digitalio
from digitalio import Direction


address_a=0X70# choose the mux board address 
address_b=0X71
address_m=0X72
address_n=0X73

activation_time=1 # choose your activation time in second 


i2c = busio.I2C(board.SCL, board.SDA) #activation du protocle I2C 
def switch_mux_on(electrode,address):
    tca= adafruit_tca9548a.TCA9548A(i2c, address)
    if electrode < 17: 
        nb_i2C=7 
        a=electrode 
    elif electrode > 16 and electrode< 33:     
        nb_i2C=6 
        a=electrode-16 
    elif electrode > 32 and electrode < 49:     
        nb_i2C=5 
        a=electrode-32 
    elif electrode > 48 and electrode < 65:     
        nb_i2C=4 
        a=electrode-48 
               
    mcp2 = MCP23017(tca[nb_i2C]) 
    mcp2.get_pin(a-1).direction=Direction.OUTPUT 
    mcp2.get_pin(a-1).value=True 
  
def switch_mux_off(electrode,address): 
    tca= adafruit_tca9548a.TCA9548A(i2c, address) 
    if electrode < 17: 
        nb_i2C=7 
        a=electrode 
    elif electrode > 16 and electrode < 33:     
        nb_i2C=6 
        a=electrode-16 
    elif electrode > 32 and electrode < 49:     
        nb_i2C=5
        
        a=electrode-32 
    elif electrode > 48 and electrode < 65:     
        nb_i2C=4 
        a=electrode-48 
           
    mcp2 = MCP23017(tca[nb_i2C])      
    mcp2.get_pin(a-1).direction=digitalio.Direction.OUTPUT 
    mcp2.get_pin(a-1).value=False 
 

def run_scheme(a, b, m, n):
    for i in range(len(a)):
        switch_mux_on(a[i],address_a)
        switch_mux_on(b[i],address_b)
        switch_mux_on(m[i],address_m)
        switch_mux_on(n[i],address_n)
        print('electrodes:',a[i], ' ', b[i], ' ', m[i], ' ', n[i],' activate' )
        time.sleep(activation_time)

        switch_mux_off(a[i],address_a)
        switch_mux_off(b[i],address_b)
        switch_mux_off(m[i],address_m)
        switch_mux_off(n[i],address_n)
        print('electrodes:',a[i], ' ', b[i], ' ', m[i], ' ', n[i],' deactivate' )
        time.sleep(activation_time)



a=input(' if vous want try 1 channel choose 1, if you want try all channel choose 2!') 
 
if a=='1': 
    b=0 
    print ("run channel by channel test") 
    electrode=int(input(' Choose your electrode number (integer):')) 
    switch_mux_on(electrode,address) 
    print('electrode:',electrode,' activate' ) 
    time.sleep(activation_time) 
    switch_mux_off(electrode,address) 
    print('electrode:',electrode,' deactivate' ) 
     
if a== '2': 
    for electrode in range(1, 65): 
        switch_mux_on(electrode,address) 
        print('electrode:',electrode,' activate' ) 
        time.sleep(activation_time) 
        switch_mux_off(electrode,address) 
        print('electrode:',electrode,' deactivate' ) 

        time.sleep(activation_time) 

if a not in ['1', '2']: 
    print ("Wrong choice !") 
