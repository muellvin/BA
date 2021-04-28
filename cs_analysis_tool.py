#script for analysing an existing crosssection
from classes import stiffener
from classes import crosssection
from input import input_analysis_tool
from proofs import buckling_proof
import initial_cs
import data
import deck
from output import geometry_output
import math


#crosssection input and creation (only trapezoid plates)
print("*************************** cross-section analysis tool ********************************")
input_analysis_tool.set_cs_geometry()
#data.check_input_data_complete()
cs = initial_cs.create_initial_cs(data.input_data.get("b_sup"), data.input_data.get("b_inf"), data.input_data.get("h"), data.input_data.get("t_side"), data.input_data.get("t_deck"), data.input_data.get("t_bottom"))

#add the deck stiffeners
deck_stiffener_list = deck.deck(data.input_data.get("b_sup"))
cs = stiffener.merge(cs, deck_stiffener_list)
number_stplates_top = 0
for plate in cs.lines:
    if plate.code.pl_type == 1:
        number_stplates_top += 1
assert number_stplates_top%3 == 0; "wattt"
number_st_top= number_stplates_top/3




#add all other stiffeners
input_analysis_tool.set_stiffeners(number_st_top)
stiffener_list = []
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
    stiffener_list.append(stiffener_i)
cs = stiffener.merge(cs, stiffener_list)

geometry_output.print_cs_red(cs)



#set the cross-sectional forces
input_analysis_tool.set_forces()


#buckling proof
cs = buckling_proof.buckling_proof(cs)

geometry_output.print_cs_red(cs)
