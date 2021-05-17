import math
from classes import crosssection
import initial_cs as ics
import deck
import copy
from classes import stiffener
from classes import proposed_stiffener
from classes import stiffeners_proposition
from classes import substantiate
from classes import merge
from output import geometry_output as go
from proofs import buckling_proof
import defaults
import data
from proofs import stress_cal
from optimizer import optimization_value


def optimize():
    b_sup = data.input_data["b_sup"]
    b_inf = data.input_data["b_inf"]
    h = data.input_data["h"]
    t_deck = data.input_data["t_deck"]
    t_range = [10, 20]
    t_max_min = 20
    I_range = [3*10**7, 7*10**7]
    counter = 1
    st_list_deck = deck.deck(b_sup)
    cs_collection = set()
    num_top_stiffeners = len(st_list_deck)
    m_ed = data.input_data.get("M_Ed")
    sign = math.copysign(1, m_ed)

    #no side stiffener block
    num_side_stiffeners = 0
    for t_side in t_range:
        for t_bottom in t_range:
            base_cs = ics.create_initial_cs(b_sup, b_inf, h, t_side, t_deck, t_bottom)
            for num_btm_stiffeners in range(4):
                strong_enough = False
                #no side stiffeners cs
                if num_side_stiffeners == 0:
                    #without bottom stiffeners
                    if num_btm_stiffeners == 0:
                        print("\n-------------------------------------------------------------------------------------------------------")
                        print("------------------------------------ CS" +str(counter) + "---------------------------------------------------------------")
                        counter += 1
                        print("#Side Stiffeners " + str(num_side_stiffeners))
                        print("#Btm Stiffeners " + str(num_btm_stiffeners))
                        test_cs = copy.deepcopy(base_cs)
                        end_cs = buckling_proof.buckling_proof(test_cs)
                        print(end_cs)
                        #go.print_cs_red(end_cs)
                        prop = stiffeners_proposition.stiffeners_proposition()
                        proven = end_cs.eta_1 < 1 and end_cs.interaction_2 < 1 and end_cs.interaction_3 < 1 and end_cs.interaction_4 < 1
                        if proven:
                            if max(t_side, t_bottom) < t_max_min:
                                t_max_min = max(t_side, t_bottom)
                            print(str(optimization_value.cost(end_cs)) + " CHF")
                            print("PASS!")
                            cs_collection.add(end_cs)
                        else:
                            print("FAIL!")
                    #with bottom stiffeners
                    else:
                        for I_btm in I_range:
                            if strong_enough == False:
                                print("\n-------------------------------------------------------------------------------------------------------")
                                print("------------------------------------ CS" +str(counter) + "---------------------------------------------------------------")
                                counter += 1
                                print("#Side Stiffeners " + str(num_side_stiffeners))
                                print("#Btm Stiffeners " + str(num_btm_stiffeners))
                                print("I_Bottom " + str(I_btm))
                                prop = stiffeners_proposition.stiffeners_proposition()
                                for num in range(num_btm_stiffeners):
                                    loc_btm = 1 - 2/(num_btm_stiffeners+1)*(num+1)
                                    st_number = num_top_stiffeners + num_side_stiffeners + num + 1
                                    st = proposed_stiffener.proposed_stiffener(pl_position = 3, st_number = st_number, location = loc_btm, i_along = I_btm)
                                    prop.stiffeners.append(st)
                                base_cs_copy = copy.deepcopy(base_cs)
                                st_list_rest = substantiate.substantiate(base_cs_copy, prop)
                                st_list = st_list_deck + st_list_rest
                                test_cs = merge.merge(base_cs_copy, st_list)
                                end_cs = buckling_proof.buckling_proof(test_cs)
                                print(end_cs)
                                #go.print_cs_red(end_cs)
                                prop = stiffeners_proposition.stiffeners_proposition()
                                proven = end_cs.eta_1 < 1 and end_cs.interaction_2 < 1 and end_cs.interaction_3 < 1 and end_cs.interaction_4 < 1
                                if proven:
                                    if max(t_side, t_bottom) < t_max_min:
                                        t_max_min = max(t_side, t_bottom)
                                    strong_enough = True
                                    cs_collection.add(end_cs)
                                    print(str(optimization_value.cost(end_cs)) + " CHF")
                                    print("PASS!")
                                else:
                                    print("FAIl!")
    t_collection = []
    for t in t_range:
        if t <= t_max_min:
            t_collection.append(t)
    t_range = t_collection

    #one side stiffener block
    num_side_stiffeners = 1
    for t_side in t_range:
        for t_bottom in t_range:
            base_cs = ics.create_initial_cs(b_sup, b_inf, h, t_side, t_deck, t_bottom)
            for num_btm_stiffeners in range(4):
                if num_side_stiffeners == 1:
                    #without bottom stiffeners
                    if num_btm_stiffeners == 0:
                        locations_side = get_locations_side(num_side_stiffeners, sign)
                        for loc_side in range(len(locations_side)):
                            strong_enough = False
                            for I_side in I_range:
                                if strong_enough == False:
                                    print("\n-------------------------------------------------------------------------------------------------------")
                                    print("------------------------------------ CS" +str(counter) + "---------------------------------------------------------------")
                                    counter += 1
                                    print("#Side Stiffeners " + str(num_side_stiffeners))
                                    print("#Btm Stiffeners " + str(num_btm_stiffeners))
                                    print("I_Side " + str(I_side))
                                    prop = stiffeners_proposition.stiffeners_proposition()
                                    for num in range(num_side_stiffeners):
                                        #create side stiffeners
                                        loc = locations_side[loc_side][num]
                                        print("Location Side" + str(loc))
                                        assert loc != -1, "Error!"
                                        st_number_right = num_top_stiffeners + num + 1
                                        st_number_left = num_top_stiffeners + num_btm_stiffeners + 2*num_side_stiffeners - num
                                        st_right = proposed_stiffener.proposed_stiffener(pl_position = 2, st_number = st_number_right, location = loc, i_along = I_side)
                                        st_left = proposed_stiffener.proposed_stiffener(pl_position = 4, st_number = st_number_left, location = loc, i_along = I_side)
                                        prop.stiffeners.append(st_right)
                                        prop.stiffeners.append(st_left)
                                    base_cs_copy = copy.deepcopy(base_cs)
                                    st_list_rest = substantiate.substantiate(base_cs_copy, prop)
                                    st_list = st_list_deck + st_list_rest
                                    test_cs = merge.merge(base_cs_copy, st_list)
                                    end_cs = buckling_proof.buckling_proof(test_cs)
                                    prop = stiffeners_proposition.stiffeners_proposition()
                                    proven = end_cs.eta_1 < 1 and end_cs.interaction_2 < 1 and end_cs.interaction_3 < 1 and end_cs.interaction_4 < 1
                                    if proven:
                                        if max(t_side, t_bottom) < t_max_min:
                                            t_max_min = max(t_side, t_bottom)
                                        strong_enough = True
                                        cs_collection.add(end_cs)
                                        print(str(optimization_value.cost(end_cs)) + " CHF")
                                        print("PASS!")
                                    else:
                                        print("FAIL!")
                    #with bottom stiffeners
                    else:
                        for I_side in I_range:
                            locations_side = get_locations_side(num_side_stiffeners, sign)
                            for loc_side in range(len(locations_side)):
                                strong_enough = False
                                for I_btm in I_range:
                                    if strong_enough == False:
                                        print("\n-------------------------------------------------------------------------------------------------------")
                                        print("------------------------------------ CS" +str(counter) + "---------------------------------------------------------------")
                                        counter += 1
                                        print("#Side Stiffeners " + str(num_side_stiffeners))
                                        print("#Btm Stiffeners " + str(num_btm_stiffeners))
                                        print("I_Side " + str(I_side))
                                        print("I_Btm " + str(I_btm))
                                        prop = stiffeners_proposition.stiffeners_proposition()
                                        for num in range(num_side_stiffeners):
                                            #create side stiffeners
                                            loc = locations_side[loc_side][num]
                                            print("Location Side" + str(loc))
                                            assert loc != -1, "Error!"
                                            st_number_right = num_top_stiffeners + num + 1
                                            st_number_left = num_top_stiffeners + num_btm_stiffeners + 2*num_side_stiffeners - num
                                            st_right = proposed_stiffener.proposed_stiffener(pl_position = 2, st_number = st_number_right, location = loc, i_along = I_side)
                                            st_left = proposed_stiffener.proposed_stiffener(pl_position = 4, st_number = st_number_left, location = loc, i_along = I_side)
                                            prop.stiffeners.append(st_right)
                                            prop.stiffeners.append(st_left)
                                            #create bottom siffeners
                                        for num in range(num_btm_stiffeners):
                                            loc_btm = 1 - 2/(num_btm_stiffeners+1)*(num+1)
                                            st_number = num_top_stiffeners + num_side_stiffeners + num + 1
                                            st = proposed_stiffener.proposed_stiffener(pl_position = 3, st_number = st_number, location = loc_btm, i_along = I_btm)
                                            prop.stiffeners.append(st)
                                        base_cs_copy = copy.deepcopy(base_cs)
                                        st_list_rest = substantiate.substantiate(base_cs_copy, prop)
                                        st_list = st_list_deck + st_list_rest
                                        test_cs = merge.merge(base_cs_copy, st_list)
                                        end_cs = buckling_proof.buckling_proof(test_cs)
                                        prop = stiffeners_proposition.stiffeners_proposition()
                                        proven = end_cs.eta_1 < 1 and end_cs.interaction_2 < 1 and end_cs.interaction_3 < 1 and end_cs.interaction_4 < 1
                                        if proven:
                                            if max(t_side, t_bottom) < t_max_min:
                                                t_max_min = max(t_side, t_bottom)
                                            strong_enough = True
                                            cs_collection.add(end_cs)
                                            print(str(optimization_value.cost(end_cs)) + " CHF")
                                            print("PASS!")
                                        else:
                                            print("FAIL!")
    t_collection = []
    for t in t_range:
        if t <= t_max_min:
            t_collection.append(t)
    t_range = t_collection

    #two side stiffeners block
    num_side_stiffeners = 2
    for t_side in t_range:
        for t_bottom in t_range:
            base_cs = ics.create_initial_cs(b_sup, b_inf, h, t_side, t_deck, t_bottom)
            for num_btm_stiffeners in range(4):
                if num_side_stiffeners == 2:
                    #without bottom stiffeners
                    if num_btm_stiffeners == 0:
                        for I_side_btm in I_range:
                            for I_side_top in I_range:
                                I_collection = [I_side_top, I_side_btm]
                                locations_side = get_locations_side(num_side_stiffeners, sign)
                                for loc_side in range(len(locations_side)):
                                    print("\n-------------------------------------------------------------------------------------------------------")
                                    print("------------------------------------ CS" +str(counter) + "---------------------------------------------------------------")
                                    counter += 1
                                    print("#Side Stiffeners " + str(num_side_stiffeners))
                                    print("#Btm Stiffeners " + str(num_btm_stiffeners))
                                    print("I_Side_Top " + str(I_side_top))
                                    print("I_Side_Bottom " + str(I_side_btm))
                                    prop = stiffeners_proposition.stiffeners_proposition()
                                    for num in range(num_side_stiffeners):
                                        #create side stiffeners
                                        loc = locations_side[loc_side][num]
                                        print("Location Side" + str(loc))
                                        assert loc != -1, "Error!"
                                        st_number_right = num_top_stiffeners + num + 1
                                        st_number_left = num_top_stiffeners + num_btm_stiffeners + 2*num_side_stiffeners - num
                                        st_right = proposed_stiffener.proposed_stiffener(pl_position = 2, st_number = st_number_right, location = loc, i_along = I_collection[num])
                                        st_left = proposed_stiffener.proposed_stiffener(pl_position = 4, st_number = st_number_left, location = loc, i_along = I_collection[num])
                                        prop.stiffeners.append(st_right)
                                        prop.stiffeners.append(st_left)
                                    base_cs_copy = copy.deepcopy(base_cs)
                                    st_list_rest = substantiate.substantiate(base_cs_copy, prop)
                                    st_list = st_list_deck + st_list_rest
                                    test_cs = merge.merge(base_cs_copy, st_list)
                                    end_cs = buckling_proof.buckling_proof(test_cs)
                                    prop = stiffeners_proposition.stiffeners_proposition()
                                    proven = end_cs.eta_1 < 1 and end_cs.interaction_2 < 1 and end_cs.interaction_3 < 1 and end_cs.interaction_4 < 1
                                    if proven:
                                        if max(t_side, t_bottom) < t_max_min:
                                            t_max_min = max(t_side, t_bottom)
                                        cs_collection.add(end_cs)
                                        print(str(optimization_value.cost(end_cs)) + " CHF")
                                        print("PASS!")
                                    else:
                                        print("FAIL!")
                    #with bottom stiffeners
                    else:
                        for I_side_btm in I_range:
                            for I_side_top in I_range:
                                I_collection = [I_side_top, I_side_btm]
                                locations_side = get_locations_side(num_side_stiffeners, sign)
                                for loc_side in range(len(locations_side)):
                                    strong_enough = False
                                    for I_btm in I_range:
                                        if strong_enough == False:
                                            print("\n-------------------------------------------------------------------------------------------------------")
                                            print("------------------------------------ CS" +str(counter) + "---------------------------------------------------------------")
                                            counter += 1
                                            print("#Side Stiffeners " + str(num_side_stiffeners))
                                            print("#Btm Stiffeners " + str(num_btm_stiffeners))
                                            print("I_Side_Top " + str(I_side_top))
                                            print("I_Side_Bottom " + str(I_side_btm))
                                            print("I_Btm " + str(I_btm))
                                            prop = stiffeners_proposition.stiffeners_proposition()
                                            for num in range(num_side_stiffeners):
                                                #create side stiffeners
                                                loc = locations_side[loc_side][num]
                                                print("Location Side" + str(loc))
                                                assert loc != -1, "Error!"
                                                st_number_right = num_top_stiffeners + num + 1
                                                st_number_left = num_top_stiffeners + num_btm_stiffeners + 2*num_side_stiffeners - num
                                                st_right = proposed_stiffener.proposed_stiffener(pl_position = 2, st_number = st_number_right, location = loc, i_along = I_collection[num])
                                                st_left = proposed_stiffener.proposed_stiffener(pl_position = 4, st_number = st_number_left, location = loc, i_along = I_collection[num])
                                                prop.stiffeners.append(st_right)
                                                prop.stiffeners.append(st_left)
                                                #create bottom siffeners
                                            for num in range(num_btm_stiffeners):
                                                loc_btm = 1 - 2/(num_btm_stiffeners+1)*(num+1)
                                                st_number = num_top_stiffeners + num_side_stiffeners + num + 1
                                                st = proposed_stiffener.proposed_stiffener(pl_position = 3, st_number = st_number, location = loc_btm, i_along = I_btm)
                                                prop.stiffeners.append(st)
                                            base_cs_copy = copy.deepcopy(base_cs)
                                            st_list_rest = substantiate.substantiate(base_cs_copy, prop)
                                            st_list = st_list_deck + st_list_rest
                                            test_cs = merge.merge(base_cs_copy, st_list)
                                            end_cs = buckling_proof.buckling_proof(test_cs)
                                            prop = stiffeners_proposition.stiffeners_proposition()
                                            proven = end_cs.eta_1 < 1 and end_cs.interaction_2 < 1 and end_cs.interaction_3 < 1 and end_cs.interaction_4 < 1
                                            if proven:
                                                if max(t_side, t_bottom) < t_max_min:
                                                    t_max_min = max(t_side, t_bottom)
                                                strong_enough = True
                                                cs_collection.add(end_cs)
                                                print(str(optimization_value.cost(end_cs)) + " CHF")
                                                print("PASS!")
                                            else:
                                                print("FAIL!")

    t_collection = []
    for t in t_range:
        if t <= t_max_min:
            t_collection.append(t)
    t_range = t_collection

    #three side stiffeners block
    num_side_stiffeners = 3
    for t_side in t_range:
        for t_bottom in t_range:
            base_cs = ics.create_initial_cs(b_sup, b_inf, h, t_side, t_deck, t_bottom)
            for num_btm_stiffeners in range(4):
                if num_side_stiffeners == 3:
                    #without bottom stiffeners
                    if num_btm_stiffeners == 0:
                        for I_side_btm in I_range:
                            for I_side_middle in I_range:
                                for I_side_top in I_range:
                                    I_collection = [I_side_top, I_side_middle, I_side_btm]
                                    locations_side = get_locations_side(num_side_stiffeners, sign)
                                    for loc_side in range(len(locations_side)):
                                        print("\n-------------------------------------------------------------------------------------------------------")
                                        print("------------------------------------ CS" +str(counter) + "---------------------------------------------------------------")
                                        counter += 1
                                        print("#Side Stiffeners " + str(num_side_stiffeners))
                                        print("#Btm Stiffeners " + str(num_btm_stiffeners))
                                        print("I_Side_Top " + str(I_side_top))
                                        print("I_Side_Bottom " + str(I_side_btm))
                                        print("I_Side_Middle" + str(I_side_middle))
                                        prop = stiffeners_proposition.stiffeners_proposition()
                                        for num in range(num_side_stiffeners):
                                            #create side stiffeners
                                            loc = locations_side[loc_side][num]
                                            print("Location Side" + str(loc))
                                            assert loc != -1, "Error!"
                                            st_number_right = num_top_stiffeners + num + 1
                                            st_number_left = num_top_stiffeners + num_btm_stiffeners + 2*num_side_stiffeners - num
                                            st_right = proposed_stiffener.proposed_stiffener(pl_position = 2, st_number = st_number_right, location = loc, i_along = I_collection[num])
                                            st_left = proposed_stiffener.proposed_stiffener(pl_position = 4, st_number = st_number_left, location = loc, i_along = I_collection[num])
                                            prop.stiffeners.append(st_right)
                                            prop.stiffeners.append(st_left)
                                        base_cs_copy = copy.deepcopy(base_cs)
                                        st_list_rest = substantiate.substantiate(base_cs_copy, prop)
                                        st_list = st_list_deck + st_list_rest
                                        test_cs = merge.merge(base_cs_copy, st_list)
                                        end_cs = buckling_proof.buckling_proof(test_cs)
                                        prop = stiffeners_proposition.stiffeners_proposition()
                                        proven = end_cs.eta_1 < 1 and end_cs.interaction_2 < 1 and end_cs.interaction_3 < 1 and end_cs.interaction_4 < 1
                                        if proven:
                                            if max(t_side, t_bottom) < t_max_min:
                                                t_max_min = max(t_side, t_bottom)
                                            strong_enough = True
                                            cs_collection.add(end_cs)
                                            print(str(optimization_value.cost(end_cs)) + " CHF")
                                            print("PASS!")
                                        else:
                                            print("FAIL!")
                    #with bottom stiffeners
                    else:
                        for I_side_btm in I_range:
                            for I_side_top in I_range:
                                for I_side_middle in I_range:
                                    I_collection = [I_side_top, I_side_middle, I_side_btm]
                                    locations_side = get_locations_side(num_side_stiffeners, sign)
                                    for loc_side in range(len(locations_side)):
                                        strong_enough = False
                                        for I_btm in I_range:
                                            if strong_enough == False:
                                                print("\n-------------------------------------------------------------------------------------------------------")
                                                print("------------------------------------ CS" +str(counter) + "---------------------------------------------------------------")
                                                counter += 1
                                                print("#Side Stiffeners " + str(num_side_stiffeners))
                                                print("#Btm Stiffeners " + str(num_btm_stiffeners))
                                                print("I_Side_Top " + str(I_side_top))
                                                print("I_Side_Middle " + str(I_side_middle))
                                                print("I_Side_Bottom " + str(I_side_btm))
                                                print("I_Btm " + str(I_btm))
                                                prop = stiffeners_proposition.stiffeners_proposition()
                                                for num in range(num_side_stiffeners):
                                                    #create side stiffeners
                                                    loc = locations_side[loc_side][num]
                                                    print("Location Side" + str(loc))
                                                    assert loc != -1, "Error!"
                                                    st_number_right = num_top_stiffeners + num + 1
                                                    st_number_left = num_top_stiffeners + num_btm_stiffeners + 2*num_side_stiffeners - num
                                                    st_right = proposed_stiffener.proposed_stiffener(pl_position = 2, st_number = st_number_right, location = loc, i_along = I_collection[num])
                                                    st_left = proposed_stiffener.proposed_stiffener(pl_position = 4, st_number = st_number_left, location = loc, i_along = I_collection[num])
                                                    prop.stiffeners.append(st_right)
                                                    prop.stiffeners.append(st_left)
                                                    #create bottom siffeners
                                                for num in range(num_btm_stiffeners):
                                                    loc_btm = 1 - 2/(num_btm_stiffeners+1)*(num+1)
                                                    st_number = num_top_stiffeners + num_side_stiffeners + num + 1
                                                    st = proposed_stiffener.proposed_stiffener(pl_position = 3, st_number = st_number, location = loc_btm, i_along = I_btm)
                                                    prop.stiffeners.append(st)
                                                base_cs_copy = copy.deepcopy(base_cs)
                                                st_list_rest = substantiate.substantiate(base_cs_copy, prop)
                                                st_list = st_list_deck + st_list_rest
                                                test_cs = merge.merge(base_cs_copy, st_list)
                                                end_cs = buckling_proof.buckling_proof(test_cs)
                                                prop = stiffeners_proposition.stiffeners_proposition()
                                                proven = end_cs.eta_1 < 1 and end_cs.interaction_2 < 1 and end_cs.interaction_3 < 1 and end_cs.interaction_4 < 1
                                                if proven:
                                                    if max(t_side, t_bottom) < t_max_min:
                                                        t_max_min = max(t_side, t_bottom)
                                                    strong_enough = True
                                                    cs_collection.add(end_cs)
                                                    print(str(optimization_value.cost(end_cs)) + " CHF")
                                                    print("PASS!")
                                                else:
                                                    print("FAIL!")

    print("# of passed CS")
    print(len(cs_collection))
    for cs in cs_collection:
        #go.print_cs_red(cs)
        pass
    return

def get_locations_side(num_side_stiffeners, sign):
    #always return locations in descending order
    if num_side_stiffeners == 0:
        return [(-1, -1, -1)]
    if num_side_stiffeners == 1:
        if sign == -1:
            return [(0.4, -1, -1), (0.3, -1, -1), (0.2, -1, -1), (0.1, -1, -1)]
        if sign == 1:
            return [(0.9, -1, -1), (0.8, -1, -1), (0.7, -1, -1), (0.6, -1, -1)]
    if num_side_stiffeners == 2:
        if sign == -1:
            return [(0.4, 0.3, -1), (0.4, 0.2, -1), (0.4, 0.1, -1), (0.3, 0.2, -1), (0.3, 0.1, -1), (0.2, 0.1, -1)]
        if sign == 1:
            return [(0.9, 0.8, -1), (0.9, 0.7, -1), (0.9, 0.6, -1),  (0.8, 0.7, -1), (0.8, 0.6, -1), (0.7, 0.6, -1)]
    if num_side_stiffeners == 3:
        if sign == -1:
            return [(0.4, 0.3, 0.2), (0.4, 0.3, 0.1), (0.4, 0.2, 0.1), (0.3, 0.2, 0.1)]
        if sign == 1:
            return [(0.9, 0.8, 0.7), (0.9, 0.8, 0.6),  (0.9, 0.7, 0.6), (0.8, 0.7, 0.6)]
