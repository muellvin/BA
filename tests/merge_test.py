import sys
import os

#just add the directory where the BA folder is on your computer
sys.path.append('C:/Users/Nino/Google Drive/Studium/FS 2021/Bachelorarbeit/BA')

import initial_cs as ics
import math
from classes import stiffener as st
from output import geometry_output as go
from classes import point as pt
from classes import line as ln
from classes import plate_code as plcd
from classes import crosssection as cs
import deck

initial_cs = ics.create_initial_cs(4000, 3000, 2000, 20, 20, 20)
#stiffener_1 = st.create_stiffener_global(1, 1, 1000, 0, 0, 300, 200, 200, 15)
#stiffener_2 = st.create_stiffener_global(1, 2, -1000, 0, 0, 300, 200, 200, 15)
#stiffener_3 = st.create_stiffener_global(2, 3, -2000, 1000, 3*math.pi/2, 200, 100, 100, 10)
#stiffener_4 = st.create_stiffener_global(3, 4, -1000, 2000, math.pi, 300, 200, 200, 15)
#stiffener_5 = st.create_stiffener_global(3, 5, 1000, 2000, math.pi, 300, 200, 200, 15)
#stiffener_6 = st.create_stiffener_global(4, 6, 2000, 1000, math.pi/2, 200, 100, 100, 10)

stiffener_list = []
#deck.deck(4000)
final_cs = st.merge(initial_cs, stiffener_list)
for line in final_cs.lines:
    print("Line:  " + str(line.a) + " " + str(line.b))
    print(str(line.code))
go.print_cs_red(final_cs)
