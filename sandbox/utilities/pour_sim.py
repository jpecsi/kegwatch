# ========== IMPORT ========== #
import json
import requests
import sys,getopt
import random
from datetime import datetime
import time
# ============================ #





# ========== FUNCTIONS ========== #
# Log a pour
def pour_beer(t,n):
    # Status message
    print("[TAP " + str(t) + "] Simulating " + str(n) + " pours...")
    
    # Generate pours
    for p in range(n):
        # Random amount
        o = random.uniform(2.00,15.99)

        # Log the pours
        pour = {
            'time': str(datetime.now()),
            'tap_id': t,
            'oz_poured': o,
            'consumer': consumer
        }

        # Log it
        r = requests.post(url=API_URL+"beer",json=pour)
        if r.text:
            print("[TAP " + str(t) + "] API Response: " + r.text)
    
        # Get status
        confirmation = check_keg(t)
        print("[TAP " + str(t) + "] Poured: " + str(o) + " oz. | Remaining: " + check_keg(t))

        # Pause
        time.sleep(1)


# Validate the tap is active
def validate_tap(t):
    # Keg status
    active = False

    # Get the list of active kegs
    kegs = (requests.get(url=API_URL+"kegs",params="")).json()
    
    # See if the requested keg is active
    for k in kegs:
        if k['tap'] == t:
          active = True
          print("[TAP " + str(t) + "] Beer found: " + k['name'])  
          
    # Return the result
    return active


# Get remaining beer
def check_keg(t):
    # Result variable
    result = 0

    # Get the active kegs
    kegs = (requests.get(url=API_URL+"kegs",params="")).json()
    
    # Get the data we need...
    for k in kegs:
        if k['tap'] == t:
            result = k['remaining']

    return str(result)

# =============================== #





# ========== MAIN ========== #
# Configs
API_URL = "http://192.168.1.2:8080/"

# Parameters for simulation
tap = 0
count = 0
consumer = "Pour Simulator"

# Get command line args
argv = sys.argv[1:]
opts,args = getopt.getopt(argv, "t:n:c:")
for opt,arg in opts:
    if opt in ['-t']:
        tap = int(arg)
    elif opt in ['-n']:
        count = int(arg)
    elif opt in ['-c']:
        consumer = arg

# Validate input
if tap == 0 or count == 0:
    print("Invalid! Both (t)ap and (n)umber of pours must be an integer!")
    sys.exit()
elif count > 10:
    print("Number of pours too high! Max of 10, let's not break the thing...")
    count = 10

# Run the sim!
if validate_tap(tap):
    pour_beer(tap,count)
else:
    print("Tap not active!")

# ========================== #