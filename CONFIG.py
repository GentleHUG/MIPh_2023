"""
Файл с параметрами кюветы
"""
from decimal import *
import Visual as vs

contex = getcontext()
contex.prec = 15

a = Decimal(50)
b = Decimal(50)
d = Decimal(0.5)
d1 = Decimal(1)
e = Decimal(20)
y = Decimal(4)
ns = Decimal(1.437762)
nq = Decimal(1.537826)
na = Decimal(1.000273)
nm = Decimal(1.5)

params = vs.Usefuldict(a=a, b=b, d=d, d1=d1, e=e, y=y, ns=ns, nq=nq, na=na, nm=nm)
