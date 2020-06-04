# Integrating physical devices with IOTA — Zigbee edition

## The 15th part in a series of beginner tutorials on integrating physical devices with the [IOTA](https://medium.com/coinmonks/iota/home) protocol

![img](https://miro.medium.com/max/2448/1*-d1smIJ93wtJHvaAaNQ8sQ.jpeg)

------

## Introduction

This is the 15th part in a series of beginner tutorials where we explore integrating physical devices with the [IOTA protocol](https://medium.com/coinmonks/iota/home). As promised in the [previous tutorial](https://medium.com/coinmonks/integrating-physical-devices-with-iota-philips-hue-edition-19eec4f28ef6); this time, instead of integrating our IOTA payment system on top of the proprietary and closed source Phillips Hue system, we will now take the same idea and apply it on top of the open source Zigbee hardware and software platform.

*Note!*
*Notice that the Phillips Hue system is also based on the Zigbee protocol, so any Hue devices that you may already own should work fine with this tutorial.*

*Note!
I suggest you browse trough the* [*first*](https://medium.com/coinmonks/integrating-physical-devices-with-iota-83f4e00cc5bb) *and* [*fourteenth*](https://medium.com/coinmonks/integrating-physical-devices-with-iota-philips-hue-edition-19eec4f28ef6) *tutorial in this series before continuing as they will provide some additional context to the general use case and what we are trying to accomplish in this tutorial.*

------

## The use case

So, why would our hotel owner want to implement his IOTA payment system on top of the open source Zigbee protocol vs the closed source Phillips Hue system as we discussed in the [previous tutorial](https://medium.com/coinmonks/integrating-physical-devices-with-iota-philips-hue-edition-19eec4f28ef6)? Well, i think there are several reasons:

1. Flexibility
   He is no longer constrained to only using smart devices from Phillips. He can now purchase and combine any Zigbee supported smart device from any vendor, such as the popular [IKEA TRÅDFRI](https://www.ikea.com/gb/en/cat/smart-lighting-36812/)
2. Cost
   Phillips Hue devices are pretty expensive compared other vendors.
3. Simplicity I
   He no longer needs a separate Hue bridge as any computer inside his local network may function as the bridge (in my case i’m using an old Raspberry PI with a defect HDMI output)
4. Simplicity II
   There is no longer any need for a separate computer running the IOTA Python code as he can now use his existing bridge computer.
5. Customization
   All software used in this tutorial is open source and could be customized and adapted to his particular use case.

------

## About deCONZ

[deCONZ](https://phoscon.de/en/conbee/software#deconz) is the open source and free to use “bridge” software running on the bridge computer. [deCONZ](https://phoscon.de/en/conbee/software#deconz) functions as the communication backbone of your new Zigbee network, providing a graphical overview of your Zigbee devices and connections. [deCONZ](https://phoscon.de/en/conbee/software#deconz) also provides a REST API that we will use to control our individual Zigbee devices using Python.

![img](https://miro.medium.com/max/1257/1*JAQ5MQgHLyaetqUXBPDHnQ.png)

------

## About Phoscon

[Phoscon](https://phoscon.de/en/conbee/software#phoscon-app) is the web-based user interface that comes with deCONZ. [Phoscon](https://phoscon.de/en/conbee/software#phoscon-app) is a user friendly UI for managing your individual Zigbee devices, grouping devices, managing scenes etc.

![img](https://miro.medium.com/max/1097/1*_C-8i50JcJA84alTIM-quQ.png)

------

## The components

Beside the bridge computer itself, we also need a hardware module (gateway) capable of communicating over the Zigbee protocol.

There are currently two alternative hardware modules compatible with deCONZ. The [RaspBee gateway for Raspberry PI](https://phoscon.de/en/raspbee) and the [ConBee universal USB gateway](https://phoscon.de/en/conbee2/). You should be able to get them both off Amazon or Ebay for about 40 USD.

![img](https://miro.medium.com/max/359/1*b89Qaq69bW4f4hxwbL8sfQ.jpeg)

*Note!*
*In my version of the project I’m using the RaspBee module. However, i guess the ConBee USB gateway is more flexible as it can be used with any USB enabled computer, including the Raspberry PI.*

*Note!*
*The RaspBee module has a very small form factor and will fit inside most standard PI casings.*

------

## Installing RaspBee/ConBee, deCONZ and Phoscon

When i first received my RaspBee module i tried setting it up using the installation guidelines that came with the module. This was not a very pleasant experience as the documentation was pretty bad and outdated. After struggling with the setup for some time i came across [this](https://flemmingss.com/how-to-set-up-deconz-and-phoscon-on-a-raspberry-pi-and-control-all-your-zigbee-devices/) tutorial published by *flemming* on his blog. Using this [excellent tutorial](https://flemmingss.com/how-to-set-up-deconz-and-phoscon-on-a-raspberry-pi-and-control-all-your-zigbee-devices/) i had everything up and running in a few minutes.

*Note!*
*If using a Raspberry PI as the bridge computer, I highly recommend you ignore the installation guide that came with your ConBee/RaspBee and use flemmings tutorial instead. This will save you a lot of time and frustration.*

*Note!
You will find additional versions of RaspBee SD card images for the Raspberry PI* [*here*](https://phoscon.de/en/conbee/sdcard)

------

## Assigning IOTA addresses to Zigbee devices

Once you have your all your Zigbee devices up and running with deCONZ. The next step is to assign a unique [IOTA](https://medium.com/coinmonks/iota/home) payment address to each individual device. The simplest way of creating new [IOTA](https://medium.com/coinmonks/iota/home) addresses (including QR codes) is using the Trinity wallet. Make a note of each address as we will need them in our Python script(s) later on.

Next, print the QR code for each address on a piece of paper and attach it to, or place it next to its respective physical Zigbee device.

------

## Required Software and libraries

Before we move on to the Python code for this project we need to make sure that all required dependencies and libraries are installed. In my setup the bridge computer will also be running the Python code that interacts with the IOTA tangle and the deCONZ REST API. This means that the following additional Python libraries must be installed on the bridge computer:

The [PyOTA library](https://github.com/iotaledger/iota.py), The Python [json library](https://pypi.org/project/jsonlib/) and the Python [requests library](https://pypi.org/project/requests/).

------

## The Code

Now that we have made all the preparations, let’s look at the Python code for this project.

The Python script we are using for this project is basically the same as we used for the [first tutorial](https://medium.com/coinmonks/integrating-physical-devices-with-iota-83f4e00cc5bb) with some minor adjustments. Notice that there are no longer any references to the Raspberry PI GPIO pins or library, which means that we now can run the Python script(s) from any computer inside the local network.

The Python script(s) are basically just checking the balance for each IOTA address (created in a previous step) every 10 sec. As new funds are being added to an address, the script simply turns ON it’s associated deCONZ device using a deCONZ REST API call. As time passes, the script continually removes time from a local device balance, switching the device OFF (again with an API call) when the balance is empty.

*Important!
Check the* [*deCONZ REST API — Getting Started*](https://dresden-elektronik.github.io/deconz-rest-doc/getting_started/) *page for more information on obtaining your deCONZ* **API key** *together with unlocking your deCONZ gateway to accept incoming API requests.*

*Note!
Notice that when turning ON/OFF a device we need to provide a device ID with the API call. Check the* [*deCONZ REST API — Getting Started*](https://dresden-elektronik.github.io/deconz-rest-doc/getting_started/) *page for more information on how to get the device ID for each individual device in your Zigbee network.*

And here is our Python script for checking balances on the IOTA tangle and turning ON/OFF individual Zigbee devices.

```python
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
```

You can download the script from [here](https://gist.github.com/huggre/0b69ee1242e5a4a2b018afdafc1388d0)

------

## Running the project

To run the project, you first need to save the script in the previous section as a text file on your computer.

Notice that Python program files uses the .py extension, so let’s save the file as **pay_the_light_zigbee_dev2.py**
*(\*_dev2.py* referring to the particular deCONZ device id being controlled by the script)

Next, we need to make some minor adjustments to the script:

1. Replace the IOTA payment address with the address you created for this particular device id earlier in this tutorial.
2. Update the device_id variable according to the particular deCONZ device you are targeting (unless the id=2, then no need to change)

To execute the script, simply start a new terminal window, navigate to the folder where you saved *pay_the_light_zigbee_dev2.py* and type:

**python pay_the_light_zigbee_dev2.py**

You should now see the code being executed in your terminal window, displaying the current light balance for device 2, and checking the devices’s IOTA address balance for new funds every 10 seconds.

------

## Pay the light

To turn on a particular Zigbee device, simply take your mobile phone with the Trinity wallet, scan the associated QR code for the device and transfer some IOTA’s to its IOTA address. As soon as the transaction is confirmed by the IOTA tangle, the device should turn ON and stay on until the balance is empty, depending on the amount of IOTA’s you transferred. In my example I have set the IOTA/device time ratio to be 1 IOTA for 1 second of service.

------

## Managing multiple Zigbee devices

If you take a look at the Python script for this tutorial you will notice that the script itself is not prepared for managing multiple Zigbee devices simultaneously. I guess the appropriate way of dealing with this would be to re-write the code to include some type of device list or array that would allow us to manage multiple devices in parallel. Another alternative is of course (as i did) to simply have multiple instances of Python running at the same time. Each instance running its own script with its own device id/IOTA address.

Feel free to make a pull request in the github repository below if you want to take on the challenge of re-writing the script to support multiple devices in parallel.

------

## Contributions

If you would like to make any contributions to this tutorial you will find a Github repository [here](https://github.com/huggre/pay_the_light_zigbee)

------

## Whats next?

In the next tutorial i was thinking we could look in to a totally different subject, namely using IOTA and the IOTA Tangle for tracking and tracing goods in a supply chain context. Here we will play around with bar-coding and bar-code scanners. Stay tuned.

------

## Donations

If you like this tutorial and want me to continue making others, feel free to make a small donation to the IOTA address below.

![img](https://miro.medium.com/max/382/0*Pa7JYU6t_co3M3eE.png)

NYZBHOVSMDWWABXSACAJTTWJOQRPVVAWLBSFQVSJSWWBJJLLSQKNZFC9XCRPQSVFQZPBJCJRANNPVMMEZQJRQSVVGZ
