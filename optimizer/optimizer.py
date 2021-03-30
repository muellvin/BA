import math
from classes import crosssection as cs
import initial_cs as ics


#optimization step 1
#the goal of this method is to create
def step_1(start_cs):
    b_sup = data.input_data[b_sup]
    b_inf = data.input_data[b_inf]
    h = data.input_data[h]
    t_deck = data.input_data[t_deck]
    t_range = [5,7,9,11,13,15,17,20]
    base_css = []

    for t_side in t_range:
        for t_bottom in t_range:
            base_cs = ics.create_initial_cs(b_sup, b_inf, h, t_side, t_deck, t_bottom)
            #perform proofs with different numbers and positins of stiffeners
            #assume all cs pass proofs without stiffeners s.t. the follwing statement holds
            st_prop = [] #or create the corresponding object which till now is useless
            base_css.append((base_cs, st_prop))

def step_2(base_css):
    #add_stiffener_set can bet put here... 
    pass

def step_3(preselect_css):
    #perform buckling proofs for defitive cs
    #what do we do with cs that do not pass anymore? -> maybe print
    pass
