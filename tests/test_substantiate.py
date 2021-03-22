import sys
#just add the directory where the BA folder is on your computer
sys.path.append('C:/Users/Nino/Google Drive/Studium/FS 2021/Bachelorarbeit/BA')

from optimizer import substantiate as ss
from classes import proposed_stiffener as ps
from classes import stiffeners_proposition as st_prop
import initial_cs as ics

#assign input to variables
b_sup = 4000 #data.input_data["b_sup"]
b_inf = 2000 #data.input_data["b_inf"]
h = 1500 #data.input_data["h"]

#create initial cross section with t=20mm
test_cs = ics.create_initial_cs(b_sup, b_inf, h)
for line in test_cs.lines:
    line.t = 20

#propose stiffeners, mimicking input from optimizer
prop_1 = ps.proposed_stiffener(3,1,0,20*10**6)

#add all propositions to a list
prop_list = st_prop.stiffeners_proposition()
prop_list.add(prop_1)

stiffener_list = ss.substantiate(test_cs, prop_list)
