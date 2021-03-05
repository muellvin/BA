#This is a test script

from classes import point
from classes import line
from classes import crosssection

a = point.point(0,0)
b = point.point(0,2)
e = point.point(2,0)
d = point.point(2,2)
line1 = point.line(0,a,b,1)
line2 = point.line(0,e,d,1)

test_cs = crosssection.crosssection()
test_cs.addline(line1)
test_cs.addline(line2)

y = test_cs.get_center_y_tot()
z = test_cs.get_center_z_tot()
a = test_cs.get_area_tot()
print(a)
print(y)
print(z)

#test
