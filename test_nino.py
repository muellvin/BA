#This is a test script
from classes import crosssection
from classes import line
from classes import point

a = gc.point(0,0)
b = gc.point(0,2)
e = gc.point(2,0)
d = gc.point(2,2)
line1 = gc.line(0,a,b,1)
line2 = gc.line(0,e,d,1)

test_cs = cs.crosssection()
test_cs.addline(line1)
test_cs.addline(line2)

y = test_cs.get_y_center_tot()
z = test_cs.get_z_center_tot()
a = test_cs.get_area_tot()
print(a)
print(y)
print(z)

#test
