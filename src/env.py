import math
import pygame

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (70, 70, 70)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class BuildEnvironment:
    def __init__(self, map):
        pygame.init()
        self.pointCloud = []
        self.externalMap = map
        self.mapW, self.mapH = map.get_size()
        self.mapWindowName = "PC Data"
        pygame.display.set_caption(self.mapWindowName)
        self.map = pygame.display.set_mode((self.mapW, self.mapH))
        self.infomap = None
        self.map.blit(self.externalMap, (0, 0))
        self.originalMap = self.map.copy()

    def pc2cartesian(self, distance, angle, robotPosition):
        x = robotPosition[0] + distance * math.cos(angle)
        y = robotPosition[1] - distance * math.sin(angle)
        return int(x), int(y)

    def dataStorage(self, data):
        if data:
            for point in data:
                if point not in self.pointCloud:
                    self.pointCloud.append(point)

    def showSensorData(self):
        self.infomap = self.map.copy()
        for point in self.pointCloud:
            self.infomap.set_at(point, RED)

