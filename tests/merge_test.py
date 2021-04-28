import sys
import os

#just add the directory where the BA folder is on your computer
sys.path.append('C:/Users/Nino/Google Drive/Studium/FS 2021/Bachelorarbeit/BA')
#sys.path.append('C:/Users/Vinzenz Müller/Dropbox/ETH/6. Semester/BA')

import initial_cs as ics
import math
from classes import stiffener as st
from output import geometry_output as go
from classes import point as pt
from classes import line as ln
from classes import plate_code as plcd
from classes import crosssection as cs
from classes import merge
import deck

initial_cs = ics.create_initial_cs(4000, 4000, 2000, 20, 20, 20)

st_list_deck = deck.deck(4000)
intermediate_cs = merge.merge(initial_cs, st_list_deck)


stiffener_1 = st.create_stiffener_global(2, 1, -2000, 1000, 3*math.pi/2, 200, 100, 100, 10)
stiffener_2 = st.create_stiffener_global(3, 2, -1000, 2000, math.pi, 300, 200, 200, 15)
stiffener_3 = st.create_stiffener_global(3, 3, 1000, 2000, math.pi, 300, 200, 200, 15)
stiffener_4 = st.create_stiffener_global(4, 4, 2000, 1000, math.pi/2, 200, 100, 100, 10)


stiffener_list = [stiffener_1, stiffener_2, stiffener_3, stiffener_4]
stiffener_list.append(stiffener_1)
stiffener_list.append(stiffener_2)
stiffener_list.append(stiffener_3)
stiffener_list.append(stiffener_4)


#deck.deck(4000)
#final_cs = merge.merge(initial_cs, stiffener_list)
print(intermediate_cs)
go.print_cs_red(intermediate_cs)
print(len(intermediate_cs.lines))
