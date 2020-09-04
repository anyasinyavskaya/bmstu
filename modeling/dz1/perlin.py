from itertools import product
import math
import random
from random import randrange, sample


class PerlinGenerator(object):

    def __init__(self, octaves=2, tile=()):
        self.octaves = octaves
        self.dimension = 2
        self.tile = tile + (0,) * 2
        self.scale = 2 * pow(2, -0.5)
        self.gradient = {}

    def find_gradient(self):
        if self.dimension == 1:
            return (random.uniform(-1, 1),)

        random_point = [random.gauss(0, 1) for _ in range(self.dimension)]
        scale = sum(n * n for n in random_point) ** -0.5
        return tuple(coord * scale for coord in random_point)

    def dot_noise(self, *point):
        tr_coords = []
        for x in point:
            min = math.floor(x)
            max = min + 1
            tr_coords.append((min, max))

        dots = []
        for tr_point in product(*tr_coords):
            if tr_point not in self.gradient:
                self.gradient[tr_point] = self.find_gradient()
            gradient = self.gradient[tr_point]

            dot = 0
            for i in range(self.dimension):
                dot += gradient[i] * (point[i] - tr_point[i])
            dots.append(dot)

        dim = self.dimension
        while len(dots) > 1:
            dim -= 1
            s = smooth_step(point[dim] - tr_coords[dim][0])

            future_dots = []
            while dots:
                future_dots.append(linear_interpolation(s, dots.pop(0), dots.pop(0)))

            dots = future_dots

        return dots[0] * self.scale

    def __call__(self, *point):
        x = 0
        for octave in range(self.octaves):
            octave2 = 1 << octave
            new_point = []
            for i, coord in enumerate(point):
                coord *= octave2
                if self.tile[i]:
                    coord %= self.tile[i] * octave2
                new_point.append(coord)
            x += self.dot_noise(*new_point) / octave2

        x /= 2 - 2 ** (1 - self.octaves)

        return x


def smooth_step(t):
    return t * t * (3. - 2. * t)


def linear_interpolation(t, a, b):
    return a + t * (b - a)
