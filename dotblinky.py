from machine import Pin, SPI
import max7219
import random
import time

class Dotblinky:
    """Hooks up to a MAX7219 dot matrix display and provides a number of animations and displays"""
    def __init__(self):
        self.spi = SPI(0, 400_000, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
        self.cs = Pin(5, Pin.OUT)
        self.display = max7219.Matrix8x8(self.spi, self.cs, 8)
        self.display.brightness(7)
        self.width=64
        self.height=8
        self.nextthink = time.time_ns()

    def weightedrand(self,density):
        if random.randint(0,100) > density:
            return False
        else:
            return True

    def update(self):
        self.display.show()
        
    def blank(self):
        self.display.rect(0, 0, self.width, self.height, 0, True)

    def wopr(self,density=50):
        for y in range (self.height):
            for x in range (self.width):
                self.display.pixel(x,y,self.weightedrand(density))

    def bitslide(self, direction=0, density=50):
        if direction == 0:
            self.display.scroll(1,0)
            for y in range(8):
                self.display.pixel(0,y,self.weightedrand(density))
        elif direction == 1:
            self.display.scroll(-1,0)
            for y in range(8):
                self.display.pixel((self.width-1),y,self.weightedrand(density))
        elif direction == 2:
            self.display.scroll(0,1)
            for x in range(63):
                self.display.pixel(x,0,random.getrandbits(1))
        elif direction == 3:
            self.display.scroll(0,-1)
            for x in range(63):
                self.display.pixel(x,(self.height-1),random.getrandbits(1))           

    def text(self, string, invert=False):
        self.display.rect(0, 0, self.width, self.height, invert, True)
        self.display.text(string,0,0, not(invert))
        
    def onebar(self, percent, invert=False, label=True):
        if percent > 100:
            percent = 100
        if percent < 0:
            percent = 0
        s = int(percent/100 * self.width)
        label = str(round(percent,1))
        labwid = (len(label) * self.height) + 1
        self.display.rect(0,0,self.width,self.height, invert, True)
        self.display.rect(0,0,s,self.height, not(invert), True)
        if label:
            if percent < 50:
                self.display.text(label, s+1,0, not(invert))
            else:
                self.display.text(label, s-(labwid) ,0, invert)
        
    def stripes(self, direction=0, offset=0, onwidth=3, offwidth=3):
        pattern = (1,1,1,1,0,0,0,0)
        for y in range(8):
            for x in range(self.width):
                self.display.pixel(x,y,pattern[(offset+y) % len(pattern)])
                offset = offset + 1
    
    # This is not protected against not sending long enough data
    def linegraph(self, data, fill=True, invert=False):
        self.blank()
        for x in range(self.width):
            s = int((data[x]/100) * self.height)
            if fill:
                self.display.vline(x, s, self.height, not(invert))
            else:
                self.display.pixel(x, s, not(invert))

