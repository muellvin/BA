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
    print(" ")
    print(" ")
    #switch clause for plates
    for stiffener in propositions.stiffeners:
        if stiffener.pl_position == 1:
            #trackplate should not be called within the for loop
            I_min = min_inertial_mom()
            b_sup, b_inf, h, t = trackplate(I_min)
            code = plcd.plate_code(1,0,1,0,0)
            angle = 0
        elif stiffener.pl_position == 2:
            b_sup, b_inf, h, t = find_dimensions(stiffener)
            code = plcd.plate_code(2,0,2,0,0)
            angle = math.pi + crosssection.get_angle(code)
            #sidplate right side
        elif stiffener.pl_position == 3:
            b_sup, b_inf, h, t = find_dimensions(stiffener)
            code = plcd.plate_code(3,0,3,0,0)
            angle = math.pi
            #bottom plate
            #make use of symmetry and equal stiffeners
        else:
            assert stiffener.pl_position == 4, "Plate not found."
            b_sup, b_inf, h, t = find_dimensions(stiffener)
            code = plcd.plate_code(4,0,4,0,0)
            angle = math.pi - crosssection.get_angle(code)
            #make us of symmetry tbd
        y,z = crosssection.get_coordinates(stiffener.location, code)
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
    #max values, are changed in case of geometrical restrictions
    b_inf_max_geo = defaults.b_inf_maximal
    b_sup_max_geo = defaults.b_sup_maximal
    h_max_geo = defaults.h_maximal

    locationchange = False
    error_inf = 0
    error_sup = 0


    #set new default values, if corrections need to be made
    if stiffener.b_inf_corr == True:
        if stiffener.b_inf > b_inf_minimal:
            b_inf_max_geo = stiffener.b_inf
            print("no location change, b_inf_max_geo: ",b_inf_max_geo)
        else:
            locationchange = True
            error_inf = b_inf_minimal - stiffener.b_inf
            b_inf_max_geo = b_inf_minimal
            stiffener.b_inf = b_inf_minimal
            print("location change, b_inf_max_geo: ",b_inf_max_geo)

    if stiffener.b_sup_corr == True:
        if stiffener.b_sup > b_sup_minimal:
            b_sup_max_geo = min(10*math.floor((stiffener.b_sup)/10), stiffener.b_sup)
            print("no location change, b_sup_max_geo: ",b_sup_max_geo)
        else:
            locationchange = True
            error_sup = b_sup_minimal - stiffener.b_sup
            b_sup_max_geo = b_sup_minimal
            stiffener.b_sup = b_sup_minimal
            print("location change, b_sup_max_geo: ",b_sup_max_geo)


    #if the inferior one is negative then both are
    if locationchange == True:
        error = max(error_inf, error_sup)
        if stiffener.pl_position == 2 or stiffener.pl_position == 4:
            if stiffener.location > 0.5: stiffener.location -= error*1.3/cs_h
            elif stiffener.location <= 0.5: stiffener.location += error*1.3/cs_h
        elif stiffener.pl_position == 3:
            if stiffener.location > 0: stiffener.location -= error*1.3/cs_b_inf
            elif stiffener.location < 0: stiffener.location += error*1.3/cs_b_inf

    if stiffener.height_corr == True:
        h_max_geo = stiffener.height
        print("h_max_geo: ",h_max_geo)
        assert h_max_geo > h_step, "Error, nothing could be found."

    print("location change: ",locationchange,"   b_sup: ",b_sup_minimal,"-",b_sup_max_geo,"   b_inf: ",b_inf_minimal,"-",b_sup_max_geo,"   h: ",h_minimal,"-",h_max_geo)
    #iterate through all the possible solutions, in order to find viable ones

    #still make restriction for angle in for-loop and possibly other restrictions...
    best = [0,0,0,0,10**8]
    best_default = best
    max_angle = defaults.max_angle
    assert b_sup_max_geo >= b_sup_minimal

    for b_sup in range(b_sup_minimal, b_sup_max_geo, b_sup_step):
        h_min = h_minimal
        h_max = 10*math.floor(min(h_max_geo, math.sin(max_angle)*b_sup/2)/10)
        if h_max > h_min:
            for h in range(h_min, h_max, h_step):
                b_inf_min = b_inf_minimal
                b_inf_max = 10*math.floor(min(max(0,b_sup/2 - h/math.tan(max_angle)), b_inf_max_geo)/10)
                if b_inf_min < b_inf_max:
                    for b_inf in range(b_inf_min, b_inf_max, b_inf_step):
                        for t in t_range:
                            I_a = st.get_i_along_stiffener(b_sup, b_inf, h, t)
                            if I_a > stiffener.i_along:
                                m = st.get_area_stiffener(b_sup, b_inf, h, t) #get_area to be implemented
                                if m < best[4]:
                                    print("b_sup: ",b_sup," b_inf: ",b_inf," h: ",h," t: ",t)
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
    if stiffener.height_corr == True:
        print("correction height:", stiffener.height_corr_val)
    print("chosen dimensions:         b_sup: ",b_sup,"        b_inf: ",b_inf,"         h: ",h,"          t:",t)
    print(" ")
        #print(f"{Fore.GREEN}No corrections were needed {Style.RESET_ALL}")


    stiffener.b_inf = 0
    stiffener.b_sup = 0
    stiffener.height = 0
    stiffener.b_inf_corr = False
    stiffener.b_sup_corr = False
    stiffener.height_corr = False
    stiffener.b_inf_corr_val = False
    stiffener.b_sup_corr_val = False
    stiffener.height_corr_val = False
    return b_sup, b_inf, h, t
