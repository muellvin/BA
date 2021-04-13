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
from proofs import global_buckling as glb

initial_cs = ics.create_initial_cs(4000, 3000, 2000, 20, 20, 20)
stiffener_1 = st.create_stiffener_global(3, 1, -1000, 2000, 0, 300, 200, 200, 15)
stiffener_2 = st.create_stiffener_global(3, 2, 1000, 2000, 0, 300, 200, 200, 15)


stiffener_list = [stiffener_1, stiffener_2]
final_cs = st.merge(initial_cs, stiffener_list)
for line in final_cs.lines:
    print("Line:  " + str(line.a) + " " + str(line.b))
go.print_cs(final_cs)
