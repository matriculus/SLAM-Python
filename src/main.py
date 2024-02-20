import pygame

import env
import sensors

map = pygame.image.load("Images/floor_plan1.jpg")

environment = env.BuildEnvironment(map)
laser = sensors.LaserSensor(200, environment.originalMap, uncertainty=(0.5, 0.01))
environment.map.fill(env.BLACK)
environment.infomap = environment.map.copy()

running = True

def sensor_check():
    sensorOn = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if pygame.mouse.get_focused():
            sensorOn = True
        elif not pygame.mouse.get_focused():
            sensorOn = False
    return sensorOn

while running:
    if sensor_check():
        laser.position = pygame.mouse.get_pos()
        sensor_data = laser.sense_obstacles()
        # print(sensor_data)
        environment.dataStorage(sensor_data)
        environment.showSensorData()

    environment.map.blit(environment.infomap, (0, 0))
    pygame.display.update()
