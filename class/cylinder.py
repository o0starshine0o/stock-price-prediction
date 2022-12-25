import math
import random
import time


def spend(func):
    def calc_time(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        print(f'{func.__name__} spend: {time.time() - start} second')

    return calc_time


class Cylinder:
    def __init__(self, radius: float | int, height: float | int):
        self.radius = radius
        self.height = height

    def PrintInfo(self):
        print(f"radius: {self.radius}, height: {self.height}")

    def GetVolume(self) -> float:
        return math.pi * (self.radius ** 2) * self.height


@spend
def delete(cylinders: list):
    while len(cylinders):
        index = random.randint(0, 9)
        if len(cylinders) > index:
            del cylinders[index]


if __name__ == "__main__":
    delete([Cylinder(index, index) for index in range(10)])
