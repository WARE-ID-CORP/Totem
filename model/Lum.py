from time import sleep
import RPi.GPIO as GPIO
from gpiozero import *

class Lum():
    def __init__(self):
        #Eclairage
        self.a = LED(13)
        self.b = LED(6)
        self.c = LED(26)
        self.d = LED(16)
        self.e = LED(19)
        self.f = LED(20)

        #Bandeau LED
        self.g = LED(11)
        #Resistances
        self.h = LED(21)
        self.i = LED(25)

        self.a.off()
        self.b.off()
        self.c.off()
        self.d.off()
        self.e.off()
        self.f.off()
        self.g.on()
        self.h.off()
        self.i.off()

    def startFlash(self):
        self.a.on()
        self.b.off()
        self.c.on()
        self.d.off()
        self.e.on()
        self.f.on()

    def stopFlash(self):
        self.a.off()
        self.b.off()
        self.c.off()
        self.d.off()
        self.e.off()
        self.f.off()

    def progStart(self):
        self.flash(1)
        sleep(0.5)
        self.flash(1)


    def isFlashing(self):
        return self.triggerLum1.value and self.triggerLum2.value

    def flash(self, delay):
        self.startFlash()
        sleep(delay)
        self.stopFlash()