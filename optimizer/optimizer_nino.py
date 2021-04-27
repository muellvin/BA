import math
from classes import crosssection
import initial_cs as ics
import deck
import copy
from classes import stiffener
from classes import proposed_stiffener
from classes import stiffeners_proposition
from classes import substantiate
from output import geometry_output as go
from proofs import local_buckling
from proofs import column_buckling
from proofs import shear_lag
from proofs import resistance_to_shear
from proofs import global_buckling
from proofs import interaction
from proofs import buckling_proof
import defaults
import data
from proofs import stress_cal

#optimization step 1
#the goal of this method is to create
def optimize():
    b_sup = data.input_data["b_sup"]
    b_inf = data.input_data["b_inf"]
    h = data.input_data["h"]
    t_deck = data.input_data["t_deck"]
    t_range = [5]
    I_range = [3*10**7, 6*10**7]
    base_css = []
    "Use correct stiffener numbers!!!"

    deck_stiffeners = deck.deck(b_sup)
    cs_collection = set()
    num_top_stiffeners = len(deck_stiffeners)
    m_ed = data.input_data.get("M_Ed")
    sign = math.copysign(1, m_ed)
    for t_side in t_range:
        for t_bottom in t_range:
            initial_cs = ics.create_initial_cs(b_sup, b_inf, h, t_side, t_deck, t_bottom)
            base_cs = stiffener.merge(initial_cs, deck_stiffeners)
            for num_side_stiffeners in range(2):
                for num_btm_stiffeners in range(4):
                    for I_a in I_range:
                        prop = stiffeners_proposition.stiffeners_proposition()
                        for num in range(num_side_stiffeners):
                            #create side stiffeners
                            loc = 0
                            if num_side_stiffeners == 1:
                                if sign > 0:
                                    loc = 5/6
                                else:
                                    loc = 1/6
                            st_number_right = num_top_stiffeners + num + 1
                            st_number_left = num_top_stiffeners + num_btm_stiffeners + 2*num_side_stiffeners - num
                            st_right = proposed_stiffener.proposed_stiffener(pl_position = 2, st_number = st_number_right, location = loc, i_along = I_a)
                            st_left = proposed_stiffener.proposed_stiffener(pl_position = 4, st_number = st_number_left, location = loc, i_along = I_a)
                            prop.stiffeners.append(st_right)
                            prop.stiffeners.append(st_left)
                            #create bottom siffeners
                        for num in range(num_btm_stiffeners):
                            loc = 1 - 2/(num_btm_stiffeners+1)*(num+1)
                            st_number = num_top_stiffeners + num_side_stiffeners + num + 1
                            st = proposed_stiffener.proposed_stiffener(pl_position = 3, st_number = st_number, location = loc, i_along = I_a)
                            prop.stiffeners.append(st)
                        base_cs_copy = copy.deepcopy(base_cs)
                        st_list = substantiate.substantiate(base_cs_copy, prop)
                        test_cs = stiffener.merge(base_cs_copy, st_list)
                        end_cs = buckling_proof.buckling_proof(test_cs)
                        proven = end_cs.eta_1 < 1 and end_cs.interaction_2 < 1 and end_cs.interaction_3 < 1 and end_cs.interaction_4 < 1
                        if proven:
                            cs_collection.add(end_cs)
    print("# of passed CS")
    print(len(cs_collection))
    for cs in cs_collection:
        go.print_cs(cs)
