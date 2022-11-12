# create ohmpi object
import os
import numpy as np
import time
os.chdir("/home/pi/OhmPi")
from ohmpi import modified_ohmpi

#todo: figure out output filenames for data

import sys
filename = sys.argv[1]

if filename:
    pass
else:
    filename = "scheme.csv" # MAKE SURE TO CHANGE THIS DEDFAULT FILE TO CSV ON RASPBERRY PI

def run():
    ### Define object from class OhmPi
    k = OhmPi(use_mux=True)

    ### Update settings if needed 
    k.update_settings({"injection_duration":0.2})
    k.load_sequence(filename) # load sequence

    # run test on first electrode combinaion
    import pandas as pd
    df = pd.read_csv(filename)
    k.run_measurement_time_domain(list(df.iloc[0]))

    # run whole sequence from input file (if none given, use default) and save data
    k.run_sequence_time_domain()

def do_one_combo(combination):
        k = OhmPi(use_mux=True)

    ### Update settings if needed 
    k.update_settings({"injection_duration":0.2})
    k.load_sequence(combination) # load sequence
    k.run_measurement_time_domain(list(df.iloc[0]))

def get_contact_resistances():

    ### Define object from class OhmPi
    k = OhmPi(use_mux=True)

    ### Update settings if needed 
    k.update_settings({"injection_duration":0.2})
    

    # run test on first electrode combinaion
    import pandas as pd
    df = pd.read_csv(filename)
    k.rs_check()

    k.load_sequence(filename) # load sequence

    # run whole sequence from input file (if none given, use default) and save data
    k.rs_check()

    
