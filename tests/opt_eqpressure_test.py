import sys
sys.path.append('C:/Users/Vinzenz Müller/Dropbox/ETH/6. Semester/BA')


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
from optimizer import opt_eqpressure


#crosssection input and creation (only trapezoid plates)
input_analysis_tool.set_cs_geometry()
#set forces
input_analysis_tool.set_forces()
#data.check_input_data_complete()
cs = initial_cs.create_initial_cs(data.input_data.get("b_sup"), data.input_data.get("b_inf"), data.input_data.get("h"), data.input_data.get("t_side"), data.input_data.get("t_deck"), data.input_data.get("t_bottom"))

#add the deck stiffeners
deck_stiffener_list = deck.deck(data.input_data.get("b_sup"))


opt_eqpressure.opt_eqpressure(cs, deck_stiffener_list)