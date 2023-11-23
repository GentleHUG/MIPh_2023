"""
Программа бинарного поиска по известному значению отклонения коэффициента преломления
"""
from time import perf_counter_ns
from decimal import Decimal
import CONFIG as C
from Simulation import Simulation
from Visual import Usefuldict

params = C.params

def bin_search(func, params: Usefuldict, target: Decimal, l: Decimal = Decimal(1.), r: Decimal = Decimal(1.8), err: Decimal = Decimal(0.00001)):
    p = params
    c = 0
    t0 = perf_counter_ns()
    while r-l > err:
        c += 1

        m = (l+r) / Decimal(2)
        p.nm = m
        m_value = Simulation.do_sim_with_params(p)

        if m_value == target:
            return m
        elif m_value > target:
            r = m
        else:
            l = m
    print(f'nm = {round((r+l)/2, 4)} was found for {c} steps and {(perf_counter_ns()-t0)} ns=)\n')
    return (r+l) / 2

l = Simulation.do_sim_with_params(params)

print('Value and time for geometric method')
bin_search(Simulation.do_sim_with_params, params, Decimal(0.043715))
print('Value and time for formulaic method')
bin_search(Simulation.find_L_float, params, Decimal(0.043715))
print(l)
