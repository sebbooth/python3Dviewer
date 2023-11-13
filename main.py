# Example file showing a circle moving on screen
import pygame
import math
import time
import sys
import numpy as np
from resources.objReader import *
from resources.rayOps import *
from resources.renderFuncs import *

#read obj file/files
filename = sys.argv[1]
vertices, polygons = readFile(filename)


# pygame setup
pygame.init()
screen = pygame.display.set_mode((720, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
center_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)


# Setup camera and viewPlane
camPos = np.array([0,0,4])
camDir = np.array([0,0,-1])
viewX = np.array([1,0,0])
viewY = np.array([0,1,0])
focalLength = 3

viewPlane = camPos + focalLength*camDir

w = 2.5

h = w * (screen.get_width()/screen.get_height())

scale = screen.get_width()/w
xDis = screen.get_width() / 2
yDis = screen.get_height() / 2


lightPos = np.array([3,3,-5])


clock = pygame.time.Clock()

rotation = 0
shading = True
points = False
wireframe = True

# For displaying text
pygame.font.init() 
my_font = pygame.font.SysFont('Arial', 20)


while running:


    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    clock.tick()

    text_surface1 = my_font.render("FPS: " + str(int(clock.get_fps())), False, 'white')
    text_surface3 = my_font.render("movement : WASD RF ", False, 'white')
    text_surface4 = my_font.render("show/hide faces : L ", False, 'white')
    text_surface5 = my_font.render("wireframe on/off : O ", False, 'white')
    text_surface6 = my_font.render("highlight vertices : P ", False, 'white')
    text_surface7 = my_font.render("exit : ESC ", False, 'white')

    screen.blit(text_surface1, (0,0))
    screen.blit(text_surface3, (screen.get_width()-text_surface3.get_width(),screen.get_height()-5*text_surface3.get_height()))
    screen.blit(text_surface4, (screen.get_width()-text_surface4.get_width(),screen.get_height()-4*text_surface4.get_height()))
    screen.blit(text_surface5, (screen.get_width()-text_surface5.get_width(),screen.get_height()-3*text_surface5.get_height()))
    screen.blit(text_surface6, (screen.get_width()-text_surface6.get_width(),screen.get_height()-2*text_surface6.get_height()))
    screen.blit(text_surface7, (screen.get_width()-text_surface7.get_width(),screen.get_height()-1*text_surface6.get_height()))


    #############################################################################
    if shading:
        polygons = sorted(polygons, key=lambda poly: polySort(poly, camPos, vertices))
        minShade = np.dot(polygons[0][0] - camPos, polygons[0][0]-camPos)
        maxShade = np.dot(polygons[-1][0] - camPos, polygons[-1][0]-camPos)

        for poly in polygons:
            p = [] 
            for v in poly:
                p.append(vertices[v-1])
            p = np.array(p)
            scaleP = []

            for v in p:
                ray = v-camPos
                shade = 255-np.dot(v - camPos, v-camPos)*2
                
                pixel = LinePlaneCollision(camDir, viewPlane, ray, camPos)
                pixelX = np.dot((pixel-camPos), viewX)
                pixelY = -np.dot((pixel-camPos), viewY)
                scaleP.append([[pixelX * scale + xDis, pixelY * scale + yDis], shade])


            norm = np.cross((p[1]-p[0]),(p[2]-p[0]))

            norm = normalize(norm)

            shade = np.dot(norm, normalize(lightPos-p[0]))
            try:
                shade = int(np.arccos(shade)*60)
            except:

                norm = np.cross((p[0]-p[1]),(p[2]-p[1]))

                shade = np.dot(norm, (lightPos-p[0]))
                try:
                    shade = int(np.arccos(shade)*60)
                except:
                    shade = 0


            scaleP = [n[0] for n in scaleP]
            pygame.draw.polygon(screen, (shade,shade,shade), scaleP, 0)

            if wireframe:
                pygame.draw.polygon(screen, "black", scaleP, 1)

            if points:
                for v in scaleP:
                    pygame.draw.circle(screen, "red", v, 3)
        
    else:
        for poly in polygons:
            p = [] 
            for v in poly:
                p.append(vertices[v-1])
            p = np.array(p)
            scaleP = []

            for v in p:
                ray = v-camPos                
                pixel = LinePlaneCollision(camDir, viewPlane, ray, camPos)
                pixelX = np.dot((pixel-camPos), viewX)
                pixelY = -np.dot((pixel-camPos), viewY)
                scaleP.append([pixelX * scale + xDis, pixelY * scale + yDis])
    
            if wireframe:
                pygame.draw.polygon(screen, "white", scaleP, 1)
      
            if points:
                for v in scaleP:
                    pygame.draw.circle(screen, "red", v, 3)
              
    camPos, camDir, lightPos, viewPlane, viewX, viewY, shading, points, wireframe = handleEvents(clock, camPos, camDir, focalLength, lightPos, viewPlane, viewX, viewY, shading, points, wireframe)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    #

pygame.quit()

