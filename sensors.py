import math
import pygame
import numpy as np
from threading import Thread, Lock

import env

mutex = Lock()
def uncertainty_add(distance, angle, sigma):
    mean = np.array([distance, angle])
    covariance = np.diag(sigma**2)
    distance, angle = np.random.multivariate_normal(mean, covariance)
    return [max(distance, 0), max(angle, 0)]

class LaserSensor:
    def __init__(self, range, map, uncertainty):
        self.range = range
        self.map = map
        self.speed = 4 # rounds per second
        self.sigma = np.array(uncertainty)
        self.position = (0, 0)
        self.width, self.height = pygame.display.get_surface().get_size()
        self.sensedObstacles = []

    def distance(self, obstaclePosition):
        px = obstaclePosition[0] - self.position[0]
        py = obstaclePosition[1] - self.position[1]
        return math.sqrt(px**2 + py**2)

    def sense_obstacles(self):
        data = []
        threads = []
        for angle in np.linspace(0, 2*math.pi, 60, False):
            t = Thread(target=self._senseAtAngle, args=(angle, data,))
            threads.append(t)
            t.start()
        for thread in threads:
            thread.join()
        if len(data) > 0:
            return data
        else:
            return False

    def _senseAtAngle(self, angle, data):
        x1 = self.position[0]
        y1 = self.position[1]
        x2 = x1 + self.range * math.cos(angle)
        y2 = y1 - self.range * math.sin(angle)
        for u in np.linspace(0, 1, 100):
            x = int(x2 * u + x1 * (1 - u))
            y = int(y2 * u + y1 * (1 - u))
            if 0 < x < self.width and 0 < y < self.height:
                colour = self.map.get_at((x, y))
                if colour == env.BLACK:
                    distance = self.distance((x, y))
                    output = self.pc2cartesian(*uncertainty_add(distance, angle, self.sigma))
                    with mutex:
                        data.append(output)
                    break

    def pc2cartesian(self, distance, angle):
        x = self.position[0] + distance * math.cos(angle)
        y = self.position[1] - distance * math.sin(angle)
        return int(x), int(y)
