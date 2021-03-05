#file for helping testing code

from classes import line as l
from classes import point as p

a = p.point(0,0)
b = p.point(20,100)
c = p.point(0,0)
d = p.point(20,-100)
line1 = l.line(0,a,b,1)
line2 = l.line(0,c,d,1)

iy1 = line1.get_i_y_tot()
iz1 = line1.get_i_z_tot()
iy2 = line2.get_i_y_tot()
iz2 = line2.get_i_z_tot()

iyrotred201 = line1.get_i_rot_red(20)
iyrottot201 = line1.get_i_rot_tot(20)
areared1 = line1.get_area_red()

print(iy1)
print(iz1)
print(iy2)
print(iz2)
print(iyrotred201)
print(iyrottot201)
print(areared1)
