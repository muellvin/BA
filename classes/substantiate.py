from classes import stiffener as st
from classes import crosssection as cs
from classes import plate_code as plcd
from classes import line as ln
import defaults
import math
import numpy


from colorama import Fore
from colorama import Style


"""crossection values are needed"""
cs_b_sup = 4000 #data.input_data["b_sup"]
cs_b_inf = 2000 #data.input_data["b_inf"]
cs_h = 1500 #data.input_data["h"]

def substantiate(crosssection, propositions):
    #initialize list for stiffeners
    stiffener_list =[]

    if propositions.stiffeners == []:
        return []
    #switch clause for plates
    for stiffener in propositions.stiffeners:
        if stiffener.pl_position == 1:
            assert stiffener.deck_st == True, "stiffener at side 1 without beeing a deck stiffener from file deck"
            b_sup, b_inf, h, t = stiffener.b_sup, stiffener.b_inf, stiffener.h, stiffener.t
            #trackplate should not be called within the for loop
            #I_min = min_inertial_mom()
            #b_sup, b_inf, h, t = trackplate(I_min)
            side = 1
            angle = 0
        elif stiffener.pl_position == 2:
            b_sup, b_inf, h, t = find_dimensions(stiffener)
            side = 2
            angle = math.pi + crosssection.get_angle(side)
            #sidplate right side
        elif stiffener.pl_position == 3:
            b_sup, b_inf, h, t = find_dimensions(stiffener)
            side = 3
            angle = math.pi
            #bottom plate
            #make use of symmetry and equal stiffeners
        else:
            assert stiffener.pl_position == 4, "Plate not found."
            b_sup, b_inf, h, t = find_dimensions(stiffener)
            side = 4
            angle = math.pi - crosssection.get_angle(side)
            #make us of symmetry tbd
        y,z = crosssection.get_coordinates(stiffener.location, side)
        global_st = st.create_stiffener_global(stiffener.pl_position, stiffener.st_number, \
        y, z, angle, b_sup, b_inf, h, t)

        #check if code correct
        test = global_st.lines[0].code.pl_position
        stiffener_list.append(global_st)

    print(" ")
    print(" ")
    #This function return a list of stiffeners in the global coordinate system
    return stiffener_list

    #check if values are still set to default
    #idea: always keep one variable free and iterate through the others

def find_dimensions(stiffener):
    print("------------------- find_dimensions for stiffener ", stiffener.st_number,"------------------------------------------")

    #initialize dimensions container
    #b_sup, b_inf, h, t, mass
    best = [0,0,0,0,0]

    #set minimal default values and step size for range
    b_inf_minimal = defaults.b_inf_minimal
    b_inf_step = defaults.b_inf_step
    b_sup_minimal = defaults.b_sup_minimal
    b_sup_step = defaults.b_sup_step
    b_sup_minimal = defaults.b_sup_minimal
    h_minimal = defaults.h_minimal
    h_step = defaults.h_step
    t_range = defaults.t_range
    max_angle = defaults.max_angle

    #max values, are changed in case of geometrical restrictions
    b_inf_max_geo = defaults.b_inf_maximal
    b_sup_max_geo = defaults.b_sup_maximal
    h_max_geo = defaults.h_maximal




    #set new default values, if corrections need to be made
    if stiffener.b_sup_corr == True:
        b_sup_max_geo = stiffener.b_sup
        assert b_sup_max_geo > b_sup_minimal, "Error, nothing could be found"

    if stiffener.h_corr == True:
        h_max_geo = stiffener.h
        assert h_max_geo > h_step, "Error, nothing could be found."


    best = [0,0,0,0,10**10]
    best_default = best

    if stiffener.b_sup_corr == True and defaults.do_height_only == True:
        print("given b_sup, only correcting heights")
        b_sup = stiffener.b_sup
        h_min = h_minimal
        h_max_angle = math.tan(max_angle) * (b_sup/2 - b_inf_minimal/2)
        h_max = 10*math.floor(min(h_max_geo, h_max_angle)/10)
        print("b_sup: ",math.floor(b_sup),"   h: ",math.floor(h_min),"-",math.floor(h_max),"   I: ",math.floor(stiffener.i_along))
        #assert h_max > h_min, "Error, nothing could be found: subst"
        if h_max < h_min:
            h_max = h_min

        for h in range(h_min, h_max, h_step):
            b_inf_min = b_inf_minimal
            b_inf_max = 10*math.floor(min(max(0,b_sup - 2*h/math.tan(max_angle)), b_inf_max_geo)/10)
            if b_inf_min < b_inf_max:
                for b_inf in range(b_inf_min, b_inf_max, b_inf_step):
                    for t in t_range:
                        I_a = st.get_i_along_stiffener(b_sup, b_inf, h, t)
                        m = st.get_area_stiffener(b_sup, b_inf, h, t) #get_area to be implemented
                        if I_a > stiffener.i_along:
                            if m < best[4]:
                                print("b_sup: ",b_sup," b_inf: ",b_inf," h: ",h," t: ",t)
                                best = [b_sup, b_inf, h, t, m]
                        elif h == h_min and b_inf == b_inf_min and t == t_range[0]:
                            print("b_sup: ",b_sup," b_inf: ",b_inf," h: ",h," t: ",t)
                            m = 10**8
                            best = [b_sup, b_inf, h, t, m]
        if best == best_default:
            h = min(10*math.floor(b_sup/math.tan(max_angle)/10),h_max)
            b_inf = b_sup - 2*1/math.sin(h)
            best = [b_sup, b_inf, h ,5]

    else:
        assert b_sup_max_geo >= b_sup_minimal
        for b_sup in range(b_sup_minimal, b_sup_max_geo, b_sup_step):
            h_min = h_minimal
            h_max = 10*math.floor(min(h_max_geo, math.sin(max_angle)*b_sup/2)/10)
            if h_max > h_min:
                for h in range(h_min, h_max, h_step):
                    b_inf_min = b_inf_minimal
                    b_inf_max = 10*math.floor(min(max(0,b_sup - 2*h/math.tan(max_angle)), b_inf_max_geo)/10)
                    if b_inf_min < b_inf_max:
                        for b_inf in range(b_inf_min, b_inf_max, b_inf_step):
                            for t in t_range:
                                I_a = st.get_i_along_stiffener(b_sup, b_inf, h, t)
                                if I_a > stiffener.i_along:
                                    m = st.get_area_stiffener(b_sup, b_inf, h, t) #get_area to be implemented
                                    if m < best[4]:
                                        #print("b_sup: ",b_sup," b_inf: ",b_inf," h: ",h," t: ",t)
                                        best = [b_sup, b_inf, h, t, m]

        if best == best_default:
            best = [b_sup_minimal, b_inf_minimal, 10*math.floor(b_sup_minimal*math.tan(max_angle)/10) ,5]

    b_sup = best[0]
    b_inf = best[1]
    h = best[2]
    t = best[3]
    if stiffener.b_sup_corr == True:
        print("correction b_sup:", stiffener.b_sup_corr_val)
    if stiffener.b_inf_corr == True:
        print("correction b_inf:", stiffener.b_inf_corr_val)
    if stiffener.h_corr == True:
        print("correction h:", stiffener.h_corr_val)
    print("chosen dimensions:         b_sup: ",math.floor(b_sup),"        b_inf: ",b_inf,"         h: ",h,"          t:",t)
    print(" ")
        #print(f"{Fore.GREEN}No corrections were needed {Style.RESET_ALL}")


    stiffener.b_inf = 0
    stiffener.b_sup = 0
    stiffener.h = 0
    stiffener.b_inf_corr = False
    stiffener.b_sup_corr = False
    stiffener.h_corr = False
    stiffener.b_inf_corr_val = False
    stiffener.b_sup_corr_val = False
    stiffener.h_corr_val = False
    return b_sup, b_inf, h, t
