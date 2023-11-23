"""
Программа сравнивает решение с помощью симуляции с решением с помощью формулы
"""
import Visual as vs
import CONFIG as cg
import math as m
from decimal import Decimal, getcontext
from Simulation import Simulation
from time import perf_counter_ns

context = getcontext()
context.prec = 15

params = vs.Usefuldict(a=cg.a, b=cg.b, d=cg.d, d1=cg.d1, e=cg.e, y=cg.y, ns=cg.ns, nq=cg.nq, na=cg.na, nm=cg.nm)


def find_L(par: vs.Usefuldict):
    a1 = m.atan(par.a/par.b)
    b1 = m.asin(Decimal(m.sin(a1))*par.ns/par.nq)
    a2 = b1
    b2 = m.asin(Decimal(m.sin(a2))*par.nq/par.nm)
    a3 = a1-b2

    b3 = m.asin(Decimal(m.sin(a3))*par.nm/par.nq)
    a4 = b3
    b4 = m.asin(Decimal(m.sin(a4))*par.nq/par.na)

    k1 = Decimal(m.tan(a1))*(par.y-(par.d/2/Decimal(m.sin(a1)))+par.d*Decimal(m.sin(a1-b1))/Decimal(m.cos(b1)))

    l1 = par.e*Decimal(m.tan(b4))
    l2 = par.d1*Decimal(m.tan(b3))
    l3 = k1*Decimal(m.tan(a3))
    l4 = par.d * Decimal(m.sin(a1 - b1) / m.cos(b1))

    return l1+l2+l3+l4

def find_L_float(args: vs.Usefuldict):
    par = vs.Usefuldict()
    for key in args:
        par[key] = float(args[key])
    a1 = m.atan(par.a/par.b)
    b1 = m.asin(m.sin(a1)*par.ns/par.nq)
    a2 = b1
    b2 = m.asin(m.sin(a2)*par.nq/par.nm)
    a3 = a1-b2

    b3 = m.asin(m.sin(a3)*par.nm/par.nq)
    a4 = b3
    b4 = m.asin(m.sin(a4)*par.nq/par.na)

    k1 = m.tan(a1)*(par.y-(par.d/2/m.sin(a1))+par.d*m.sin(a1-b1)/m.cos(b1))

    l1 = par.e*m.tan(b4)
    l2 = par.d1*m.tan(b3)
    l3 = k1*m.tan(a3)
    l4 = par.d*m.sin(a1-b1)/m.cos(b1)

    return l1+l2+l3+l4

t1 = perf_counter_ns()
print(find_L_float(params))
print(perf_counter_ns() - t1)
print('-------')
t2 = perf_counter_ns()
print(Simulation.do_sim_with_params(params))
print(perf_counter_ns() - t2)