import math
import os
import sys
from assembly import add_stiffeners
from assembly import substantiate
from assembly import merge
from classes import crosssection
from proofs_and_stress_calculation import buckling_proof
from deck_and_initial_cs import deck
from deck_and_initial_cs import initial_cs
from data_and_defaults import data
from data_and_defaults import defaults
from output import geometry_output
from user_interface import cs_to_html
sys.path.insert(0, './user_interface')
from output import printing


#sys.path.append('C:/Users/Vinzenz Müller/Dropbox/ETH/6. Semester/BA')
#crosssection input and creation (only trapezoid plates)




#if defaults.do_print_to_txt == True:
#    os.remove("output\cs_analysis.txt")
#    file = open("output\cs_analysis.txt", "w+")
#    file.write("*************************** cross-section analysis tool ********************************")
#    file.close()

def cs_analysis_gui():

    file = open("user_interface\output\cs_analysis.txt", "w+")
    file.close()

    cs_cs_position = "neither"
    data.input_data.update({"cs position": cs_cs_position})

    cs = initial_cs.create_initial_cs(data.input_data.get("b_sup"), data.input_data.get("b_inf"), data.input_data.get("h"), data.input_data.get("t_side"), data.input_data.get("t_deck"), data.input_data.get("t_bottom"))

    #add the deck stiffeners
    st_list_deck = deck.deck(data.input_data.get("b_sup"))


    #add all other stiffeners
    st_list_rest = []
    for st in data.stiffener_data.stiffeners:
        y,z = cs.get_coordinates(st.location, st.pl_position)
        if st.pl_position == 2:
            angle = math.pi + cs.get_angle(2)
        if st.pl_position == 3:
            angle = math.pi
        if st.pl_position == 4:
            angle = math.pi - cs.get_angle(2)
        stiffener_i = add_stiffeners.create_stiffener_global(st.pl_position, st.st_number, y, z, angle, \
        st.b_sup, st.b_inf, st.h, st.t)
        st_list_rest.append(stiffener_i)
    stiffener_list = st_list_deck + st_list_rest
    stiffener_list = sorted(stiffener_list, key = lambda st: st.lines[0].code.st_number)
    cs = merge.merge(cs, stiffener_list)
    print(cs)


    #buckling proof
    cs = buckling_proof.buckling_proof(cs)
    results = {"eta_1": round(cs.eta_1,2), "eta_3_side_1":round(cs.eta_3_side_1,2), "interaction_1": round(cs.interaction_1,2),  "eta_3_side_2":round(cs.eta_3_side_2,2), \
    "interaction_2": round(cs.interaction_2,2), "eta_3_side_3":round(cs.eta_3_side_3,2), "interaction_3": cs.interaction_3, "eta_3_side_4":round(cs.eta_3_side_4,2), "interaction_4": cs.interaction_4}
    image = cs_to_html.print_cs_red(cs)
    results.update({"image": image})
    printing.txt_to_pdf(cs, "cs")
    return results
