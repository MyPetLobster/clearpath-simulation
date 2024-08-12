from config import PEDESTRIAN_BASE_SPEED

class Pedestrian:
    def __init__(self, x, y, speed=PEDESTRIAN_BASE_SPEED):
        self.x = x
        self.y = y
        self.speed = speed

    def move(self):
        pass

    def draw(self, win):
        pass
