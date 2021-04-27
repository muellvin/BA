from proofs import buckling_proof
import cs_collector
import data
from classes import proposed_stiffener
from classes import stiffeners_proposition
from classes import stiffener


#an optimizer that puts the stiffeners in place, such that the single plates inbetween each have the same total pressure
def opt_eqpressure(cs_fresh):
    t_values = [5, 10, 20]
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
            #the optimizer loop does not loop i_along, as this should be set optimally by the set functions
            while n_st_side <= n_st_side_max and stop_side == False:
                cs_temp = buckling_proof.buckling_proof(copy.deepcopy(cs))
                sigma_top_red = cs_temp.get_line(pl_position = 2).sigma_a_red
                sigma_bottom_red = cs_temp.get_line(pl_position = 2).sigma_b_red

                if tension_bottom == True:
                    cs = set_t_side(copy.deepcopy(cs_fresh), t_side)
                    cs = set_t_bottom(cs, t_bottom)
                    cs = set_stiffeners_side(cs, n_st_side, sigma_a_red, sigma_b_red)
                    #stresses at the top and bottom corner
                    sigma_top_red = get_sigma_top_red(cs)
                    sigma_bottom_red = get_sigma_bottom_red(cs)


                    if cs.utilisation_web <= 1:
                        cs_collector.into_collector(cs)
                        stop_side = True
                    elif cs.utilisation_web >1:
                        n_st_side += 1
                else:
                    n_st_bottom = 0
                    while n_st_bottom <= n_st_bottom_max and stop_bottom == False:
                        cs = set_t_side(copy.deepcopy(cs_fresh), t_side)
                        cs = set_t_bottom(cs, t_bottom)
                        cs = set_stiffeners_side(cs, n_st_side)
                        cs = set_stiffeners_bottom(cs, n_st_bottom)

                        if cs.utilisation_web <= 1 and cs.utilisation_flange_top <= 1 and cs.utilisation_flange_bottom <= 1:
                            cs_collector.into_collector(cs)
                            stop_bottom = True
                        else:
                            n_st_bottom += 1
                    n_st_side += 1

    return finished = True



def set_t_side(cs, t_side):
    for plate in cs.lines:
        if plate.code.pl_type == 0 and (plate.code.pl_position == 2 or plate.code.pl_position == 4):
            plate.t = t_side
    return cs


def set_t_bottom(cs, t_bottom):
    for plate in cs.lines:
        if plate.code.pl_type == 0 and plate.code.pl_position == 3:
            plate.t = t_side
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
            distance_i = 1/(2*m) * ( (-2)*sigma_before + math.sqrt((2*sigma_before)**2 - 4*m*(-2*F)))
            distances.append(distance_i)
            sigma_i_before = sigma_i_before + m*distance_i
            plate_i += 1

        locations = []
        """do the locations"""

        #create the proposed_stiffeners
        i_along_values = [3*10**7, 6*10**7, 9*10**7]
        st_number_side1_max = 0
        for plate in cs.plates:
            if plate.code.pl_position == 1 and plate.code.st_number > st_number_side1_max:
                st_number_side1_max = plate.code.st_number
        propositions = stiffeners_proposition.stiffeners_proposition()
        i = 1
        while i <= amount:
            proposition = proposed_stiffener.proposed_stiffener(2,st_number_side1_max + i, location[i-1], i_along_values[0], distances[i])
            proposition.b_sup_corr = True
            i += 1


        """do side 4 and the i_along loop"""


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
        i_along_values = [3*10**7, 6*10**7, 9*10**7]
        st_number_side2_max = 0
        for plate in cs.plates:
            if plate.code.pl_position == 2 and plate.code.st_number > st_number_side2_max:
                st_number_side2_max = plate.code.st_number

        propositions = stiffeners_proposition.stiffeners_proposition()
        st_number = st_number_side2_max + 1
        for location in locations:
            proposition = proposed_stiffener.proposed_stiffener(3,st_number, location, i_along_values[0], st_b_sup)
            proposition.b_sup_corr = True
            st_number += 1

        """correct the stiffener numbers for side 4"""


        #try all i_along give the smallest one that works or then the biggest one
        for i_along in i_along_values:
            for proposition in propositions:
                proposition.i_along = i_along

            cs = stiffener.merge(cs, propositions)
            cs = buckling_proof.buckling_proof(cs)
            if cs.utilisation_flange_bottom <= 1:
                return cs
        return cs


def get_sigma_top_red(cs):
    top_plate = cs.get_line(pl_position = 2 and pl_type = 0)
    for plate in cs.lines:
        if plate.code.tpl_number =< top_plate.code.tpl_number and plate.code.pl_type = 0:
            top_plate = plate
    return top_plate.sigma_a_red

def get_sigma_bottom_red(cs):
    bottom_plate = cs.get_line(pl_position = 2 and pl_type = 0)
    for plate in cs.lines:
        if plate.code.tpl_number >= top_plate.code.tpl_number and plate.code.pl_type = 0:
            bottom_plate = plate
    return top_plate.sigma_b_red
