import pygame as pg
import os
import sys

import dungeon as dg

pg.init()
pg.font.init()

programIcon = pg.image.load('Assets/eob_icon.png')

pg.display.set_icon(programIcon)

pg.display.set_caption('Py of the Beholder')

FPS = 60

WIDTH = 40*24
HEIGHT = WIDTH*625//1000

#Width and height of Background of environment window
BG_WH = (WIDTH*55//100,HEIGHT*60//100)
#define width and height on environment panels
P1_WH = (WIDTH*9//120,HEIGHT*60//100)
P2_WH = (WIDTH*9//120,HEIGHT*48//100)
P2_WH = (WIDTH*9//120,HEIGHT*48//100)
P3_WH = (WIDTH*5//100,HEIGHT*32//100)
P4_WH = (WIDTH*5//300,HEIGHT*20//100)

FP3_WH = (WIDTH*5//100,HEIGHT*24//100)
KP3_WH = (WIDTH*5//100,HEIGHT*24//100)

FP4_WH = (WIDTH*15//200,HEIGHT*20//100)
KP4_WH = (WIDTH*15//200,HEIGHT*20//100)

F1_WH = (WIDTH*40//100,HEIGHT*48//100)
F2_WH = (WIDTH*25//100,HEIGHT*32//100)
F3_WH = (WIDTH*15//100,HEIGHT*20//100)

COMPASS1_WH = (60,51)
COMPASS2_WH = (50,30)

#position arguments of Panels
ORIGIN_POS = (0,0)
LP1_POS = (0,0)
LP2_POS = (WIDTH*9//120,HEIGHT*4//100)
LP3_POS = (WIDTH*15//100,HEIGHT*8//100)
LP4_POS = (WIDTH*20//100,HEIGHT*12//100)

FP3_POS = (0,HEIGHT*12//100)
KP3_POS = (WIDTH*50//100,HEIGHT*12//100)

FP4_POS = (WIDTH*5//100,HEIGHT*12//100)
KP4_POS = (WIDTH*85//200,HEIGHT*12//100)

RP1_POS = (WIDTH*95//200,0)
RP2_POS = (WIDTH*40//100,HEIGHT*4//100)
RP3_POS = (WIDTH*35//100,HEIGHT*8//100)
RP4_POS = (WIDTH*1//3,HEIGHT*12//100)

LF1_POS = (WIDTH*9//120-F1_WH[0],HEIGHT*4//100)
CF1_POS = (WIDTH*9//120,HEIGHT*4//100)
RF1_POS = (WIDTH*9//120+F1_WH[0],HEIGHT*4//100)

LF2_POS = (-WIDTH*10//100,HEIGHT*8//100)
CF2_POS = (WIDTH*15//100,HEIGHT*8//100)
RF2_POS = (WIDTH*40//100,HEIGHT*8//100)

FF3_POS = (WIDTH*20//100-F3_WH[0]*2,HEIGHT*12//100)
LF3_POS = (WIDTH*20//100-F3_WH[0],HEIGHT*12//100)
CF3_POS = (WIDTH*20//100,HEIGHT*12//100)
RF3_POS = (WIDTH*20//100+F3_WH[0],HEIGHT*12//100)
KF3_POS = (WIDTH*20//100+F3_WH[0]*2,HEIGHT*12//100)

RF2_POS = (WIDTH*40//100,HEIGHT*8//100)

COMPASSC_POS = (WIDTH*336//960,HEIGHT*384//600) #(336,384)
COMPASSL_POS = (WIDTH*232//960,HEIGHT*462//600) #(232,462)
COMPASSR_POS = (WIDTH*450//960,HEIGHT*462//600) #(450,462)

WIN = pg.display.set_mode((WIDTH, HEIGHT))


Walls_path = os.path.join('Assets/Environments', dg.environment, 'Walls')
Adornments_path = os.path.join('Assets/Environments', dg.environment, 'Adornments')




panels={
'FP4':['x','FP4.png',FP4_WH,FP4_POS,{'E':(3,-1),'W':(-3,2),'N':(-1,-3),'S':(2,3)}],
'KP4':['x','KP4.png',KP4_WH,KP4_POS,{'E':(3,2),'W':(-3,-1),'N':(2,-3),'S':(-1,3)}],
'LP4':['x','LP4.png',P4_WH,LP4_POS,{'E':(3,0),'W':(-3,1),'N':(0,-3),'S':(1,3)}],
'RP4':['x','RP4.png',P4_WH,RP4_POS,{'E':(3,1),'W':(-3,0),'N':(1,-3),'S':(0,3)}],
'FF3':['x','F3.png',F3_WH,FF3_POS,{'E':(3,-2),'W':(-2,2),'N':(-2,-2),'S':(2,3)}],
'LF3':['x','F3.png',F3_WH,LF3_POS,{'E':(3,-1),'W':(-2,1),'N':(-1,-2),'S':(1,3)}],
'CF3':['x','F3.png',F3_WH,CF3_POS,{'E':(3,0),'W':(-2,0),'N':(0,-2),'S':(0,3)}],
'RF3':['x','F3.png',F3_WH,RF3_POS,{'E':(3,1),'W':(-2,-1),'N':(1,-2),'S':(-1,3)}],
'KF3':['x','F3.png',F3_WH,KF3_POS,{'E':(3,2),'W':(-2,-2),'N':(2,-2),'S':(-2,3)}],
'CD3':['0','D3.png',F3_WH,CF3_POS,{'E':(3,0),'W':(-3,0),'N':(0,-3),'S':(0,3)}],
'LD3':['0','LD3.png',F3_WH,LF3_POS,{'E':(3,-1),'W':(-3,1),'N':(-1,-3),'S':(1,3)}],
'RD3':['0','RD3.png',F3_WH,RF3_POS,{'E':(3,1),'W':(-3,-1),'N':(1,-3),'S':(-1,3)}],
'FP3':['x','FP3.png',FP3_WH,FP3_POS,{'E':(2,-1),'W':(-2,2),'N':(-1,-2),'S':(2,2)}],
'LP3':['x','LP3.png',P3_WH,LP3_POS,{'E':(2,0),'W':(-2,1),'N':(0,-2),'S':(1,2)}],
'RP3':['x','RP3.png',P3_WH,RP3_POS,{'E':(2,1),'W':(-2,0),'N':(1,-2),'S':(0,2)}],
'KP3':['x','KP3.png',KP3_WH,KP3_POS,{'E':(2,2),'W':(-2,-1),'N':(2,-2),'S':(-1,2)}],
'LF2':['x','F2.png',F2_WH,LF2_POS,{'E':(2,-1),'W':(-1,1),'N':(-1,-1),'S':(1,2)}],
'CF2':['x','F2.png',F2_WH,CF2_POS,{'E':(2,0),'W':(-1,0),'N':(0,-1),'S':(0,2)}],
'RF2':['x','F2.png',F2_WH,RF2_POS,{'E':(2,1),'W':(-1,-1),'N':(1,-1),'S':(-1,2)}],
'CD2':['0','D2.png',F2_WH,CF2_POS,{'E':(2,0),'W':(-2,0),'N':(0,-2),'S':(0,2)}],
'LD2':['0','LD2.png',F2_WH,LF2_POS,{'E':(2,-1),'W':(-2,1),'N':(-1,-2),'S':(1,2)}],
'RD2':['0','RD2.png',F2_WH,RF2_POS,{'E':(2,1),'W':(-2,-1),'N':(1,-2),'S':(-1,2)}],
'LP2':['x','LP2.png',P2_WH,LP2_POS,{'E':(1,0),'W':(-1,1),'N':(0,-1),'S':(1,1)}],
'RP2':['x','RP2.png',P2_WH,RP2_POS,{'E':(1,1),'W':(-1,0),'N':(1,-1),'S':(0,1)}],
'LF1':['x','F1.png',F1_WH,LF1_POS,{'E':(1,-1),'W':(0,1),'N':(-1,0),'S':(1,1)}],
'CF1':['x','F1.png',F1_WH,CF1_POS,{'E':(1,0),'W':(0,0),'N':(0,0),'S':(0,1)}],
'RF1':['x','F1.png',F1_WH,RF1_POS,{'E':(1,1),'W':(0,-1),'N':(1,0),'S':(-1,1)}],
'CD1':['0','D1.png',F1_WH,CF1_POS,{'E':(1,0),'W':(-1,0),'N':(0,-1),'S':(0,1)}],
'LD1':['0','LD1.png',F1_WH,LF1_POS,{'E':(1,-1),'W':(-1,1),'N':(-1,-1),'S':(1,1)}],
'RD1':['0','RD1.png',F1_WH,RF1_POS,{'E':(1,1),'W':(-1,-1),'N':(1,-1),'S':(-1,1)}],
'LP1':['x','LP1.png',P1_WH,LP1_POS,{'E':(0,0),'W':(0,1),'N':(0,0),'S':(1,0)}],
'RP1':['x','RP1.png',P1_WH,RP1_POS,{'E':(0,1),'W':(0,0),'N':(1,0),'S':(0,0)}],
      }

Adornments_panels={
'FP4':['x','FP4.png',FP4_WH,FP4_POS],
'KP4':['x','KP4.png',KP4_WH,KP4_POS],
'LP4':['x','LP4.png',P4_WH,LP4_POS],
'RP4':['x','RP4.png',P4_WH,RP4_POS],
'FF3':['x','F3.png',F3_WH,FF3_POS],
'LF3':['x','F3.png',F3_WH,LF3_POS],
'CF3':['x','F3.png',F3_WH,CF3_POS],
'RF3':['x','F3.png',F3_WH,RF3_POS],
'KF3':['x','F3.png',F3_WH,KF3_POS],
'CD3':['0','D3.png',F3_WH,CF3_POS],
'LD3':['0','LD3.png',F3_WH,LF3_POS],
'RD3':['0','RD3.png',F3_WH,RF3_POS],
'FP3':['x','FP3.png',FP3_WH,FP3_POS],
'LP3':['x','LP3.png',P3_WH,LP3_POS],
'RP3':['x','RP3.png',P3_WH,RP3_POS],
'KP3':['x','KP3.png',KP3_WH,KP3_POS],
'LF2':['x','F2.png',F2_WH,LF2_POS],
'CF2':['x','F2.png',F2_WH,CF2_POS],
'RF2':['x','F2.png',F2_WH,RF2_POS],
'CD2':['0','D2.png',F2_WH,CF2_POS],
'LD2':['0','LD2.png',F2_WH,LF2_POS],
'RD2':['0','RD2.png',F2_WH,RF2_POS],
'LP2':['x','LP2.png',P2_WH,LP2_POS],
'RP2':['x','RP2.png',P2_WH,RP2_POS],
'LF1':['x','F1.png',F1_WH,LF1_POS],
'CF1':['x','F1.png',F1_WH,CF1_POS],
'RF1':['x','F1.png',F1_WH,RF1_POS],
'CD1':['0','D1.png',F1_WH,CF1_POS],
'LD1':['0','LD1.png',F1_WH,LF1_POS],
'RD1':['0','RD1.png',F1_WH,RF1_POS],
'LP1':['x','LP1.png',P1_WH,LP1_POS],
'RP1':['x','RP1.png',P1_WH,RP1_POS],
      }


playerPosition=[7,13,'E']


def move(KeyPress):
    global playerPosition

    Moves = {
        'w':{'N':[0,-1,'N'],'S':[0,+1,'S'],'E':[+1,0,'E'],'W':[-1,0,'W']},
        's':{'N':[0,+1,'N'],'S':[0,-1,'S'],'E':[-1,0,'E'],'W':[+1,0,'W']},
        'a':{'N':[-1,0,'N'],'S':[+1,0,'S'],'E':[0,-1,'E'],'W':[0,+1,'W']},
        'd':{'N':[+1,0,'N'],'S':[-1,0,'S'],'E':[0,+1,'E'],'W':[0,-1,'W']},
        'q':{'N':[0,0,'W'],'S':[0,0,'E'],'E':[0,0,'N'],'W':[0,0,'S']},
        'e':{'N':[0,0,'E'],'S':[0,0,'W'],'E':[0,0,'S'],'W':[0,0,'N']}
        }

    if dg.Clipping[playerPosition[1]+Moves[KeyPress][playerPosition[2]][1]][playerPosition[0] + Moves[KeyPress][playerPosition[2]][0]] in [1,3]:
        print("You can't go that way")
    else:
        playerPosition[0] += Moves[KeyPress][playerPosition[2]][0]
        playerPosition[1] += Moves[KeyPress][playerPosition[2]][1]
        playerPosition[2] =  Moves[KeyPress][playerPosition[2]][2]
        print(playerPosition)

def clickSwitch():
    global panels
    global playerPosition
    x,y,d = playerPosition    
    
    if tuple(playerPosition) in dg.switches.keys():
        x  = dg.switches[tuple(playerPosition)][0][0]
        y  = dg.switches[tuple(playerPosition)][0][1]
        if dg.Clipping[x][y] == 3:
            dg.Clipping[x][y] = 2
            dg.Adornments[dg.switches[tuple(playerPosition)][1]]='LeverDown'
            
        else:
            dg.Clipping[x][y] = 3
            dg.Adornments[dg.switches[tuple(playerPosition)][1]]='LeverUp'
  

def getPanels(playerPosition,WallsX,WallsY):
    global panels
    x,y,d = playerPosition
    
    if d in 'EW':
        a,b = 'P','F'
    else:
        a,b = 'F','P'
    
    # assign WallX panels
    for panel in filter(lambda x:x[1]==a, panels.keys()):
        panels[panel][0]=dg.WallsX[y+panels[panel][4][d][1]][x+panels[panel][4][d][0]]
        
        Adornment_Key = ('x',x+panels[panel][4][d][0],y+panels[panel][4][d][1])
        if Adornment_Key in dg.Adornments.keys():
            Adornments_panels[panel][0] = dg.Adornments[Adornment_Key]
        else:
            Adornments_panels[panel][0] = 'x'

    # assign WallY Panels
    for panel in filter(lambda x:x[1]==b, panels.keys()):
        panels[panel][0]=dg.WallsY[y+panels[panel][4][d][1]][x+panels[panel][4][d][0]]
        
        Adornment_Key = ('y',x+panels[panel][4][d][0],y+panels[panel][4][d][1])
        if Adornment_Key in dg.Adornments.keys():
            Adornments_panels[panel][0] = dg.Adornments[Adornment_Key]
        else:
            Adornments_panels[panel][0] = 'x'



    # Assign the door panels        
    for panel in filter(lambda x:x[1]=='D', panels.keys()):
        panels[panel][0]=str(dg.Clipping[y+panels[panel][4][d][1]][x+panels[panel][4][d][0]])

def quitGame():
    pg.quit()
    # sys.exit()

def redrawWindow():

    #Choose background art based on position
    if playerPosition[0] % 2 == 0 and playerPosition[1] % 2 == 0 and playerPosition[2] in 'NS':
        BG_ART = 'BG1.png'
    elif playerPosition[0] % 2 == 1 and playerPosition[1] % 2 == 0 and playerPosition[2] in 'NS':
        BG_ART = 'BG2.png'
    elif playerPosition[0] % 2 == 0 and playerPosition[1] % 2 == 1 and playerPosition[2] in 'NS':
        BG_ART = 'BG2.png'
    elif playerPosition[0] % 2 == 1 and playerPosition[1] % 2 == 1 and playerPosition[2] in 'NS':
        BG_ART = 'BG1.png'
        
    elif playerPosition[0] % 2 == 0 and playerPosition[1] % 2 == 0 and playerPosition[2] in 'EW':
        BG_ART = 'BG2.png'
    elif playerPosition[0] % 2 == 1 and playerPosition[1] % 2 == 0 and playerPosition[2] in 'EW':
        BG_ART = 'BG1.png'
    elif playerPosition[0] % 2 == 0 and playerPosition[1] % 2 == 1 and playerPosition[2] in 'EW':
        BG_ART = 'BG1.png'
    elif playerPosition[0] % 2 == 1 and playerPosition[1] % 2 == 1 and playerPosition[2] in 'EW':
        BG_ART = 'BG2.png'

    #  Render the background of the view window        
    BG = pg.transform.scale(pg.image.load(os.path.join('Assets/Environments', dg.environment, BG_ART)), BG_WH)    
    WIN.blit(BG, ORIGIN_POS)
    
    # Render all the wall panels and environment
    for panel in panels.keys():
        # Redender the Wall panel
        img = pg.transform.scale(pg.image.load(os.path.join(Walls_path, panels[panel][0], panels[panel][1])), panels[panel][2])
        WIN.blit(img, panels[panel][3])

        # Render the Adornment
        img = pg.transform.scale(pg.image.load(os.path.join(Adornments_path, Adornments_panels[panel][0], Adornments_panels[panel][1])), Adornments_panels[panel][2])
        WIN.blit(img, Adornments_panels[panel][3])          

    # render the UI
    UI = pg.transform.scale(pg.image.load(os.path.join('Assets', 'UI', playerPosition[2] + '.png')), (WIDTH, HEIGHT))
    WIN.blit(UI, ORIGIN_POS)
    
    # display it in pygame
    pg.display.update()

def main():
    
    clock = pg.time.Clock()
    
    while True:
        clock.tick(FPS)
        getPanels(playerPosition,dg.WallsX,dg.WallsY)
        redrawWindow()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                quitGame()
                
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    quitGame() 
                
                if pg.key.name(event.key) in 'qweasd':
                    move(pg.key.name(event.key))
                    
                if event.key == pg.K_SPACE:
                    clickSwitch()

                                     
                    
main()