import sys
import os

#just add the directory where the BA folder is on your computer
sys.path.append('C:/Users/Nino/Google Drive/Studium/FS 2021/Bachelorarbeit/BA')

import initial_cs as ics
from classes import stiffener as st
from output import geometry_output as go
from classes import point as pt
from classes import line as ln
from classes import plate_code as plcd
from classes import crosssection as cs
from proofs import global_plate_buckling as glb
import data
import math

data.input_data.update({"M_Ed": -45000*10**6})

initial_cs = ics.create_initial_cs(4000, 3000, 2000, 10, 10, 5)
stiffener_1 = st.create_stiffener_global(3, 1, -1000, 2000, math.pi, 200, 150, 100, 5)
stiffener_2 = st.create_stiffener_global(3, 2, 1000, 2000, math.pi, 200, 150, 100, 5)


stiffener_list = [stiffener_1, stiffener_2]
final_cs = st.merge(initial_cs, stiffener_list)
final_cs = initial_cs

point_a = pt.point(-1500, 2000)
point_b = pt.point(1500, 2000)
code = plcd.plate_code(3,0,3,0,0)
plate = ln.line(code, point_a, point_b, 5)
x_sec = ics.create_initial_cs(4000, 3000, 2000, 10, 10, 5)
stiffened_plate = st.merge(x_sec, stiffener_list)
x_sec.lines.remove(x_sec.get_pl_line(1))
x_sec.lines.remove(x_sec.get_pl_line(2))
x_sec.lines.remove(x_sec.get_pl_line(4))

glb.global_plate_buckling(final_cs, stiffened_plate)
