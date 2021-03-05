#file for helping testing code

from classes import line as l
from classes import point as p

a = p.point(0,0)
b = p.point(20,100)
c = p.point(0,0)
d = p.point(20,-100)
line1 = l.line(0,a,b,1)
line2 = l.line(0,c,d,1)

iy1 = line1.get_iy_tot()
iz1 = line1.get_iz_tot()
iy2 = line2.get_iy_tot()
iz2 = line2.get_iz_tot()


print(iy1)
print(iz1)
print(iy2)
print(iz2)
