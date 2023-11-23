"""
Файл с параметрами кюветы, использованными для симуляций, представленных в презентации
"""
from decimal import *
import Visual as vs

contex = getcontext()
contex.prec = 15

a = Decimal(50)
b = Decimal(40)
d = Decimal(2.5)
d1 = Decimal(5)
e = Decimal(5)
y = Decimal(20)
ns = Decimal(1.2)
nq = Decimal(1.4584)
na = Decimal(1.0002926)
nm = Decimal(1.)

params = vs.Usefuldict(a=a, b=b, d=d, d1=d1, e=e, y=y, ns=ns, nq=nq, na=na, nm=nm)
