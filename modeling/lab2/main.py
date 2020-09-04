import numpy as np
import matplotlib.pyplot as plt
import pickle as pkl
import time
from scipy import ndimage
import copy
import random
import math

p1 = 0.05
p2 = 0.01

dict_pirson = {0.64: p1, 0.79: p2}

l = 1.8
n = 8
k = 10

patients = []


def exprand(l):
    return -math.log(1.0 - random.random()) / l


signs_matrice = []
signs_dict = {}

# заполнение

for i in range(0, n):
    patient = {}
    signs = {}
    for j in range(0, k):
        y = random.random()
        signs[y] = 0
    signs_dict[i] = signs

for x in signs_dict.values():
    print(x.keys())

# ранг

for j in range(0, n):
    list_keys = list(signs_dict[j].keys())
    list_keys.sort()
    # print(list_keys)
    rang = 1
    signs_dict[j][list_keys[0]] = rang
    for i in range(1, len(list_keys)):
        if list_keys[i] == list_keys[i - 1]:
            signs_dict[j][list_keys[i]] = rang
        else:
            rang = rang + 1
            signs_dict[j][list_keys[i]] = rang

for j in range(0, n):
    print(signs_dict[j])

# корреляция
correlation_matrix = [[0 for i in range(0, n)] for j in range(0, n)]

for i in range(0, n):
    for j in range(0, n):
        if i == j:
            correlation_matrix[i][j] = 1

for j in range(0, n - 1):
    dispersion = []
    print()
    for i in range(1, n - j):
        r = []
        s = []
        sum_rs = 0
        for rang in signs_dict[j].values():
            r.append(rang)
        for rang in signs_dict[j + i].values():
            s.append(rang)
        for t in range(0, len(r)):
            sum_rs = sum_rs + pow(r[t] - s[t], 2)

        correlation_matrix[j][j + i] = sum_rs
        correlation_matrix[j + i][j] = sum_rs

for i in range(0, n):
    for j in range(0, n):
        correlation_matrix[i][j] = 1 - (6 / (k * (k ** 2 - 1))) * correlation_matrix[i][j]

print(correlation_matrix)

correlation_coefs = []
correlation_dict = {}
for i in range(0, n):
    for j in range(i + 1, n):
        correlation_dict[abs(correlation_matrix[i][j])] = (i, j)
        correlation_coefs.append(correlation_matrix[i][j])

print(correlation_dict)

list_keys = list(correlation_dict.keys())
list_keys.sort()

print(list_keys)

glav_1 = list_keys[len(list_keys) - 1]
signs1 = correlation_dict[glav_1]
glav_2 = list_keys[len(list_keys) - 2]
signs2 = correlation_dict[glav_2]
glav_3 = list_keys[len(list_keys) - 3]
signs3 = correlation_dict[glav_3]

print(glav_1)
print(glav_2)
print(glav_3)

u1 = 0
u2 = 0
u3 = 0

for x in dict_pirson.keys():
    if glav_1 >= x:
        u1 = dict_pirson[x]
for x in dict_pirson.keys():
    if glav_2 >= x:
        u2 = dict_pirson[x]
for x in dict_pirson.keys():
    if glav_3 >= x:
        u3 = dict_pirson[x]

print(u1, u2, u3)

res = {u1: signs1, u2: signs2, u3: signs3}
for u in res.keys():
    if u>0:
        print("Зависимые признаки на уровне значимости ", u, " : ", res[u])
