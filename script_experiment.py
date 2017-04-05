from pygame.locals import *
import pygame, sys, math
from random import randint
import time
import json
import datetime
from datetime import timedelta

data = {}
data['fittslaw'] = [] 
pygame.init()
scr = pygame.display.set_mode((700, 700))
pygame.display.set_caption('Fitts law experiment with mouse clicks')
pygame.mouse.set_cursor(*pygame.cursors.broken_x)
succ_score = 0
unsucc_score = 0
xpos = 200
ypos = 200

#Change radius to change the width of the ball
#radius = 10
radius = 100

oldx = 0
oldy = 0

target_sizes = [ 30, 100]
col1 = (0,20)
col2 = (500,650)
col3 = (350,700)
col4 = (650,20)
target_distances = [col1, col2, col3, col4]
pos = 0
##print(target_distances[pos][1])
pygame.mouse.set_pos(350,350)

def calcDist(x1, y1, x2, y2):
    dist = math.hypot(x2 - x1, y2 - y1)
    return dist

def printstmt(succ,unsucc):
    print('Successful clicks:'+str(succ)+' vs Unsuccessful clicks:'+str(unsucc))

while True:
    pygame.display.update(); scr.fill((200, 200, 255))
    pygame.draw.circle(scr, (255, 0, 0), (xpos, ypos), radius)
    start_time = datetime.datetime.now()
    x = pygame.mouse.get_pos()[0]
    y = pygame.mouse.get_pos()[1]

    sqx = (x - xpos)**2
    sqy = (y - ypos)**2
    for event in pygame.event.get():
        if event.type == QUIT:
            with open('data.json', 'w') as outfile:
                json.dump(data, outfile)
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            dist1 = math.sqrt(sqx + sqy)
            if  dist1 < 100:
                difftime = datetime.datetime.now() - start_time
                print(str(difftime.microseconds))
                succ_score +=1
                dist = calcDist(oldx,oldy,xpos,ypos)

                #appending to data
                data['fittslaw'].append({
                    'time': difftime.microseconds,
                    'distance': dist,
                    'width': 2*radius
                    })
                print(data)
                print("distance by click:" + str(dist1))
                pygame.mouse.set_pos(350,350)
                oldx = xpos
                oldy = ypos 
                xpos = target_distances[pos][0]
                ypos = target_distances[pos][1]
##                radius = randint(10, radius-1)
##                if(radius < 0):
##                    radius = 10
                print("target size:" + str(radius))
                print("target distances:" + str(target_distances[pos]))
                printstmt(succ_score, unsucc_score)
                pos = (pos + 1)%4
                if(pos == 4):
                    sys.exit()
            else:
                unsucc_score +=1
                printstmt(succ_score, unsucc_score)

    
