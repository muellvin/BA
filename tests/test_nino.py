#This is a test script

import sys
#just add the directory where the BA folder is on your computer
sys.path.append('C:/Users/Nino/Google Drive/Studium/FS 2021/Bachelorarbeit/BA')


from classes import point
from classes import line
from classes import crosssection
from output import geometry_output as go


a = point.point(0,0)
b = point.point(0,2)
e = point.point(2,0)
d = point.point(2,2)
line1 = line.line(0,a,b,1)
line2 = line.line(0,e,d,1)

test_cs = crosssection.crosssection()
test_cs.addline(line1)
test_cs.addline(line2)

go.print_cs(test_cs)

#test
