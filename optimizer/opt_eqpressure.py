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
from output import printing

#an optimizer that puts the stiffeners in place, such that the single plates inbetween each have the same total pressure
def opt_eqpressure(cs_fresh, st_prop_deck):



    set_defaults_for_opt_eqpressure()

    t_values = [5]
    i_along_values = [10**7] # range(10**6, 10**8, 10*10**6)
    #i_along_values = [3*10**7, 6*10**7, 9*10**7]
    n_st_side_max = 1
    n_st_bottom_max = 4

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

            cs_temp = stiffener.add_stiffener_set(copy.deepcopy(empty_cs), st_prop_deck)
            cs_temp = buckling_proof.buckling_proof(copy.deepcopy(empty_cs))
            sigma_top_red = get_sigma_top_red(cs_temp)
            sigma_bottom_red = get_sigma_bottom_red(cs_temp)


            #the optimizer loop does not loop i_along, as this should be set optimally by the set functions
            n_st_side = 0
            while n_st_side <= n_st_side_max:
                print("\n888888888888888888888888888888888  ITERATION SIDE ", n_st_side, "888888888888888888888888888888888")
                for i_along_side in i_along_values:
                    print("\n&&&&&&&&&&&&&&&&&&&&&&&&& ITERATION I_ALONG_SIDE ", i_along_side, " &&&&&&&&&&&&&&&&&&&&&&&&&&&")

                    if tension_bottom == True:
                        #do it twice; the stresses now are the ones calculated for the same amount of stiffeners (but different place (could do more))
                        for times in range(2):
                            n_st_bottom = 0
                            st_prop_side = set_stiffeners_side(copy.deepcopy(empty_cs), n_st_side, n_st_bottom, sigma_top_red, sigma_bottom_red, i_along_side)
                            st_prop = stiffeners_proposition.stiffeners_proposition()
                            st_prop.stiffeners = copy.deepcopy(st_prop_deck.stiffeners) + copy.deepcopy(st_prop_side.stiffeners)
                            st_prop.stiffeners = sorted(st_prop.stiffeners, key = lambda st: st.st_number)
                            stiffened_cs = stiffener.add_stiffener_set(copy.deepcopy(empty_cs), st_prop)
                            stiffened_cs = buckling_proof.buckling_proof(copy.deepcopy(stiffened_cs))

                            #stresses at the top and bottom corner
                            sigma_top_red = get_sigma_top_red(stiffened_cs)
                            sigma_bottom_red = get_sigma_bottom_red(stiffened_cs)

                            #geometry_output.print_cs_red(stiffened_cs)

                        if stiffened_cs.eta_1 <= 1 and stiffened_cs.interaction_2 < 1 and stiffened_cs.interaction_3 < 1 and stiffened_cs.interaction_4 < 1:
                            print("\n\n GOT ONE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                            cs_collector.into_collector(stiffened_cs)

                    else:
                        n_st_bottom = 4
                        while n_st_bottom <= n_st_bottom_max:
                            print("\n888888888888888888888888888888888  ITERATION BOTTOM ", n_st_bottom, "888888888888888888888888888888888")
                            for i_along_bottom in i_along_values:
                                print("\n&&&&&&&&&&&&&&&&&&&&&&&&& ITERATION I_ALONG_SIDE ", i_along_bottom, " &&&&&&&&&&&&&&&&&&&&&&&&&&&")
                                #do it twice; the stresses now are the ones calculated for the same amount of stiffeners (but different place (could do more))
                                for times in range(2):
                                    st_prop_side = set_stiffeners_side(copy.deepcopy(empty_cs), n_st_side, n_st_bottom, sigma_top_red, sigma_bottom_red, i_along_side)
                                    st_prop_bottom = set_stiffeners_bottom(copy.deepcopy(empty_cs),n_st_side, n_st_bottom, sigma_bottom_red, i_along_bottom)
                                    st_prop = stiffeners_proposition.stiffeners_proposition()
                                    st_prop.stiffeners = copy.deepcopy(st_prop_deck.stiffeners) + copy.deepcopy(st_prop_side.stiffeners) + copy.deepcopy(st_prop_bottom.stiffeners)
                                    st_prop.stiffeners = sorted(st_prop.stiffeners, key = lambda st: st.st_number)

                                    stiffened_cs = stiffener.add_stiffener_set(copy.deepcopy(empty_cs), st_prop)
                                    #geometry_output.print_cs_red(stiffened_cs)
                                    stiffened_cs = buckling_proof.buckling_proof(copy.deepcopy(stiffened_cs))

                                    #stresses at the top and bottom corner
                                    sigma_top_red = get_sigma_top_red(stiffened_cs)
                                    sigma_bottom_red = get_sigma_bottom_red(stiffened_cs)

                                    #geometry_output.print_cs_red(stiffened_cs)
                                if stiffened_cs.eta_1 <= 1 and stiffened_cs.interaction_2 < 1 and stiffened_cs.interaction_3 < 1 and stiffened_cs.interaction_4 < 1:

                                    cs_collector.into_collector(stiffened_cs)


                                    #geometry_output.print_cs_red(stiffened_cs)
                            #terminate i_along_bottom
                            n_st_bottom += 1
                        #terminate n_st_bottom
                    #terminate else
                #terminate i_along _side
            #terminate n_st_side
                n_st_side += 1
        #terminate t bottom
    #terminate t_side
    printing.print_best()



def set_defaults_for_opt_eqpressure():
    defaults.b_inf_minimal = 10
    defaults.b_inf_step = 10
    defaults.b_inf_maximal = 500
    defaults.b_sup_minimal = 1
    defaults.b_sup_step = 50
    defaults.b_sup_maximal = 500
    defaults.b_sup_minimal = 50
    defaults.h_minimal = 50
    defaults.h_step = 10
    defaults.h_maximal = 300
    defaults.t_range = [5,7,9,11,13,15,17,20]
    defaults.max_angle = math.pi/12*5 #75 grad
    #check_geometry
    defaults.do_check_geometry = True
    defaults.do_check_stiffeners_in_corners_top = False
    defaults.do_check_stiffeners_in_corners_bottom = False
    defaults.do_height_only = True
    defaults.do_width_only = False

    defaults.do_shear_lag_plastically = False
    defaults.do_shear_lag = False
    defaults.do_global_plate_buckling = False
    defaults.do_column_plate_buckling = False

    defaults.do_print = True
    defaults.do_print_to_txt = False

    defaults.do_deck_as_prop = True

    defaults.optimize_for_cost_only = False
    defaults.optimize_for_spec_ei = False
    defaults.optimize_for_target_function = True



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


def set_stiffeners_side(cs, amount, n_st_bottom, sigma_top_red, sigma_bottom_red, i_along_side):
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
        F = (m*h_c**2/2 - m*h_min**2/2) / (2*amount + 1)

        #now to find the distances between the welding points
        distances = []
        i = 1
        sigma_i_before = sigma_min
        #distance is
        #from sigma_min to sigma_max find the distances using m and F
        while i <= 2*amount+1:
            #F = 1/2 * (sigma_before + sigma_before + m * distance_i) * distance_i
            #= = m*distance_i**2 + 2*sigma_before*distance_i -2*F
            distance_i = 1/(2*m) * ( (-2)*sigma_i_before + math.sqrt((2*sigma_i_before)**2 - 4*m*(-2*F)))
            #print("distance_i: "+str(distance_i))
            distances.append(distance_i)
            sigma_i_before = sigma_i_before + m*distance_i
            i += 1

        #sanity check
        #print("h_0", h_0)
        #print("+ sum(distances)", sum(distances))
        #print("= ", math.floor(h_0 + sum(distances)))
        #print("should be ", h)
        assert abs(h-(h_0 + sum(distances))) <= 5, "distances are wrong"

        #locations_abs are the centers between the welding points
        #the first is in distances[1]
        locations_abs = []
        b_sup_list = []
        i = 2
        locations_abs.append(h_0 + copy.deepcopy(distances[0]) + copy.deepcopy(distances[1])/2)
        b_sup_list.append(copy.deepcopy(distances[1]))
        locations_abs_last = copy.deepcopy(locations_abs[0])
        print("")
        print("widths_side: "+str(round(b_sup_list[0])))
        while i <= amount:
            locations_abs_i = locations_abs_last + distances[2*i-2]/2 + distances[2*i-2] + distances[2*i-1]/2
            locations_abs.append(locations_abs_i)
            locations_abs_last = copy.deepcopy(locations_abs_i)
            width_i = copy.deepcopy(distances[2*i-1])
            print("widths_side: "+str(round(width_i)))
            b_sup_list.append(width_i)
            i+=1

        print("")
        print("there are "+str(len(locations_abs))+" in locations_abs")

        #correct to relative height
        locations_side = []
        for locations_abs_i in locations_abs:
            locations_side.append(locations_abs_i / h)
            print("locations_side: "+str(locations_abs_i/h))

        i_alongs = [i_along_side]
        i = 2
        i_along_before = i_along_side
        #the i_alongs are scaled propotionally to the pressure gradient starting from i_along argument being the smallest
        while i <= amount:
            #2*i -1 is the width of the stiffener i
            i_along_next = i_along_before* (locations_abs[i-1] - h_0) / (locations_abs[i-2] - h_0)
            i_alongs.append(i_along_next)
            i_along_before = i_along_next
            i += 1


        #create the proposed_stiffeners
        #find the highest st number on the deck plate the bottom plate has no stiffener yet
        st_number_side1_max = 0
        for plate in cs.lines:
            if plate.code.pl_position == 1 and plate.code.st_number > st_number_side1_max:
                st_number_side1_max = plate.code.st_number


        propositions = stiffeners_proposition.stiffeners_proposition()


        if higher_top == True:

            #propositions are created from bottom to top
            for i in range(amount):
                proposition_right_i = proposed_stiffener.proposed_stiffener(2, st_number_side1_max + amount - i, locations_side[i], i_alongs[i], b_sup_list[i])
                proposition_right_i.b_sup_corr = True
                propositions.add(proposition_right_i)
                proposition_left_i = proposed_stiffener.proposed_stiffener(4, st_number_side1_max + n_st_bottom + amount + i +1, locations_side[i], i_alongs[i], b_sup_list[i])
                proposition_left_i.b_sup_corr = True
                propositions.add(proposition_left_i)
                i += 1
        else:
            for i in range(len(locations_side)):
                locations_side[i] = 1- locations_side[i]
            #propositions are created from top to bottom
            for i in range(amount):
                proposition_right_i = proposed_stiffener.proposed_stiffener(2, st_number_side1_max + 1 + i, locations_side[i], i_alongs[i], b_sup_list[i])
                proposition_right_i.b_sup_corr = True
                propositions.add(proposition_right_i)
                proposition_left_i = proposed_stiffener.proposed_stiffener(4, st_number_side1_max + n_st_bottom + 2*amount - i, locations_side[i], i_alongs[i], b_sup_list[i])
                proposition_left_i.b_sup_corr = True
                propositions.add(proposition_left_i)
                i += 1


        propositions.stiffeners = sorted(propositions.stiffeners, key = lambda st: st.st_number)

        return propositions



def set_stiffeners_bottom(cs, n_st_side, amount, sigma_bottom_red, i_along_bottom):
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
            print("locations bottom: ", locations[l])
        #print("sum of widths", amount*st_b_sup)



        #create the proposed_stiffeners
        if st_b_sup < 100:
            i_along = 10**5
        elif st_b_sup < 300:
            i_along = 10**6
        elif st_b_sup < 500:
            i_along = 10**7
        else:
            i_along = 5*10**7
        st_number_side1_max = 0
        for plate in cs.lines:
            if plate.code.pl_position == 1 and plate.code.st_number > st_number_side1_max:
                st_number_side1_max = plate.code.st_number

        propositions = stiffeners_proposition.stiffeners_proposition()
        st_number = st_number_side1_max + n_st_side + 1
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
