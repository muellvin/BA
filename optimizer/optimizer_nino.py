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
    t_range = [5,10]
    I_range = [3*10**7, 6*10**7, 9*10**7]
    base_css = []

    deck_stiffeners = deck.deck(b_sup)
    for t_side in t_range:
        for t_bottom in t_range:
            initial_cs = ics.create_initial_cs(b_sup, b_inf, h, t_side, t_deck, t_bottom)
            base_cs = stiffener.merge(initial_cs, deck_stiffeners)
            #find required number of stiffeners in bottom plate
            #only with elastic shear lag for the moment
            utilisation = prove_bottom_plate(base_cs)
            print("Utilisation")
            print(utilisation)
            number_of_btm_stiffeners = 0
            test_cs = copy.deepcopy(base_cs)
            while utilisation > 1 or number_of_btm_stiffeners < 6:
                number_of_btm_stiffeners += 1
                while utilisation > 1 or I_index < len(I_range):
                    prop = stiffeners_proposition.stiffeners_proposition()
                    for i in range(number_of_btm_stiffeners):
                        loc = 1 - 2/(number_of_btm_stiffeners+1)*i
                        st = proposed_stiffener.proposed_stiffener(pl_position = 3, st_number = i, location = loc, i_along = I_range[i])
                        prop.stiffeners.append(st)
                    base_cs_copy = copy.deepcopy(base_cs)
                    st_list = substantiate(x_sec, prop)
                    test_cs = stiffener.merge(base_cs_copy, st_list)
                    utilisation = prove_bottom_plate(test_cs)
                    print("Utilisation")
                    print(utilisation)
            base_cs = test_cs
            go.print_cs(base_cs)
            #find optimal solution for stiffeners in side plates
            #tbd

def prove_bottom_plate(cs):
    #3.2 shear lag elastically
    #cs = shear_lag.shear_lag(cs)
    #4.4 plate elements without longitudinal stiffeners
    cs = local_buckling.local_buckling(cs)
    #4.5 stiffened plate elements with longitudinal stiffeners
    cs = global_buckling.global_buckling(cs)
    #4.6 verification
    m_rd_eff = cs.get_m_rd_el_eff()
    plate_glob = cs.get_stiffened_plate(side = 3)
    #interaction
    V_Ed_plate = stress_cal.get_tau_int_flange(cs, 3, data.input_data.get("V_Ed"),\
    data.input_data.get("T_Ed"))
    eta_3 = resistance_to_shear.resistance_to_shear(plate_glob, V_Ed_plate)
    utilisation = interaction.interaction_flange(cs, plate_glob, eta_3)
    return utilisation
