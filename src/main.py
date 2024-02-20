import pygame
import sys

import env
import sensors

sys.path.append("./")
from QuadtreeMap import quadtreemap

map = pygame.image.load("Images/floor_plan1.jpg")


maxlevel = 5
WIDTH, HEIGHT = map.get_size()
boundbox = quadtreemap.Rectangle(0, 0, WIDTH, HEIGHT)
qmap = quadtreemap.QuadTree(boundbox, maxlevel)
tapp = quadtreemap.Tree(WIDTH, HEIGHT)

environment = env.BuildEnvironment(map)
laser = sensors.LaserSensor(200, environment.originalMap, uncertainty=(0.5, 0.01))
environment.map.fill(env.BLACK)
environment.infomap = environment.map.copy()

running = True

while running:
    sensorOn = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if pygame.mouse.get_focused():
            sensorOn = True
        elif not pygame.mouse.get_focused():
            sensorOn = False
    
    if sensorOn:
        laser.position = pygame.mouse.get_pos()
        sensor_data = laser.sense_obstacles()
        qmap.insert(sensor_data)
        # tapp.draw(map.root)
        # tapp.drawPCData(pcData)
        # tapp.update()
        environment.dataStorage(sensor_data)
        environment.showSensorData()

    environment.map.blit(environment.infomap, (0, 0))
    pygame.display.update()
