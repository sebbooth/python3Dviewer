import pygame
import math
import time
import sys
import numpy as np

def polySort(e, camPos, vertices):
        p = []
        for v in e:
            p.append(vertices[v-1])
        p = np.array(p)
        avg = 0
        for v in p:
            avg += np.dot(v - camPos, v-camPos)
        avg /= len(p)
        return -avg

def rotateCamX(camPos, camDir, focalLength, lightPos, viewPlane, viewX, viewY, angle):
    
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
    lightPos = np.matmul(rotMat, lightPos)
    viewPlane = camPos + focalLength*camDir
    return camPos, camDir, lightPos, viewPlane, viewX, viewY

def rotateCamY(camPos, camDir, focalLength, lightPos, viewPlane, viewX, viewY, angle):
    
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
    lightPos = np.matmul(rotMat, lightPos)
    viewPlane = camPos + focalLength*camDir
    return camPos, camDir, lightPos, viewPlane, viewX, viewY


def handleEvents(clock, camPos, camDir, focalLength, lightPos, viewPlane, viewX, viewY, shading, points, wireframe):
    dt = clock.tick(60) / 1000
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        camPos, camDir, lightPos, viewPlane, viewX, viewY = rotateCamX(camPos, camDir, focalLength, lightPos, viewPlane, viewX, viewY, 100*dt)

    if keys[pygame.K_s]:
        camPos, camDir, lightPos, viewPlane, viewX, viewY = rotateCamX(camPos, camDir, focalLength, lightPos, viewPlane, viewX, viewY, -100*dt)

    if keys[pygame.K_a]:
        camPos, camDir, lightPos, viewPlane, viewX, viewY = rotateCamY(camPos, camDir, focalLength, lightPos, viewPlane, viewX, viewY, 100*dt)

    if keys[pygame.K_d]:
        camPos, camDir, lightPos, viewPlane, viewX, viewY = rotateCamY(camPos, camDir, focalLength, lightPos, viewPlane, viewX, viewY, -100*dt)

    if keys[pygame.K_r]:
        camPos = np.add(camPos, camDir * 5 * dt)
        viewPlane = camPos + focalLength*camDir


    if keys[pygame.K_f]:
        camPos = np.add(camPos, camDir * 5 * -dt)
        viewPlane = camPos + focalLength*camDir
    

    for ev in pygame.event.get():
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_p:
                if points:
                    points = False
                else:
                    points = True
    
            if ev.key == pygame.K_l:
                if shading:
                    shading = False
                else:
                    shading = True

            if ev.key == pygame.K_o:
                if wireframe:
                    wireframe = False
                else:
                    wireframe = True

            if ev.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    return camPos, camDir, lightPos, viewPlane, viewX, viewY, shading, points, wireframe

