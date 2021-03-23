import sys
#just add the directory where the BA folder is on your computer
sys.path.append('C:/Users/Nino/Google Drive/Studium/FS 2021/Bachelorarbeit/BA')

from classes import substantiate as ss
from classes import proposed_stiffener as ps
from classes import stiffeners_proposition as st_prop
import initial_cs as ics
from output import geometry_output as go
from classes import stiffener as st

#assign input to variables
b_sup = 4000 #data.input_data["b_sup"]
b_inf = 2000 #data.input_data["b_inf"]
h = 1500 #data.input_data["h"]

#create initial cross section with t=20mm
test_cs = ics.create_initial_cs(b_sup, b_inf, h)
for line in test_cs.lines:
    line.t = 20

#propose stiffeners, mimicking input from optimizer
prop_1 = ps.proposed_stiffener(3, 1, 0.5, 20*10**6)
prop_2 = ps.proposed_stiffener(3, 2, -0.5, 10**7)
prop_3 = ps.proposed_stiffener(2, 1, 0.5, 15*10**6)
prop_4 = ps.proposed_stiffener(4, 1, 0.9, 10**6)
prop_5 = ps.proposed_stiffener(3,1, -0.3, 3*10**6)

#add all propositions to a list
prop_list = st_prop.stiffeners_proposition()
prop_list.add(prop_1)
#prop_list.add(prop_2)
#prop_list.add(prop_3)
#prop_list.add(prop_4)
#prop_list.add(prop_5)

st.add_stiffener_set(test_cs, prop_list)

#stiffener_list = ss.substantiate(test_cs, prop_list)
#go.print_cs(test_cs, stiffener_list)
