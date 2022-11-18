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

def format_scheme(scheme_file):
    with open(scheme_file) as f:
    lines = f.readlines()

    start = lines.index('# a b m n err i ip iperr k r rhoa u valid \n')
    scheme = lines[start:][1:-1]

    elec_combos = np.array([scheme[i].split() for i in range(len(scheme))]).astype(float)

    a = np.transpose(elec_combos)[0]
    b = np.transpose(elec_combos)[1]
    m = np.transpose(elec_combos)[2]
    n = np.transpose(elec_combos)[3]

    return a, b, m, n

def run_one_cycle(fn="scheme3d.shm", repeat=65):
    a, b, m, n = format_scheme(fn)
    print("STARTING DIPOLE DIPOLE SCHEME FOR", len(a), "ELECTRODE COMBINATIONS")
    print("Time: ", time.ctime(time.time()))
    print("Estimated time for one cycle: ", round(activation_time*2*len(a)/60), " minutes.")
    print("Repeating cycle every ", repeat, " minutes.")

    start = time()
    run_scheme(a, b, m, n)
    duration = start - time()

    print("FINISHED CYCLE. SLEEPING FOR ", round(repeat - duration/60), "MINUTES.")

    time.sleep(repeat - duration/60)




a=input('If you want to test one electrode combination, press 1. If you want to test one cycle, press 2.') 
 
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
