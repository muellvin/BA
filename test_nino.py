import classes as cl

a = cl.point(2,3)
b = cl.point(2,0)
c = cl.point(0,3)
d = cl.point(0,0)

line1 = cl.line(0,a,b,1)
line2 = cl.line(0,c,d,1)

cs = cl.crosssection()
cs.addline(line1)
cs.addline(line2)

y = cs.get_y_center_tot()
z = cs.get_z_center_tot()

a = cs.get_area_tot()

print(y)
print(z)
print(a)
