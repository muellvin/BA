from proofs import buckling_proof
from proofs import local_buckling
import cs_collector
import data
from classes import proposed_stiffener
from classes import stiffeners_proposition
from classes import stiffener
from classes import substantiate
import copy
import math


#an optimizer that puts the stiffeners in place, such that the single plates inbetween each have the same total pressure
def opt_eqpressure(cs_fresh):
    t_values = [5, 10, 20]
    i_along_values = [3*10**7, 6*10**7, 9*10**7]
    n_st_side_max = 8
    n_st_bottom_max = 10

    if data.input_data.get("M_Ed") > 1:
        tension_bottom = True
    else:
        tension_bottom = False

    for t_side in t_values:
        for t_bottom in t_values:

            stop_side = False
            stop_bottom = False

            n_st_side = 0
            sigma_top_red = 0
            sigma_bottom_red = 0
            first_iteration_side = True
            iteration_i = 0
            #the optimizer loop does not loop i_along, as this should be set optimally by the set functions
            while n_st_side <= n_st_side_max and stop_side == False:
                print("888888888888888888888888888888888  ITERATION ", iteration_i, "88888888888888888888888888888888")
                if first_iteration_side == True:
                    cs_temp = local_buckling.local_buckling(copy.deepcopy(cs_fresh))
                    print(" I WAS HERE I WAS HERE I WAS HERE I AWS HERE")
                    sigma_top_red = cs_temp.get_line(pl_position = 2).sigma_a_red
                    sigma_bottom_red = cs_temp.get_line(pl_position = 2).sigma_b_red

                else:
                    print(" I WAS HERE TOOOOOOOOOOOOOOOO I WAS HERE I WAS HERE I AWS HERE")
                    sigma_top_red = cs.get_line(pl_position = 2).sigma_a_red
                    sigma_bottom_red = cs.get_line(pl_position = 2).sigma_b_red


                if tension_bottom == True:
                    print("TENSION BOTTOM TRUEEEEEEEEEEEEEEEEEEEEEE")
                    cs = set_t_side(copy.deepcopy(cs_fresh), t_side)

                    cs = set_t_bottom(cs, t_bottom)
                    print("im stuck heereee")
                    cs = set_stiffeners_side(cs, n_st_side, sigma_top_red, sigma_bottom_red)
                    print("im stuck heereee")

                    cs = buckling_proof.buckling_proof(copy.deepcopy(cs))
                    #stresses at the top and bottom corner
                    sigma_top_red = get_sigma_top_red(cs)
                    sigma_bottom_red = get_sigma_bottom_red(cs)

                    if cs.interaction_2 <= 1:
                        return cs
                        cs_collector.into_collector(cs)
                        stop_side = True
                    elif cs.interaction_2 >1:
                        n_st_side += 1
                    first_iteration_side = False
                    iteration_i += 1
                else:
                    print("TENSION BOTTOM FAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALSE")
                    n_st_bottom = 0
                    while n_st_bottom <= n_st_bottom_max and stop_bottom == False:
                        cs = set_t_side(copy.deepcopy(cs_fresh), t_side)
                        cs = set_t_bottom(cs, t_bottom)
                        cs = set_stiffeners_side(cs, n_st_side)
                        cs = set_stiffeners_bottom(cs, n_st_bottom)

                        if cs.interaction_2 <= 1 and cs.interaction_2 <= 1 and cs.utilisation_flange_bottom <= 1:
                            return cs
                            cs_collector.into_collector(cs)
                            stop_bottom = True
                        else:
                            n_st_bottom += 1
                    first_iteration_side = False
                    iteration_i += 1
                    n_st_side += 1

    return cs



def set_t_side(cs, t_side):
    for plate in cs.lines:
        if plate.code.pl_type == 0 and (plate.code.pl_position == 2 or plate.code.pl_position == 4):
            plate.t = t_side
    return cs


def set_t_bottom(cs, t_bottom):
    for plate in cs.lines:
        if plate.code.pl_type == 0 and plate.code.pl_position == 3:
            plate.t = t_bottom
    return cs


def set_stiffeners_side(cs, amount, sigma_top_red, sigma_bottom_red):
    if amount == 0:
        cs = buckling_proof.buckling_proof(cs)
        return cs
    else:
        #all tension?
        if sigma_top_red < 0 and sigma_bottom_red < 0:
            return cs
        #where is the higher pressure
        if sigma_top_red > sigma_bottom_red:
            higher_top = True
            sigma_max = sigma_top_red
        else:
            higher_top = False
            sigma_max = sigma_bottom_red
        #the max stress and if all pressure than also the small one
        if sigma_top_red > 0 and sigma_bottom_red > 0:
            if higher_top == True:
                sigma_min = sigma_bottom_red
            else:
                sigma_min = sigma_top_red
        else:
            sigma_min = 0

        psi = min(sigma_top_red, sigma_bottom_red)/max(sigma_top_red, sigma_bottom_red)
        h = data.input_data.get("h")
        h_c = h / (1-psi)
        if h_c < h:
            h_min = 0
            h_0 = h - h_c
        else:
            h_min = h_c - h
            h_0 = 0
        #pressure gradient m
        m = (sigma_max - sigma_min) / (h_c - h_min)
        #eqpressure means all single plates get the same total force F
        F = (h_c**2/2 - h_min**2/2)*m / (amount + 1)

        #now to find the distances between the welding points
        distances = []
        plate_i = 1
        sigma_i_before = sigma_min
        #from sigma_min to sigma_max find the distances using m and F
        while plate_i <= amount:
            #F = 1/2 * (2*sigma_before + m * distance_i) * distance_i
            #= = m*distance_i**2 + 2*sigma_before*distance_i -2*F
            distance_i = 1/(2*m) * ( (-2)*sigma_i_before + math.sqrt((2*sigma_i_before)**2 - 4*m*(-2*F)))
            distances.append(distance_i)
            sigma_i_before = sigma_i_before + m*distance_i
            plate_i += 1

        locations_abs = []
        b_sup_list = []
        i = 1
        location_abs_last = distances[0]/2
        while i <= amount:
            location_abs_i = location_abs_last + distances[i-2]/2 + distances[i-1]/2
            locations_abs.append(location_abs_i)
            location_abs_last = location_abs_i
            width_i = distances[i-1]
            b_sup_list.append(width_i)
            i+=1

        #correct to relative height
        locations = []
        for location_abs_i in locations_abs:
            locations.append(location_abs_i / h)


        #create the proposed_stiffeners
        #find the highest st number on the deck plate the bottom plate has no stiffener yet
        st_number_side1_max = 0
        for plate in cs.lines:
            if plate.code.pl_position == 1 and plate.code.st_number > st_number_side1_max:
                st_number_side1_max = plate.code.st_number


        propositions = stiffeners_proposition.stiffeners_proposition()
        i_along = 3*10**7

        if higher_top == True:
            #propositions are created from bottom to top
            i = 1
            while i < amount:
                proposition_right_i = proposed_stiffener.proposed_stiffener(2, st_number_side1_max + amount + 1 - i, locations[i-1], i_along, distances[i])
                proposition_right_i.b_sup_corr = True
                propositions.add(proposition_right_i)
                proposition_left_i = proposed_stiffener.proposed_stiffener(4, st_number_side1_max + amount + i - 1, locations[i-1], i_along, distances[i])
                proposition_left_i.b_sup_corr = True
                propositions.add(proposition_left_i)
                i += 1
        else:
            #propositions are created from top to bottom
            i = 1
            while i < amount:
                proposition_right_i = proposed_stiffener.proposed_stiffener(2, st_number_side1_max + i, locations[i-1], i_along, distances[i])
                proposition_right_i.b_sup_corr = True
                propositions.add(proposition_right_i)
                proposition_left_i = proposed_stiffener.proposed_stiffener(4, st_number_side1_max + 2*amount - i + 1, locations[i-1], i_along, distances[i])
                proposition_left_i.b_sup_corr = True
                propositions.add(proposition_left_i)


        propositions.stiffeners = sorted(propositions.stiffeners, key = lambda st: st.st_number)
        stiffener_list = substantiate.substantiate(copy.deepcopy(cs),propositions)
        cs = stiffener.merge(cs, stiffener_list)
        return cs



def set_stiffeners_bottom(cs, amount):
    if amount == 0:
        cs = buckling_proof.buckling_proof(cs)
        return cs
    else:
        cs_b_inf = data.input_data.get("b_inf")
        st_b_sup = data.input_data.get("b_inf")/(2*amount + 1)

        locations = []
        #where are the centers of the stiffeners
        #the location is the number of st_b_sup away from y = 0
        #1 st gives 0
        #2 st give -1, 1
        #3 st give -2, 0, 2 ...
        i = -amount + 1
        while i <= amount:
            locations.append(i)
            i += 2
        #change it to the convention of create_stiffener_global
        for location in locations:
            location = location * b_st_sup / cs_b_inf


        #create the proposed_stiffeners
        i_along = 3*10**7
        st_number_side2_max = 0
        for plate in cs.plates:
            if plate.code.pl_position == 2 and plate.code.st_number > st_number_side2_max:
                st_number_side2_max = plate.code.st_number

        propositions = stiffeners_proposition.stiffeners_proposition()
        st_number = st_number_side2_max + 1
        for location in locations:
            proposition = proposed_stiffener.proposed_stiffener(3,st_number, location, i_along, st_b_sup)
            proposition.b_sup_corr = True
            st_number += 1

        #correct the st_numbers of side 4
        for plate in cs.lines:
            if plate.code.pl_type == 1 and plate.code.pl_position == 4:
                plate.code.st_number += amount

        propositions.stiffeners = sorted(propositions.stiffeners, key = lambda st: st.st_number)
        stiffeners_list = substantiate.substantiate(copy.deepcopy(cs), propositions)
        cs = stiffener.merge(cs, stiffeners_list)
        return cs


def get_sigma_top_red(cs):
    top_plate = cs.get_line(pl_position = 2, pl_type = 0)
    for plate in cs.lines:
        if plate.code.tpl_number <= top_plate.code.tpl_number and plate.code.pl_type == 0:
            top_plate = plate
    return top_plate.sigma_a_red

def get_sigma_bottom_red(cs):
    bottom_plate = cs.get_line(pl_position = 2, pl_type = 0)
    for plate in cs.lines:
        if plate.code.tpl_number <= bottom_plate.code.tpl_number and plate.code.pl_type == 0:
            bottom_plate = plate
    return bottom_plate.sigma_b_red
