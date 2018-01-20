#Splitter
#By Matthew Farias and Nicholas Culmone

from pygame import *
from math import *
from random import *

#========================================

class Barth(object):
    x=0
    y=0

    def __init__(self,x,y):
        self.x=x
        self.y=y

    def

myClock = time.Clock()
global WID, HEI
WID = 1024
HEI = 720
screen = display.set_mode((WID, HEI))

loadimages()

running = True
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False

    keys = key.get_pressed()
    mx,my = mouse.get_pos()
    mb = mouse.get_pressed()



    myClock.tick(60)
    display.flip()
quit()
