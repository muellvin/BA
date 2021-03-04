#file for helping testing code

import classes as c

a = c.point(0,0)
b = c.point(20,100)
e = c.point(0,0)
d = c.point(20,-100)
line1 = c.line(0,a,b,10)
line2 = c.line(0,e,d,10)

iy1 = line1.get_iy_tot()
iz1 = line1.get_iz_tot()
iy2 = line2.get_iy_tot()
iz2 = line2.get_iz_tot()


print(iy1)
print(iz1)
print(iy2)
print(iz2)
