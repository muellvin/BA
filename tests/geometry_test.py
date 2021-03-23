#first version of geometry output using matplotlib

import sys
#just add the directory where the BA folder is on your computer
sys.path.append('C:/Users/Nino/Google Drive/Studium/FS 2021/Bachelorarbeit/BA')

#imports
import matplotlib.pyplot as plt
import numpy as np
import initial_cs as ics
from classes import crosssection as cs
from classes import point
from classes import line as ln
from output import geometry_output as go

test_cs = ics.create_initial_cs(1000,500,400)
stiffener = cs.crosssection()

code = (0,0,0,0,0)

a = point.point(100,0)
b = point.point(50,50)
c = point.point(-50,50)
d = point.point(-100,0)
e = point.point(100,400)
f = point.point(50,350)
g = point.point(-50,350)
h = point.point(-100,400)


stiffener.addline(ln.line(code,a,b,1))
stiffener.addline(ln.line(code,b,c,1))
stiffener.addline(ln.line(code,c,d,1))
stiffener.addline(ln.line(code,e,f,1))
stiffener.addline(ln.line(code,f,g,1))
stiffener.addline(ln.line(code,g,h,1))

go.print_cs(test_cs, stiffener)
