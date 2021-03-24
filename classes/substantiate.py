from classes import stiffener as st
from classes import crosssection as cs
from classes import plate_code as plcd
from classes import line as ln
import math

def substantiate(crosssection, propositions):
    #initialize list for stiffeners
    stiffener_list =[]

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

    #This function return a list of stiffeners in the global coordinate system
    return stiffener_list

    #check if values are still set to default
    #idea: always keep one variable free and iterate through the others

def find_dimensions(stiffener):
    #initialize dimensions container
    #b_sup, b_inf, h, t, mass
    best = [0,0,0,0,0]
    #set maximum default values and step size for range
    b_inf_max_geo = 500
    b_inf_step = 20
    b_sup_max_geo = 500
    b_sup_step = 20
    h_max_geo = 200
    h_step = 10
    t_range = [5,7,9,11,13,15,17,20]

    #set new default values, if corrections need to be made
    if stiffener.b_inf != 0:
        b_inf_max_geo = stiffener.b_inf
        assert b_inf_max_geo > b_inf_step, "Error, nothing could be found."

    if stiffener.b_sup != 0:
        b_sup_max_geo = 10*math.floor(stiffener.b_sup/10)
        assert b_sup_max_geo > b_sup_step, "Error, nothing could be found."

    if stiffener.height != 0:
        h_max_geo = stiffener.height
        assert h_max_geo > h_step, "Error, nothing could be found."

    #iterate through all the possible solutions, in order to find viable ones

    #still make restriction for angle in for-loop and possibly other restrictions...
    best = [0,0,0,0,10**8]
    assert b_sup_max_geo > 50
    for b_sup in range(50, b_sup_max_geo, b_sup_step):
        h_max = 10*math.floor(min(h_max_geo, 0.5*math.sqrt(3)*b_sup)/10)
        if h_max > 30:
            for h in range(30, h_max, h_step):
                b_inf_min = 10*math.floor(max(0,b_sup - 2*h)/10)
                b_inf_max = 10*math.floor(min(b_sup - 2*h/math.tan(math.pi/3), b_inf_max_geo)/10)
                if b_inf_min < b_inf_max:
                    for b_inf in range(b_inf_min, b_inf_max, b_inf_step):
                        for t in t_range:
                            I_a = st.get_i_along_stiffener(b_sup, b_inf, h, t)
                            if I_a > stiffener.i_along:
                                m = st.get_area_stiffener(b_sup, b_inf, h, t) #get_area to be implemented
                                if m < best[4]:
                                    best = [b_sup, b_inf, h, t, m]

    b_sup = best[0]
    b_inf = best[1]
    h = best[2]
    t = best[3]
    print(b_sup, b_inf, h, t)
    return b_sup, b_inf, h, t

def trackplate():
    #returns the dimensions for a track plate stiffener
    #thickness of plate itself should somewhere be set to 16mm! --> tbd

    #set maximum default values and step size for range
    b_inf_max_geo = 500
    b_inf_step = 10
    h_max_geo = 200
    h_step = 5
    #must be >6mm according to EC 3-2
    t_range = [7,9,11,13,15,17,20]

    #b_sup, b_inf, h, t, mass
    best = [0,0,0,0,10**8]

    #iterate through all the possible solutions, in order to find viable ones
    assert b_sup_max_geo > 50
    for t in t_range:
        b_sup = min(25*t, 300)
        b_inf_min = 10*math.floor(max(0,b_sup - 2*h)/10)
        b_inf_max = 10*math.floor(min(b_sup - 2*h/math.tan(math.pi/3), b_inf_max_geo)/10)
        if b_inf_min < b_inf_max:
            for b_inf in range(b_inf_min, b_inf_max, b_inf_step):
                for h in range(30, h_max, h_step):
                    I_a = st.get_i_along_stiffener(b_sup, b_inf, h, t)
                    if I_a > stiffener.i_along:
                        m = st.get_area_stiffener(b_sup, b_inf, h, t) #get_area to be implemented
                        if m < best[4]:
                            best = [b_sup, b_inf, h, t, m]

    b_sup = best[0]
    b_inf = best[1]
    h = best[2]
    t = best[3]
    return b_sup, b_inf, h, t


def min_inertial_mom(a):
    #returns the minimal required inertial moment of the track plate according to EC-3 2
    #This inertial momenent is calculated with the track plate
    #Lower Inertial moments for stiffeners in the corners should be considered
    #Minimal value of track plate thickness should be considered somewhere
    I = 15*10**6
    return I
