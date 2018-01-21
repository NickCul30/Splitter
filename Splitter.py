#Splitter
#By Nicholas Culmone

from pygame import *
from math import *
from random import *
from tkinter import *


global WID, HEI, pKeys, keyTaken, players, dupPressed
pKeys = [[K_w, K_a, K_s, K_d], [K_t, K_f, K_g, K_h], [K_i, K_j, K_k, K_l], [K_UP, K_LEFT, K_LEFT, K_RIGHT]]
keyTaken = [True, False, False, False]
WID = 1024
HEI = 720
dupPressed = False


maskPic1 = image.load("Mask/L1Mask.png")
l1Pic = image.load("Levels/L1.png")
maskPic2 = image.load("Mask/L2Mask.png")
l2Pic = image.load("Levels/L2.png")
maskPic3 = image.load("Mask/L3Mask.png")
l3Pic = image.load("Levels/L3.png")
menuPic = image.load("Menu.png")
inst = image.load("Controls.png")
endSc = image.load("endScreen.png")

masks = [maskPic1, maskPic2, maskPic3]
backs = [l1Pic, l2Pic, l3Pic]
playerCols = [(255,140,0), (0,255,255), (0,0,255),  (255,255,0)]
colTaken = [True, False, False, False]

#========================================
# Class Definitions
#========================================

class Player(object):
    #x ,y, master, vel, key, colour, onGround

    def __init__(self, x, y, master, key, colour):
        self.x=x
        self.y=y
        self.master = master
        self.key = key
        self.colour = colour
        self.vel = 0
        self.onGround = True
        
    def setXY(self, x, y):
        self.x = x
        self.y = y
    
    def moveX(self, val):
        self.x += val

    def moveY(self, val):
        self.y += val

    def setKey(self, val):
        self.key = val

    def setOnGround(self, val):
        self.onGround = val

    def setVel(self, val):
        self.vel = val



#========================================
# Method Definitions
#========================================

def move():
    global dupPressed, levelObjColours, solidColours, players, curLevel, mainGame, menuSc

    # Create new char
    if keys[K_q] == 1 and dupPressed == False and len(players) < 4:
        dupPressed = True
        keyTmp = 0
        for i in range(0, len(keyTaken)):
            if keyTaken[i] == False:
                keyTaken[i] = True
                keyTmp = i
                break

        for i in range (0, len(colTaken)):
            if colTaken[i] == False:
                tmpCol = playerCols[i]
                colTaken[i] = True
                break
        tmpPlayer = Player(players[0].x, players[0].y, False, keyTmp, tmpCol)
        players.append(tmpPlayer)

    elif keys[K_q] == 0:
        dupPressed = False

    # Level Checker
    tmpRight = colourR(players[0].x, players[0].y, masks[curLevel])
    if tmpRight[0] == (0,255,0) or tmpRight[1] == (0,255,0):
        curLevel += 1
        if curLevel == 3:
            mainGame = False
            menuSc = 2
            return
        players[0].setXY(spawns[curLevel][0],spawns[curLevel][1])
        for i in range(1, len(players)):
            keyTaken[players[1].key] = False
            colTaken[playerCols.index(players[1].colour)] = False

            players.remove(players[1])

    # Reset
    if keys[K_r] == 1:
        players[0].y = 1200
        
        
    ##################################
    # Player Movement
    ##################################
    
    for i in range(0, len(players)):
        
        # Falling
        if players[i].onGround == True:
            tmpCol = colourD(players[i].x, players[i].y, masks[curLevel])
            flag = True

            top = tmpCol[0]
            bot = tmpCol[1]
            
            for j in range(0, len(levelObjColours[curLevel])):
                if (top == levelObjColours[curLevel][j] or bot == levelObjColours[curLevel][j]) and solidColours[curLevel][j] == True:
                    flag = True

            if flag == True:
                players[i].setOnGround(False)

        # On Ground      
        elif players[i].onGround == False:
            players[i].setVel(players[i].vel + 0.52)
            canMoveD = True
            tmpCol = colourD(players[i].x, players[i].y + players[i].vel, masks[curLevel])

            top = tmpCol[0]
            bot = tmpCol[1]
            
            for j in range(0, len(levelObjColours[curLevel])):
                if (top == levelObjColours[curLevel][j] or bot == levelObjColours[curLevel][j]) and solidColours[curLevel][j] == True:
                    canMoveD = False
                    players[i].setOnGround(True)
                    players[i].setVel(0)
                    
            if canMoveD == True:
                players[i].moveY(players[i].vel)

        # Jump
        if keys[pKeys[players[i].key][0]] == 1 and players[i].onGround == True:
            players[i].setOnGround(False)
            players[i].setVel(-10)

        # Move Left
        if keys[pKeys[players[i].key][1]] == 1:
            canMoveL = True
            tmpCol = colourL(players[i].x - 3, players[i].y, masks[curLevel])
            top = tmpCol[0]
            bot = tmpCol[1]
                            
            
            for j in range(0, len(levelObjColours[curLevel])):
                if (top == levelObjColours[curLevel][j] or bot == levelObjColours[curLevel][j]) and solidColours[curLevel][j] == True or players[i].x - 3 < 0:
                    canMoveL = False
                
    
            if canMoveL == True:
                players[i].moveX(-3)
            
        # Move Right
        if keys[pKeys[players[i].key][3]] == 1:
            canMoveR = True
            tmpCol = colourR(players[i].x + 3, players[i].y, masks[curLevel])
            top = tmpCol[0]
            bot = tmpCol[1]                
            
            for j in range(0, len(levelObjColours[curLevel])):
                if (top == levelObjColours[curLevel][j] or bot == levelObjColours[curLevel][j]) and solidColours[curLevel][j] == True or players[i].x + 23 > 1024:
                    canMoveR = False
                
    
            if canMoveR == True:
                players[i].moveX(3)

        # Death Checker
        if players[i].y > 1024:
            if i == 0: 
                players[0].setXY(spawns[curLevel][0],spawns[curLevel][1])
                for j in range(1, len(players)):
                    keyTaken[players[1].key] = False
                    colTaken[playerCols.index(players[1].colour)] = False

                    players.remove(players[1])
                return
                
            else:
                keyTaken[players[i].key] = False
                colTaken[playerCols.index(players[i].colour)] = False

                players.remove(players[i])
                break
                

def getPixel(mask,x,y):
    if 0<= x < mask.get_width() and 0 <= y < mask.get_height():
        return mask.get_at((int(x),int(y)))[:3]
    else:
        return (-1,-1,-1)

def colourR(x, y, levelMask):
    return [getPixel(levelMask, x + 21, y), getPixel(levelMask, x + 21, y + 20)]

def colourL(x, y, levelMask):
    return [getPixel(levelMask, x -1, y), getPixel(levelMask, x - 1, y + 20)]

def colourD(x, y, levelMask):
    return [getPixel(levelMask, x, y + 21), getPixel(levelMask, x + 20, y + 21)]

def colourU(x, y, levelMask):
    return [getPixel(levelMask, x, y - 1), getPixel(levelMask, x + 20, y - 1)]

def level1Action():
    global solidColours
    solidColours[0][2] = False
    
    for i in range(0, len(players)):
        tmp = colourD(players[i].x, players[i].y + 5, masks[0])

        if tmp[0] == (0,255,255) or tmp[1] == (0,255,255):
            solidColours[0][2] = True

def leve12Action():
    global solidColours

    swit1, swit2, swit3 = [False, False, False]
    solidColours[1][4] = False

    for i in range(0, len(players)):
        left, right = colourD(players[i].x, players[i].y + 10, masks[1])

        if left == (0,255,255) or right == (0,255,255):
            swit1 = True
        if left == (0,0,255) or right == (0,0,255):
            swit2 = True
        if left == (255,255,0) or right == (255,255,0):
            swit3 = True

        if swit1 and swit2 and swit3:
            solidColours[1][4] = True

def leve13Action():
    global solidColours

    swit1, swit2, swit3 = [False, False, False]
    solidColours[2][4] = False
    solidColours[2][5] = True

    for i in range(0, len(players)):
        left, right = colourD(players[i].x, players[i].y + 10, masks[2])

        if left == (100,255,100) or right == (100,255,100):
            swit1 = True
        if left == (255,255,100) or right == (255,255,100):
            swit2 = True
        if left == (255,50,40) or right == (255,50,40):
            swit3 = True

    if swit1 and swit3:
        solidColours[2][4] = True
    if swit2 and not swit1 and not swit3:
        solidColours[2][5] = False

# Draw Level
def drawScene():
    draw.rect(screen, (255, 255, 255), (0, 0, 1980, 1024))
    if curLevel == 0:
        screen.blit(l1Pic, (0,0))
    elif curLevel == 1:
        screen.blit(l2Pic, (0,0))
    elif curLevel == 2:
        screen.blit(l3Pic, (0,0))

    if curLevel == 0:
        if solidColours[0][2] == True:
            draw.rect(screen, (178,101,0), (496, 522,  400, 10))

    if curLevel == 1:
        if solidColours[1][4] == True:
            draw.rect(screen, (178,101,0), (468, 450,  275, 14))
            draw.rect(screen, (178,101,0), (629, 363,  14, 97))
            draw.rect(screen, (178,101,0), (629, 363,  118, 14))

    if curLevel == 2:
        if solidColours[2][5] == True:
            draw.rect(screen, (178,101,0), (860, 0,  17, 150))
        if solidColours[2][4] == True:
            draw.rect(screen, (178,101,0), (357, 493, 120, 75))
            

            
    for i in range(0, len(players)):
        draw.rect(screen,players[i].colour,(int(players[i].x), int(players[i].y), 20, 20))

def mainMenu():
    global mainGame, menuSc
    screen.blit(menuPic, (0,0))
    if mb[0] == 1 and mx > 250 and mx < 775 and my > 390 and my < 470:
        mainGame = True
    elif mb[0] == 1 and mx > 250 and mx < 775 and my > 525 and my < 615:
        menuSc = 1

def instructions():
    global menuSc
    screen.blit(inst, (0,0))

    if keys[K_ESCAPE] == 1:
        menuSc = 0
    

#========================================
# Main Program Follows
#========================================

myClock = time.Clock()
screen = display.set_mode((WID, HEI))
display.set_caption("Splitter")
spawns = [[200,400], [100,400], [50 ,20]]
players = []

curLevel = 0
players.append(Player(spawns[curLevel][0], spawns[curLevel][1], True, 0, playerCols[0]))
menuSc = 0
levelObjColours = [[(255,0,0),(0,255,255),(255,0,255)],
                   [(255,0,0), (0,255,255), (0,0,255), (255,255,0), (255,0,255)],
                   [(178,101,0), (100,255,100), (255,255,100), (255,50,40), (255,0,255), (0,255,255)]]
solidColours = [[True, True, False],
                [True, True, True, True, False],
                [True, True, True, True, False, True]]

mainGame = False

running = True
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False

    keys = key.get_pressed()
    mx,my = mouse.get_pos()
    mb = mouse.get_pressed()

    if mainGame:
        move()
        if mainGame:
            if curLevel == 0:
                level1Action()
            if curLevel == 1:
                leve12Action()
            if curLevel == 2:
                leve13Action()

            drawScene()
    else:
        if menuSc == 0:
            mainMenu()
        elif menuSc == 1:
            instructions()
        else:
            screen.blit(endSc, (0,0))
            
    myClock.tick(60)
    display.flip()
quit()
