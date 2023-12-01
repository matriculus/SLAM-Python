import numpy as np
import math

class Cluster:
    def __init__(self, data):
        self.rawData = data
        self.pairs = {x:None for x in self.rawData}
        self.closestPairs = 0 # self.closest(self.rawData)
        self.bruteForce(self.rawData)

    def distance(self, p1, p2):
        assert len(p1) == len(p2), "Dimensions of the points are not the same"
        dimDiff = []
        for x1, x2 in zip(p1, p2):
            dimDiff.append((x2-x1)**2)

        return math.sqrt(sum(dimDiff))

    def bruteForce(self, points):
        n = len(points)
        for i in range(n):
            min_dist = float("inf")
            for j in range(n):
                if i == j:
                    continue
                d = self.distance(points[i], points[j])
                if d < min_dist:
                    min_dist = d
                    self.pairs[points[i]] = points[j]
        return min_dist

    def stripClosest(self, strip, d):
        size = len(strip)
        min_dist = d
        strip = sorted(strip, key=lambda point: point[0])
        for i in range(size):
            for j in range(i+1, size):
                if (strip[j][1] - strip[i][1]) >= min_dist:
                    break
                dist = self.distance(strip[i], strip[j])
                if dist < min_dist:
                    min_dist = dist
        return min_dist

    def closestUtil(self, sortedPoints):
        n = len(sortedPoints)
        if n <= 3:
            return self.bruteForce(points)

        mid = n//2
        midPoint = points[mid]
        dl = self.closestUtil(points[:mid])
        dr = self.closestUtil(points[mid:])
        d = min(dl, dr)
        strip = []
        for i in range(n):
            if abs(points[i][0] - midPoint[0]) < d:
                strip.append(points[i])
        return min(d, self.stripClosest(strip, d))

    def closest(self, points):
        points = sorted(points, key=lambda point: point[0])
        return self.closestUtil(points)

if __name__ == "__main__":
    points = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4), (4, 5), (41, 51)]
    c = Cluster(points)
    print(c.distance((0, 0), (1, 1)))
    for k, v in c.pairs.items():
        print(k, v)
