import random
import _random
import numpy as np
import matplotlib.pyplot as plt

n = 4  # количество состояний


# таблица состояний

conversion_table3 = {
    (0, 0): 0.2, (0, 1): 0.5, (0, 2): 0.3, (0, 3): 0,
    (1, 0): 0.7, (1, 1): 0, (1, 2): 0.3, (1, 3): 0,
    (2, 0): 0.6, (2, 1): 0, (2, 2): 0, (2, 3): 0.4,
    (3, 0): 0, (3, 1): 0, (3, 2): 0, (3, 3): 1
}

sum_days = 0
m = 1000

seasons = []
r = _random.Random()
for l in range(0, m):

    season_number = 0
    s_cur = (0, 0)
    x = 0

    fl = False

    while s_cur[0] < 3:
        i, j = s_cur

        p_array = r.random()

        if s_cur == (0, 0):
            season_number += 1

        p = 0
        delta = 0

        for k in range(0, n):
            p = p + conversion_table3[i, k]
            delta = k
            if p_array <= p:
                break


        s_cur = (delta, 0)
        x += 1

    sum_days += season_number
    seasons.append(season_number)


print(sum_days / m)

fig, ax = plt.subplots()
ax.scatter([i for i in range(1, len(seasons)+1)], seasons, c = 'deeppink')
plt.show()
