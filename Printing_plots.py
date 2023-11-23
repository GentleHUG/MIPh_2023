"""
Программа с функциями для отображения графиков
"""
import csv
import matplotlib.pyplot as plt
import numpy as np
import DEFAULT
from Simulation import Simulation
from decimal import Decimal, getcontext

context = getcontext()
context.prec = 10

fig, ax = plt.subplots()

par_name = 'd1'
ranging = [2, 4, 6, 8, 10]
title=f'Зависимось от параметра {par_name}'

params = DEFAULT.params

for i in ranging:
    data = {}
    params[par_name] = Decimal(i)
    y_arr = [Decimal(1) + Decimal(0.0001) * Decimal(i) for i in range(10000)]
    for nm in y_arr:
        try:
            params.nm = nm
            data[nm] = Simulation.do_sim_with_params(params)
        except Exception:
            pass
    ax.plot(data.values(), data.keys(), label=f'{par_name}={i}, mm')
    print(f'Sim for {par_name}={i} was ended')

ax.set_ylabel('nm')
ax.set_xlabel('L, mm')
ax.legend()
ax.set_title(title)
plt.savefig(f'{title}.png')