#!/usr/bin/python

# Imports some Python Date/Time functions
import time
import datetime

# Import requests library
import requests

# Import json library
import json

# Imports the PyOTA library
from iota import Iota
from iota import Address

# Function for checking address balance on the IOTA tangle. 
def checkbalance():

    print("Checking balance")
    gb_result = api.get_balances(address)
    balance = gb_result['balances']
    return (balance[0])

# Function for turning ON/OFF a deCONZ device using the deCONZ REST API
# id is the deCONZ device ID
# state = True or False (True = Turn device ON, False = Turn device OFF)
def light(id, state):
    url = deconz_ip + '/api/' + deconz_key + '/lights/' + id + '/state'
    data = { 'on': state }
    r = requests.put(url, data=json.dumps(data))
    print(r.text)

# Specify IP address for your deCONZ server
deconz_ip = 'http://localhost:80'

# Specify deCONZ API key
# See "https://dresden-elektronik.github.io/deconz-rest-doc/getting_started/" on how to
# get your API key
deconz_key = 'D1E67BB18B'

# URL to IOTA fullnode used when checking balance
iotaNode = "https://nodes.thetangle.org:443"

# Create an IOTA object
api = Iota(iotaNode, "")

# IOTA address to be checked for new light funds 
# IOTA addresses can be created using the IOTA Wallet
address = [Address(b'NYZBHOVSMDWWABXSACAJTTWJOQRPVVAWLBSFQVSJSWWBJJLLSQKNZFC9XCRPQSVFQZPBJCJRANNPVMMEZQJRQSVVGZ')]

# Get current address balance at startup and use as baseline for measuring new funds being added.   
currentbalance = checkbalance()
lastbalance = currentbalance

# Define some variables
lightbalance = 0
balcheckcount = 0
lightstatus = False

# Assign deCONZ device ID
device_id = 2

# Main loop that executes every 1 second
while True:
    
    # Check for new funds and add to lightbalance when found.
    if balcheckcount == 10:
        currentbalance = checkbalance()
        if currentbalance > lastbalance:
            lightbalance = lightbalance + (currentbalance - lastbalance)
            lastbalance = currentbalance
        balcheckcount = 0

    # Manage light balance and light ON/OFF
    if lightbalance > 0:
        if lightstatus == False:
            print("light ON")
            light(device_id, True) # Turn deCONZ device ON
            lightstatus=True
        lightbalance = lightbalance -1       
    else:
        if lightstatus == True:
            print("light OFF")
            light(device_id, False) # Turn deCONZ device OFF
            lightstatus=False
 
    # Print remaining light balance     
    print(datetime.timedelta(seconds=lightbalance))

    # Increase balance check counter
    balcheckcount = balcheckcount +1

    # Pause for 1 sec.
    time.sleep(1)