import math
import copy
import sys
from classes import crosssection
from classes import proposed_stiffener
from classes import stiffeners_proposition
from deck_and_initial_cs import initial_cs
from deck_and_initial_cs import deck
from assembly import add_stiffeners
from assembly import merge
from proofs_and_stress_calculation import buckling_proof
from proofs_and_stress_calculation import stress_cal
from data_and_defaults import defaults
from data_and_defaults import data
from cs_optimization_tool import optimization_value
from cs_optimization_tool import cs_collector
sys.path.insert(0, './user_interface')
from output import printing

#Optimizer Iterative Steps
def optimize():
    b_sup = data.input_data["b_sup"]
    b_inf = data.input_data["b_inf"]
    h = data.input_data["h"]
    t_deck = data.input_data["t_deck"]
    t_range = copy.deepcopy(defaults.t_range_opt)
    t_max_min = max(t_range)
    I_range = defaults.I_range
    counter = 1
    bottom_max = defaults.num_bottom_stiffeners_max
    side_max = defaults.num_side_stiffeners_max
    st_prop_deck = deck.deck(b_sup, True)
    num_top_stiffeners = len(st_prop_deck.stiffeners)
    m_ed = data.input_data.get("M_Ed")
    sign = math.copysign(1, m_ed)

    #no side stiffener block
    num_side_stiffeners = 0
    if num_side_stiffeners <= side_max:
        for t_side in t_range:
            for t_bottom in t_range:
                base_cs = initial_cs.create_initial_cs(b_sup, b_inf, h, t_side, t_deck, t_bottom)
                for num_btm_stiffeners in range(bottom_max+1):
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
                            print("t_bottom:" + str(t_bottom))
                            print("t_side:" + str(t_side))
                            test_cs = copy.deepcopy(base_cs)
                            if test_cs != False:
                                #proof
                                end_cs = buckling_proof.buckling_proof(test_cs)
                                st_prop_rest = stiffeners_proposition.stiffeners_proposition()
                                if end_cs.proven():
                                    if max(t_side, t_bottom) < t_max_min:
                                        t_max_min = max(t_side, t_bottom)
                                    print("PASS!")
                                    cs_collector.into_collector(end_cs)
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
                                    st_prop = stiffeners_proposition.stiffeners_proposition()
                                    st_prop_rest = stiffeners_proposition.stiffeners_proposition()
                                    for num in range(num_btm_stiffeners):
                                        loc_btm = -1 + 2/(num_btm_stiffeners+1)*(num+1)
                                        st_number = num_top_stiffeners + num_side_stiffeners + num + 1
                                        st = proposed_stiffener.proposed_stiffener(pl_position = 3, st_number = st_number, location = loc_btm, i_along = I_btm)
                                        st_prop_rest.stiffeners.append(st)
                                    st_prop.stiffeners = st_prop_deck.stiffeners + st_prop_rest.stiffeners
                                    st_prop.stiffeners = sorted(st_prop.stiffeners, key = lambda proposed_stiffener: proposed_stiffener.st_number)
                                    test_cs = add_stiffeners.add_stiffener_set(base_cs, st_prop, "b")
                                    if test_cs != False:
                                        #proof
                                        end_cs = buckling_proof.buckling_proof(test_cs)
                                        st_prop_rest = stiffeners_proposition.stiffeners_proposition()
                                        st_prop_rest = stiffeners_proposition.stiffeners_proposition()
                                        if end_cs.proven():
                                            if max(t_side, t_bottom) < t_max_min:
                                                t_max_min = max(t_side, t_bottom)
                                            strong_enough = True
                                            cs_collector.into_collector(end_cs)
                                            print("PASS!")
                                        else:
                                            print("FAIl!")
        #set net maximum plate thickness
        t_collection = []
        for t in t_range:
            if t <= t_max_min:
                t_collection.append(t)
        t_range = t_collection


    #one side stiffener block
    num_side_stiffeners = 1
    if num_side_stiffeners <= side_max:
        for t_side in t_range:
            for t_bottom in t_range:
                base_cs = initial_cs.create_initial_cs(b_sup, b_inf, h, t_side, t_deck, t_bottom)
                for num_btm_stiffeners in range(bottom_max+1):
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
                                        st_prop = stiffeners_proposition.stiffeners_proposition()
                                        st_prop_rest = stiffeners_proposition.stiffeners_proposition()
                                        for num in range(num_side_stiffeners):
                                            #create side stiffeners
                                            loc = locations_side[loc_side][num]
                                            assert loc != -1, "Error!"
                                            st_number_right = num_top_stiffeners + num + 1
                                            st_number_left = num_top_stiffeners + num_btm_stiffeners + 2*num_side_stiffeners - num
                                            st_right = proposed_stiffener.proposed_stiffener(pl_position = 2, st_number = st_number_right, location = loc, i_along = I_side)
                                            st_left = proposed_stiffener.proposed_stiffener(pl_position = 4, st_number = st_number_left, location = loc, i_along = I_side)
                                            st_prop_rest.stiffeners.append(st_right)
                                            st_prop_rest.stiffeners.append(st_left)
                                        st_prop.stiffeners = st_prop_deck.stiffeners + st_prop_rest.stiffeners
                                        st_prop.stiffeners = sorted(st_prop.stiffeners, key = lambda proposed_stiffener: proposed_stiffener.st_number)
                                        test_cs = add_stiffeners.add_stiffener_set(base_cs, st_prop, "b")
                                        if test_cs != False:
                                            #proof
                                            end_cs = buckling_proof.buckling_proof(test_cs)
                                            st_prop_rest = stiffeners_proposition.stiffeners_proposition()
                                            if end_cs.proven():
                                                if max(t_side, t_bottom) < t_max_min:
                                                    t_max_min = max(t_side, t_bottom)
                                                strong_enough = True
                                                cs_collector.into_collector(end_cs)
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
                                            st_prop = stiffeners_proposition.stiffeners_proposition()
                                            st_prop_rest = stiffeners_proposition.stiffeners_proposition()
                                            for num in range(num_side_stiffeners):
                                                #create side stiffeners
                                                loc = locations_side[loc_side][num]
                                                assert loc != -1, "Error!"
                                                st_number_right = num_top_stiffeners + num + 1
                                                st_number_left = num_top_stiffeners + num_btm_stiffeners + 2*num_side_stiffeners - num
                                                st_right = proposed_stiffener.proposed_stiffener(pl_position = 2, st_number = st_number_right, location = loc, i_along = I_side)
                                                st_left = proposed_stiffener.proposed_stiffener(pl_position = 4, st_number = st_number_left, location = loc, i_along = I_side)
                                                st_prop_rest.stiffeners.append(st_right)
                                                st_prop_rest.stiffeners.append(st_left)
                                                #create bottom siffeners
                                            for num in range(num_btm_stiffeners):
                                                loc_btm = -1 + 2/(num_btm_stiffeners+1)*(num+1)
                                                st_number = num_top_stiffeners + num_side_stiffeners + num + 1
                                                st = proposed_stiffener.proposed_stiffener(pl_position = 3, st_number = st_number, location = loc_btm, i_along = I_btm)
                                                st_prop_rest.stiffeners.append(st)
                                            st_prop.stiffeners = st_prop_deck.stiffeners + st_prop_rest.stiffeners
                                            st_prop.stiffeners = sorted(st_prop.stiffeners, key = lambda proposed_stiffener: proposed_stiffener.st_number)
                                            test_cs = add_stiffeners.add_stiffener_set(base_cs, st_prop, "b")
                                            if test_cs != False:
                                                #proof
                                                end_cs = buckling_proof.buckling_proof(test_cs)
                                                st_prop_rest = stiffeners_proposition.stiffeners_proposition()
                                                if end_cs.proven():
                                                    if max(t_side, t_bottom) < t_max_min:
                                                        t_max_min = max(t_side, t_bottom)
                                                    strong_enough = True
                                                    cs_collector.into_collector(end_cs)
                                                    print("PASS!")
                                                else:
                                                    print("FAIL!")
        #set new maximum plate thickness
        t_collection = []
        for t in t_range:
            if t <= t_max_min:
                t_collection.append(t)
        t_range = t_collection

    #two side stiffeners block
    num_side_stiffeners = 2
    if num_side_stiffeners <= side_max:
        for t_side in t_range:
            for t_bottom in t_range:
                base_cs = initial_cs.create_initial_cs(b_sup, b_inf, h, t_side, t_deck, t_bottom)
                for num_btm_stiffeners in range(bottom_max+1):
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
                                        st_prop = stiffeners_proposition.stiffeners_proposition()
                                        st_prop_rest = stiffeners_proposition.stiffeners_proposition()
                                        for num in range(num_side_stiffeners):
                                            #create side stiffeners
                                            loc = locations_side[loc_side][num]
                                            assert loc != -1, "Error!"
                                            st_number_right = num_top_stiffeners + num + 1
                                            st_number_left = num_top_stiffeners + num_btm_stiffeners + 2*num_side_stiffeners - num
                                            st_right = proposed_stiffener.proposed_stiffener(pl_position = 2, st_number = st_number_right, location = loc, i_along = I_collection[num])
                                            st_left = proposed_stiffener.proposed_stiffener(pl_position = 4, st_number = st_number_left, location = loc, i_along = I_collection[num])
                                            st_prop_rest.stiffeners.append(st_right)
                                            st_prop_rest.stiffeners.append(st_left)
                                        st_prop.stiffeners = st_prop_deck.stiffeners + st_prop_rest.stiffeners
                                        st_prop.stiffeners = sorted(st_prop.stiffeners, key = lambda proposed_stiffener: proposed_stiffener.st_number)
                                        test_cs = add_stiffeners.add_stiffener_set(base_cs, st_prop, "b")
                                        if test_cs != False:
                                            #proof
                                            end_cs = buckling_proof.buckling_proof(test_cs)
                                            st_prop_rest = stiffeners_proposition.stiffeners_proposition()
                                            if end_cs.proven():
                                                if max(t_side, t_bottom) < t_max_min:
                                                    t_max_min = max(t_side, t_bottom)
                                                cs_collector.into_collector(end_cs)
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
                                                st_prop = stiffeners_proposition.stiffeners_proposition()
                                                st_prop_rest = stiffeners_proposition.stiffeners_proposition()
                                                for num in range(num_side_stiffeners):
                                                    #create side stiffeners
                                                    loc = locations_side[loc_side][num]
                                                    assert loc != -1, "Error!"
                                                    st_number_right = num_top_stiffeners + num + 1
                                                    st_number_left = num_top_stiffeners + num_btm_stiffeners + 2*num_side_stiffeners - num
                                                    st_right = proposed_stiffener.proposed_stiffener(pl_position = 2, st_number = st_number_right, location = loc, i_along = I_collection[num])
                                                    st_left = proposed_stiffener.proposed_stiffener(pl_position = 4, st_number = st_number_left, location = loc, i_along = I_collection[num])
                                                    st_prop_rest.stiffeners.append(st_right)
                                                    st_prop_rest.stiffeners.append(st_left)
                                                    #create bottom siffeners
                                                for num in range(num_btm_stiffeners):
                                                    loc_btm = -1 + 2/(num_btm_stiffeners+1)*(num+1)
                                                    st_number = num_top_stiffeners + num_side_stiffeners + num + 1
                                                    st = proposed_stiffener.proposed_stiffener(pl_position = 3, st_number = st_number, location = loc_btm, i_along = I_btm)
                                                    st_prop_rest.stiffeners.append(st)
                                                st_prop.stiffeners = st_prop_deck.stiffeners + st_prop_rest.stiffeners
                                                st_prop.stiffeners = sorted(st_prop.stiffeners, key = lambda proposed_stiffener: proposed_stiffener.st_number)
                                                test_cs = add_stiffeners.add_stiffener_set(base_cs, st_prop, "b")
                                                if test_cs != False:
                                                    #proof
                                                    end_cs = buckling_proof.buckling_proof(test_cs)
                                                    st_prop_rest = stiffeners_proposition.stiffeners_proposition()
                                                    if end_cs.proven():
                                                        if max(t_side, t_bottom) < t_max_min:
                                                            t_max_min = max(t_side, t_bottom)
                                                        strong_enough = True
                                                        cs_collector.into_collector(end_cs)
                                                        print("PASS!")
                                                    else:
                                                        print("FAIL!")

        #set new maximum plate thickness
        t_collection = []
        for t in t_range:
            if t <= t_max_min:
                t_collection.append(t)
        t_range = t_collection

    #three side stiffeners block
    num_side_stiffeners = 3
    if num_side_stiffeners <= side_max:
        for t_side in t_range:
            for t_bottom in t_range:
                base_cs = initial_cs.create_initial_cs(b_sup, b_inf, h, t_side, t_deck, t_bottom)
                for num_btm_stiffeners in range(bottom_max+1):
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
                                            st_prop = stiffeners_proposition.stiffeners_proposition()
                                            st_prop_rest = stiffeners_proposition.stiffeners_proposition()
                                            for num in range(num_side_stiffeners):
                                                #create side stiffeners
                                                loc = locations_side[loc_side][num]
                                                assert loc != -1, "Error!"
                                                st_number_right = num_top_stiffeners + num + 1
                                                st_number_left = num_top_stiffeners + num_btm_stiffeners + 2*num_side_stiffeners - num
                                                st_right = proposed_stiffener.proposed_stiffener(pl_position = 2, st_number = st_number_right, location = loc, i_along = I_collection[num])
                                                st_left = proposed_stiffener.proposed_stiffener(pl_position = 4, st_number = st_number_left, location = loc, i_along = I_collection[num])
                                                st_prop_rest.stiffeners.append(st_right)
                                                st_prop_rest.stiffeners.append(st_left)
                                            st_prop.stiffeners = st_prop_deck.stiffeners + st_prop_rest.stiffeners
                                            st_prop.stiffeners = sorted(st_prop.stiffeners, key = lambda proposed_stiffener: proposed_stiffener.st_number)
                                            test_cs = add_stiffeners.add_stiffener_set(base_cs, st_prop, "b")
                                            if test_cs != False:
                                                #proof
                                                end_cs = buckling_proof.buckling_proof(test_cs)
                                                st_prop_rest = stiffeners_proposition.stiffeners_proposition()
                                                if end_cs.proven():
                                                    if max(t_side, t_bottom) < t_max_min:
                                                        t_max_min = max(t_side, t_bottom)
                                                    strong_enough = True
                                                    cs_collector.into_collector(end_cs)
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
                                                    st_prop = stiffeners_proposition.stiffeners_proposition()
                                                    st_prop_rest = stiffeners_proposition.stiffeners_proposition()
                                                    for num in range(num_side_stiffeners):
                                                        #create side stiffeners
                                                        loc = locations_side[loc_side][num]
                                                        assert loc != -1, "Error!"
                                                        st_number_right = num_top_stiffeners + num + 1
                                                        st_number_left = num_top_stiffeners + num_btm_stiffeners + 2*num_side_stiffeners - num
                                                        st_right = proposed_stiffener.proposed_stiffener(pl_position = 2, st_number = st_number_right, location = loc, i_along = I_collection[num])
                                                        st_left = proposed_stiffener.proposed_stiffener(pl_position = 4, st_number = st_number_left, location = loc, i_along = I_collection[num])
                                                        st_prop_rest.stiffeners.append(st_right)
                                                        st_prop_rest.stiffeners.append(st_left)
                                                        #create bottom siffeners
                                                    for num in range(num_btm_stiffeners):
                                                        loc_btm = -1 + 2/(num_btm_stiffeners+1)*(num+1)
                                                        st_number = num_top_stiffeners + num_side_stiffeners + num + 1
                                                        st = proposed_stiffener.proposed_stiffener(pl_position = 3, st_number = st_number, location = loc_btm, i_along = I_btm)
                                                        st_prop_rest.stiffeners.append(st)
                                                    st_prop.stiffeners = st_prop_deck.stiffeners + st_prop_rest.stiffeners
                                                    st_prop.stiffeners = sorted(st_prop.stiffeners, key = lambda proposed_stiffener: proposed_stiffener.st_number)
                                                    test_cs = add_stiffeners.add_stiffener_set(base_cs, st_prop, "b")
                                                    if test_cs != False:
                                                        #proof
                                                        end_cs = buckling_proof.buckling_proof(test_cs)
                                                        st_prop_rest = stiffeners_proposition.stiffeners_proposition()
                                                        if end_cs.proven():
                                                            if max(t_side, t_bottom) < t_max_min:
                                                                t_max_min = max(t_side, t_bottom)
                                                            strong_enough = True
                                                            cs_collector.into_collector(end_cs)
                                                            print("PASS!")
                                                        else:
                                                            print("FAIL!")

    printing.print_best()
    return

#function that returns locations where stiffeners should be placed
def get_locations_side(num_side_stiffeners, sign):
    #always return locations in descending order
    if num_side_stiffeners == 0:
        return [(-1, -1, -1)]
    if num_side_stiffeners == 1:
        if sign == -1:
            return [(0.6, -1, -1), (0.5, -1, -1), (0.4, -1, -1), (0.3, -1, -1), (0.2, -1, -1)]
        if sign == 1:
            return [(0.8, -1, -1), (0.7, -1, -1), (0.6, -1, -1), (0.5, -1, -1), (0.4, -1, -1)]
    if num_side_stiffeners == 2:
        if sign == -1:
            locations = []
            for i in reversed(range(20, 70, 10)):
                for j in reversed(range(20, i, 10)):
                    combination = (i/100, j/100, -1)
                    locations.append(combination)
            return locations
        if sign == 1:
            locations = []
            for i in reversed(range(40, 90, 10)):
                for j in reversed(range(40, i, 10)):
                    combination = (i/100, j/100, -1)
                    locations.append(combination)
            return locations
    if num_side_stiffeners == 3:
        if sign == -1:
            locations = []
            for i in reversed(range(20, 70, 10)):
                for j in reversed(range(20, i, 10)):
                    for k in reversed(range(20, j, 10)):
                        combination = (i/100, j/100, k/100)
                        locations.append(combination)
            return locations
        if sign == 1:
            locations = []
            for i in reversed(range(40, 90, 10)):
                for j in reversed(range(40, i, 10)):
                    for k in reversed(range(40, j, 10)):
                        combination = (i/100, j/100, k/100)
                        locations.append(combination)
            return locations
