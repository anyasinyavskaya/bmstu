import tkinter as tk
import matplotlib
import matplotlib.pyplot as plt
import random
import matplotlib.tri as mtri
from random import randrange, sample
from itertools import chain
from mpl_toolkits.mplot3d import Axes3D
from delaunay_triangulation import *
from perlin import *
import numpy as np


def line_plotter(points_list, noise):
    set_triangles = set()
    triangles = delaunay_triangulation(points_list)

    for (a, b), c in triangles.items():
        if (b, c) in triangles:
            tr = frozenset([a, c, b])
            set_triangles.add(tr)

    dots = {}
    triangulation_points = points_list
    triangulation_triangles = []
    triangulation_z = []
    for i in range(0, len(points_list)):
        dots[points_list[i]] = i
        triangulation_z.append(noise[points_list[i][0], points_list[i][1]])

    for triangle in set_triangles:
        list_dots = []
        for point in triangle:
            list_dots.append(dots[point])
        triangulation_triangles.append(list_dots)

    draw_triangulation(triangulation_points, triangulation_triangles)
    draw_triangulation_3d(triangulation_points, triangulation_triangles, triangulation_z)


def draw_triangulation(p, t):
    points = np.array(p)
    triangles = np.array(t)
    tri = mtri.Triangulation(points[:, 0], points[:, 1], triangles)
    fig, ax = plt.subplots()
    ax.triplot(tri, 'bo-', lw=1)
    ax.set_title("Трингуляция Делоне методом 'Разделяй и властвуй'")
    plt.show()


def draw_triangulation_3d(p, t, z):
    points = np.array(p)
    triangles = np.array(t)
    tri = mtri.Triangulation(points[:, 0], points[:, 1], triangles)
    ax = plt.figure().gca(projection='3d')
    ax.plot_trisurf(tri, z, cmap='viridis', edgecolor='none')
    plt.show()


def generate_points(n, borne):
    points = set()
    x, y = randrange(borne), randrange(borne)
    for i in range(n):
        while (x, y) in points:
            x, y = randrange(borne), randrange(borne)
        points.add((x, y))
    return list(points)


set_triangles = set()
triangles_w_height = []

n = 100
p_list = generate_points(n, 650)
p_list_2 = generate_points(2 * n, 650)
p_list_3 = generate_points(3 * n, 650)

frameSize = 700
noise_1 = {}
noise_2 = {}
noise_3 = {}
PNFactory = PerlinGenerator(2)
for (i, j) in p_list:
    noise_1[i, j] = PNFactory(i / frameSize, j / frameSize)
    noise_1[i, j] = 10 * abs(noise_1[i, j])

for (i, j) in p_list_2:
    noise_2[i, j] = PNFactory(i / frameSize, j / frameSize)
    noise_2[i, j] = 10 * abs(noise_2[i, j])

for (i, j) in p_list_3:
    noise_3[i, j] = PNFactory(i / frameSize, j / frameSize)
    noise_3[i, j] = 10 * abs(noise_3[i, j])

p_list_2 = p_list + p_list_2
p_list_3 = p_list_2 + p_list_3
noise_new1 = {**noise_1, **noise_2}
noise_new2 = {**noise_new1, **noise_3}
line_plotter(p_list, noise_1)
line_plotter(p_list_2, noise_new1)
line_plotter(p_list_3, noise_new2)
