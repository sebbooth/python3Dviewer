# Example file showing a circle moving on screen
import pygame
import math
import time
import numpy as np
from objReader import *
from rayOps import *

#read obj file/files
vertices, polygons = readFile("car.obj")


# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
center_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)


# Setup camera and viewPlane
camPos = np.array([0,3,-23])
camDir = np.array([0,0,1])
viewX = np.array([1,0,0])
viewY = np.array([0,1,0])
focalLength = 2

viewPlane = camPos + focalLength*camDir

w = 2.5
h = w * (screen.get_width()/screen.get_height())

scale = screen.get_width()/w
xDis = screen.get_width() / 2
yDis = screen.get_height() / 2


lightPos = np.array([6,6,-3])


clock = pygame.time.Clock()

def polySort(e, camPos, vertices):
        p = []
        for v in e:
            p.append(vertices[v-1])
        p = np.array(p)
        p = np.average(p)
        return np.dot(p - camPos, p-camPos)

def rotateCamX(camPos, camDir, viewPlane, viewX, viewY, angle):
    
    angle = np.pi * (angle/180)
    rotMat = np.array([
    [1, 0, 0],
    [0,math.cos(angle),-math.sin(angle)],
    [0, math.sin(angle), math.cos(angle)]
    ])

    camPos = np.matmul(rotMat, camPos)
    camDir = np.matmul(rotMat, camDir)
    viewX = np.matmul(rotMat, viewX)
    viewY = np.matmul(rotMat, viewY)
    viewPlane = camPos + focalLength*camDir
    return camPos, camDir, viewPlane, viewX, viewY

def rotateCamY(camPos, camDir, viewPlane, viewX, viewY, angle):
    
    angle = np.pi * (angle/180)
    rotMat = np.array([
    [math.cos(angle),0,math.sin(angle)],
    [0, 1, 0],
    [-math.sin(angle), 0, math.cos(angle)]
    ])

    camPos = np.matmul(rotMat, camPos)
    camDir = np.matmul(rotMat, camDir)
    viewX = np.matmul(rotMat, viewX)
    viewY = np.matmul(rotMat, viewY)
    viewPlane = camPos + focalLength*camDir
    return camPos, camDir, viewPlane, viewX, viewY

rotation = 0

# For displaying text
pygame.font.init() 
my_font = pygame.font.SysFont('Arial', 30)

while running:
    
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    clock.tick()

    text_surface = my_font.render("FPS: " + str(int(clock.get_fps())), False, 'white')

    screen.blit(text_surface, (0,0))
    
    """
    pygame.draw.circle(screen, "red", player_pos, 5)
    pygame.draw.line(screen, "black", center_pos, player_pos)
    """

    polygons = sorted(polygons, key=lambda poly: polySort(poly, camPos, vertices))
    minShade = np.dot(polygons[0][0] - camPos, polygons[0][0]-camPos)
    maxShade = np.dot(polygons[-1][0] - camPos, polygons[-1][0]-camPos)
    #############################################################################
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


        """
        norm = np.cross((p[1]-p[0]),(p[2]-p[0]))
        shade = np.dot(norm, (lightPos-p[0]))
        try:
            shade = int(np.arccos(shade)*60)
        except:
            norm = np.cross((p[0]-p[1]),(p[2]-p[1]))

            shade = np.dot(norm, (lightPos-p[0]))
            try:
                shade = int(np.arccos(shade)*60)
            except:
                shade = 0

        pygame.draw.polygon(screen, (shade,shade,shade), scaleP, 0)
        """
        """
        for n in scaleP:
            #print(n[1])
            if n[1] > 255:
                n[1] = 255
            elif n[1] < 0 :
                n[1] = 0
        
            pygame.draw.circle(screen, (n[1],n[1],n[1]), n[0], 2)
        """
        scaleP = [n[0] for n in scaleP]

        pygame.draw.polygon(screen, "white", scaleP, 1)

        """
        pygame.draw.line(screen, "black", scaleP[0], scaleP[1])
        pygame.draw.line(screen, "black", scaleP[0], scaleP[2])
        pygame.draw.line(screen, "black", scaleP[1], scaleP[2])
        
        """

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
        camPos, camDir, viewPlane, viewX, viewY = rotateCamX(camPos, camDir, viewPlane, viewX, viewY, 10)

    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
        camPos, camDir, viewPlane, viewX, viewY = rotateCamX(camPos, camDir, viewPlane, viewX, viewY, -10)

    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
        camPos, camDir, viewPlane, viewX, viewY = rotateCamY(camPos, camDir, viewPlane, viewX, viewY, 10)
        rotation += 1

    if keys[pygame.K_d]:
        player_pos.x += 300 * dt
        camPos, camDir, viewPlane, viewX, viewY = rotateCamY(camPos, camDir, viewPlane, viewX, viewY, -10)
        rotation -= 1


    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()