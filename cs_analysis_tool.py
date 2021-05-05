#script for analysing an existing crosssection
from classes import stiffener
from classes import crosssection
from classes import substantiate
from input import input_analysis_tool
from proofs import buckling_proof
from classes import merge
import initial_cs
import data
import deck
from output import geometry_output
import math
import os
import sys
import defaults


#sys.path.append('C:/Users/Vinzenz Müller/Dropbox/ETH/6. Semester/BA')
#crosssection input and creation (only trapezoid plates)




if defaults.do_print_to_txt == True:
    os.remove("output\cs_analysis.txt")
    file = open("output\cs_analysis.txt", "w+")
    file.write("*************************** cross-section analysis tool ********************************")
    file.close()
if defaults.do_print_to_terminal == True:
    print("*************************** cross-section analysis tool ********************************")


input_analysis_tool.set_defaults()

input_analysis_tool.set_cs_geometry()
#data.check_input_data_complete()
cs = initial_cs.create_initial_cs(data.input_data.get("b_sup"), data.input_data.get("b_inf"), data.input_data.get("h"), data.input_data.get("t_side"), data.input_data.get("t_deck"), data.input_data.get("t_bottom"))

#add the deck stiffeners
st_list_deck = deck.deck(data.input_data.get("b_sup"))
number_st_top = len(st_list_deck.stiffeners)
st_list_deck = substantiate.substantiate(cs, st_list_deck)




#add all other stiffeners
input_analysis_tool.set_stiffeners(number_st_top)
st_list_rest = []
for st in data.stiffener_data.stiffeners:
    y,z = cs.get_coordinates(st.location, st.pl_position)
    if st.pl_position == 2:
        angle = math.pi + cs.get_angle(2)
    if st.pl_position == 3:
        angle = math.pi
    if st.pl_position == 4:
        angle = math.pi - cs.get_angle(2)
    stiffener_i = stiffener.create_stiffener_global(st.pl_position, st.st_number, y, z, angle, \
    st.b_sup, st.b_inf, st.h, st.t)
    st_list_rest.append(stiffener_i)
stiffener_list = st_list_deck + st_list_rest
cs = merge.merge(cs, stiffener_list)
print(cs)
geometry_output.print_cs_red(cs)



#set the cross-sectional forces
input_analysis_tool.set_forces()


#buckling proof
cs = buckling_proof.buckling_proof(cs)
print("eta_1", cs.eta_1)
print("verification 2", cs.interaction_2)
print("verification 3", cs.interaction_3)
print("verification 4", cs.interaction_4)
print(cs)
geometry_output.print_cs_red(cs)
