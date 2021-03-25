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
prop_1 = ps.proposed_stiffener(2, 1, 0.67, 10**7)
prop_2 = ps.proposed_stiffener(2, 2, 0.4, 10**7)
prop_3 = ps.proposed_stiffener(3, 3, -0.6, 10**7)
prop_4 = ps.proposed_stiffener(3, 4, -0.3, 10**7)
prop_5 = ps.proposed_stiffener(3, 5, 0, 10**7)
prop_6 = ps.proposed_stiffener(3, 6, 0.3, 10**7)
prop_7 = ps.proposed_stiffener(3, 7, 0.6, 10**7)
prop_8 = ps.proposed_stiffener(4, 8, 0.4, 10**7)
prop_9 = ps.proposed_stiffener(4, 9, 0.67, 10**7)


#add all propositions to a list
prop_list = st_prop.stiffeners_proposition()
prop_list.add(prop_1)
prop_list.add(prop_2)
prop_list.add(prop_3)
prop_list.add(prop_4)
prop_list.add(prop_5)
prop_list.add(prop_6)
prop_list.add(prop_7)
prop_list.add(prop_8)
prop_list.add(prop_9)


end_cs = st.add_stiffener_set(test_cs, prop_list)
go.print_cs(end_cs)

#stiffener_list = ss.substantiate(test_cs, prop_list)
#geometry_ok = st.check_geometry(test_cs, stiffener_list, prop_list)
#go.print_cs_st(test_cs, stiffener_list)
