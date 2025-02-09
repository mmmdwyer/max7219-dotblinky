import dotblinky
import math
import time
import network
import json
import requests
import config


n = network.WLAN(network.STA_IF)
n.active(True)
n.connect(config.wifi, config.wifipw)
while n.isconnected() == False:
    print('Waiting for connection...')
    time.sleep(1)
print(n.ifconfig())


def getenergy():
    res = requests.get(config.url)
    if res.status_code == 200:
        j = res.json()
        current = round(j["StatusSNS"]["ENERGY"]["Current"],3)
        power =  j["StatusSNS"]["ENERGY"]["Power"]
        volts =  j["StatusSNS"]["ENERGY"]["Voltage"]
        print(f"{current}A @ {volts}V = {power}W")
    else:
        print(res.status_code)
        print(res.text)
    
d = dotblinky.Dotblinky()


# This makes a sinewave for graph demos
data = []
for i in range(128):
    data.extend([math.sin(i/2)*50+50])

# Show a moving line, then bar graph
for i in range(20):
    d.linegraph(data[i:], fill=False)
    d.update()
    time.sleep(.1)
d.blank()    
for i in range(20):
    d.linegraph(data[i:], fill=True)
    d.update()
    time.sleep(.1)

# WOPR mode (random blinky lights)
for i in range(20):
    d.wopr()
    d.update()
    time.sleep(.1)
for i in range(20):
    d.wopr(density=3)
    d.update()
    time.sleep(.1)

# Text
d.text("Welcome!")
d.update()
time.sleep(1)

d.text("WARNING!",invert=True)
d.update()
time.sleep(1)

# Bitslide mode (moving random)
for i in range(150):
    d.bitslide()
    d.update()
    time.sleep(.01)
d.blank()
for i in range(150):
    d.bitslide(direction=2, density=5)
    d.update()
    time.sleep(.01)

# Barberpole stripes
for i in range(250,0,-1):
    d.stripes(offset=i)
    d.update()

# Bargraph
for i in range(20):
    d.onebar(data[i])
    d.update()
    time.sleep(.5)

nextthink = time.ticks_ms() + 10000
while True:
    if time.ticks_ms() > nextthink:
        nextthink = time.ticks_ms() + 10000
        getenergy()
    d.bitslide(density=5)
    d.update()
    time.sleep(.01)
    
