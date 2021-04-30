from proofs import buckling_proof
from proofs import local_buckling
import cs_collector
import data
from classes import proposed_stiffener
from classes import stiffeners_proposition
from classes import stiffener
from classes import merge
from classes import substantiate
import copy
import math
from output import geometry_output
import defaults

#an optimizer that puts the stiffeners in place, such that the single plates inbetween each have the same total pressure
def opt_eqpressure(cs_fresh, st_list_deck):
    defaults.do_height_only = True

    t_values = [5]
    #i_along_values = [3*10**7, 6*10**7, 9*10**7]
    n_st_side_max = 2
    n_st_bottom_max = 5

    """TILL NOW: ONLY ONE I_ALONG FOR ALL"""

    if data.input_data.get("M_Ed") > 1:
        tension_bottom = True
    else:
        tension_bottom = False

    for t_side in t_values:
        print("888888888888888888888888888888888  SIDE T = ", t_side, "888888888888888888888888888888888")
        for t_bottom in t_values:
            print("888888888888888888888888888888888  BOTTOM T = ", t_bottom, "888888888888888888888888888888888")

            empty_cs = set_t_side(copy.deepcopy(cs_fresh), t_side)
            empty_cs = set_t_bottom(empty_cs, t_bottom)

            cs_temp = merge.merge(copy.deepcopy(empty_cs), st_list_deck)
            cs_temp = buckling_proof.buckling_proof(copy.deepcopy(empty_cs))
            sigma_top_red = get_sigma_top_red(cs_temp)
            sigma_bottom_red = get_sigma_bottom_red(cs_temp)


            #the optimizer loop does not loop i_along, as this should be set optimally by the set functions
            n_st_side = 0
            while n_st_side <= n_st_side_max:
                print("888888888888888888888888888888888  ITERATION SIDE ", n_st_side, "888888888888888888888888888888888")

                if tension_bottom == True:
                    #do it twice; the stresses now are the ones calculated for the same amount of stiffeners (but different place (could do more))
                    for twice in range(2):
                        st_prop_side = set_stiffeners_side(copy.deepcopy(empty_cs), n_st_side, sigma_top_red, sigma_bottom_red)
                        st_list_side = substantiate.substantiate(copy.deepcopy(empty_cs), st_prop_side)
                        st_list = st_list_deck + st_list_side
                        st_list = sorted(st_list, key = lambda st: st.lines[0].code.st_number)

                        stiffened_cs = merge.merge(copy.deepcopy(empty_cs), st_list)
                        stiffened_cs = buckling_proof.buckling_proof(copy.deepcopy(stiffened_cs))

                        #stresses at the top and bottom corner
                        sigma_top_red = get_sigma_top_red(stiffened_cs)
                        sigma_bottom_red = get_sigma_bottom_red(stiffened_cs)

                    if stiffened_cs.eta_1 <= 1 and stiffened_cs.interaction_2 < 1 and stiffened_cs.interaction_3 < 1 and stiffened_cs.interaction_4 < 1:
                        #cs_collector.into_collector(stiffened_cs)
                        pass

                    geometry_output.print_cs_red(stiffened_cs)


                else:
                    n_st_bottom = 4
                    while n_st_bottom <= n_st_bottom_max:
                        print("888888888888888888888888888888888  ITERATION BOTTOM ", n_st_bottom, "888888888888888888888888888888888")
                        #do it twice; the stresses now are the ones calculated for the same amount of stiffeners (but different place (could do more))
                        for twice in range(2):
                            print("~~~~~~~~~~~~~ find stiffeners side")
                            st_prop_side = set_stiffeners_side(copy.deepcopy(empty_cs), n_st_side, sigma_top_red, sigma_bottom_red)
                            print("~~~~~~~~~~~~~ find stiffeners bottom")
                            st_prop_bottom = set_stiffeners_bottom(copy.deepcopy(empty_cs), n_st_bottom, sigma_bottom_red)
                            st_list_side = substantiate.substantiate(copy.deepcopy(empty_cs), st_prop_side)
                            st_list_bottom = substantiate.substantiate(copy.deepcopy(empty_cs), st_prop_bottom)
                            st_list = st_list_deck + st_list_side + st_list_bottom
                            st_list = sorted(st_list, key = lambda st: st.lines[0].code.st_number)

                            stiffened_cs = merge.merge(copy.deepcopy(empty_cs), st_list)
                            stiffened_cs = buckling_proof.buckling_proof(copy.deepcopy(stiffened_cs))

                            #stresses at the top and bottom corner
                            sigma_top_red = get_sigma_top_red(stiffened_cs)
                            sigma_bottom_red = get_sigma_bottom_red(stiffened_cs)


                        if stiffened_cs.eta_1 <= 1 and stiffened_cs.interaction_2 < 1 and stiffened_cs.interaction_3 < 1 and stiffened_cs.interaction_4 < 1:
                            cs_collector.into_collector(stiffened_cs)
                        n_st_bottom += 1

                        geometry_output.print_cs_red(stiffened_cs)

                n_st_side += 1




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
        propositions = stiffeners_proposition.stiffeners_proposition()
        return propositions
    else:
        #all tension?
        if sigma_top_red < 0 and sigma_bottom_red < 0:
            propositions = stiffeners_proposition.stiffeners_proposition()
            return propositions

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

        #h_c height that is under pressure length of whole triangle
        h_c = h / (1-psi)

        #h_min is the height under pressure that exceeds h
        #h_0 is the height under tension of h
        if h_c < h:
            h_min = 0
            h_0 = h - h_c
        else:
            h_min = h_c - h
            h_0 = 0

        #pressure gradient m
        m = sigma_max / h_c
        #eqpressure means all single plates get the same total force F
        F = (h_c**2/2 - h_min**2/2)*m / (2*amount + 1)

        #now to find the distances between the welding points
        distances = []
        i = 1
        sigma_i_before = sigma_min
        #distance is
        #from sigma_min to sigma_max find the distances using m and F
        while i <= 2*amount+1:
            #F = 1/2 * (2*sigma_before + m * distance_i) * distance_i
            #= = m*distance_i**2 + 2*sigma_before*distance_i -2*F
            distance_i = 1/(2*m) * ( (-2)*sigma_i_before + math.sqrt((2*sigma_i_before)**2 - 4*m*(-2*F)))
            distances.append(distance_i)
            sigma_i_before = sigma_i_before + m*distance_i
            i += 1

        #sanity check
        #print("h_0", h_0)
        #print("+ sum(distances)", sum(distances))
        #print("= ", math.floor(h_0 + sum(distances)))
        #print("should be ", h)
        assert abs(h-(h_0 + sum(distances))) <= 5, "distances are wrong"

        locations_abs = []
        b_sup_list = []
        i = 1
        location_abs_last = distances[0]/2
        while i <= amount:
            location_abs_i = h_0 + location_abs_last + distances[i-1]/2 + distances[i]/2
            locations_abs.append(location_abs_i)
            location_abs_last = location_abs_i
            width_i = distances[i]
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


        if higher_top == True:
            #propositions are created from bottom to top
            i = 1
            while i <= amount:
                if distances[i] < 100:
                    i_along = 10**5
                elif distances[i] < 300:
                    i_along = 10**6
                elif distances[i] < 500:
                    i_along = 10**7
                else:
                    i_along = 5*10**7
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
            while i <= amount:
                if distances[i] < 100:
                    i_along = 10**5
                elif distances[i] < 300:
                    i_along = 10**6
                elif distances[i] < 500:
                    i_along = 10**7
                else:
                    i_along = 5*10**7
                proposition_right_i = proposed_stiffener.proposed_stiffener(2, st_number_side1_max + i, (1-locations[i-1]), i_along, distances[i])
                proposition_right_i.b_sup_corr = True
                propositions.add(proposition_right_i)
                proposition_left_i = proposed_stiffener.proposed_stiffener(4, st_number_side1_max + 2*amount - i + 1, (1-locations[i-1]), i_along, distances[i])
                proposition_left_i.b_sup_corr = True
                propositions.add(proposition_left_i)
                i += 1


        propositions.stiffeners = sorted(propositions.stiffeners, key = lambda st: st.st_number)

        return propositions



def set_stiffeners_bottom(cs, amount, sigma_bottom_red):
    if amount == 0:
        propositions = stiffeners_proposition.stiffeners_proposition()
        return propositions
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
        for l in range(amount):
            locations[l] = locations[l] * st_b_sup /cs_b_inf*2
            print("location: ", locations[l])
        print("sum of widths", amount*st_b_sup)



        #create the proposed_stiffeners
        if st_b_sup < 100:
            i_along = 10**5
        elif st_b_sup < 300:
            i_along = 10**6
        elif st_b_sup < 500:
            i_along = 10**7
        else:
            i_along = 5*10**7
        st_number_side2_max = 0
        for plate in cs.lines:
            if plate.code.pl_position == 2 and plate.code.st_number > st_number_side2_max:
                st_number_side2_max = plate.code.st_number

        propositions = stiffeners_proposition.stiffeners_proposition()
        st_number = st_number_side2_max + 1
        for location in locations:
            proposition = proposed_stiffener.proposed_stiffener(3,st_number, location, i_along, st_b_sup)
            proposition.b_sup_corr = True
            propositions.add(proposition)
            st_number += 1
        #correct the st_numbers of side 4
        for plate in cs.lines:
            if plate.code.pl_type == 1 and plate.code.pl_position == 4:
                plate.code.st_number += amount

        propositions.stiffeners = sorted(propositions.stiffeners, key = lambda st: st.st_number)
        return propositions


def get_sigma_top_red(cs):
    top_plate = cs.get_line(pl_position = 2, pl_type = 0)
    for plate in cs.lines:
        if plate.code.tpl_number <= top_plate.code.tpl_number and plate.code.pl_position == 2 and plate.code.pl_type == 0:
            top_plate = plate
    return top_plate.sigma_a_red

def get_sigma_bottom_red(cs):
    bottom_plate = copy.deepcopy(cs.get_line(pl_position = 2, pl_type = 0))
    for plate in cs.lines:
        if plate.code.tpl_number >= bottom_plate.code.tpl_number and plate.code.pl_position == 2 and plate.code.pl_type == 0:
            bottom_plate = copy.deepcopy(plate)
    return bottom_plate.sigma_b_red
