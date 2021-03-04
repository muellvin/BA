#file for helping testing code

import classes as c

a = c.point(0,0)
b = c.point(0,100)
line = c.line(0,a,b,10)
l = line.get_length_tot()
area = line.get_area_tot()
iy = line.get_iy_tot()
iz = line.get_iz_tot()

print(l)
print(area)
print(iy)
print(iz)
