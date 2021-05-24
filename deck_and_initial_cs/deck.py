import math
from data_and_defaults import defaults
from data_and_defaults import data
from classes import point
from classes import line
from classes import crosssection
from classes import plate_code
from classes import stiffeners_proposition
from classes import proposed_stiffener
from assembly import add_stiffeners


#function that returns deck stiffeners for a given cross section
def deck(b_deck, as_prop):
    #get the minimal required inertial moment according to EC 3-2
    min_Iy = min_inertial_mom()
    #choose correct value according to EC 3-2, C.1.2.2. in the defaults
    t_deck = defaults.t_deck
    #set maximum default values and step size for range
    h_max = defaults.h_maximal
    h_step = defaults.h_step
    h_min = defaults.h_minimal

    #must be >6mm according to EC 3-2, C.1.2.2.
    t_range = [8,10,12,15,16,18,20]

    #b_sup, b_inf, h, t, mass
    best = [0,0,0,0,10**8]

    #iterate through all the possible solutions, in order to find viable ones
    for t in t_range:
        b_sup_theor = min(25*t, 300)
        num_of_plates = math.ceil(b_deck / b_sup_theor)
        if num_of_plates % 2 == 0:
            num_of_plates += 1
        assert num_of_plates % 2 == 1, "You are stupid!"
        num_of_stiffeners = (num_of_plates-1)/2
        b_sup = b_deck / num_of_plates

        #assume the stiffener angle to be 75°
        for h in range(h_min, h_max, h_step):
            b_inf = b_sup - 2*h / math.tan(defaults.max_angle)
            #arbitrary value for evaluation
            if b_inf > 3*t:
                deck_stiffener = create_deck_stiffener_local(b_sup, b_inf, h, t, t_deck)
                I_a = deck_stiffener.get_i_y_tot()
                if I_a > min_Iy:
                    m = num_of_stiffeners*deck_stiffener.get_area_tot()
                    if m < best[4]:
                        best = [b_sup, b_inf, h, t, m]

    b_sup = best[0]
    b_inf = best[1]
    h = best[2]
    t = best[3]
    assert best[4] != 10**8, "You are Stupid."

    #For the optimizer: return stiffeners as propositions
    if as_prop == True:
        deck_st_prop = stiffeners_proposition.stiffeners_proposition()
        num_of_plates = round(b_deck / b_sup)
        num_of_stiffeners = (num_of_plates-1)/2

        for i in range(int(num_of_stiffeners)):
            center_y = (0.5*b_deck - (2*i+1.5)*b_sup)/b_deck*2
            st_prop = proposed_stiffener.proposed_stiffener(1, i+1, center_y, min_Iy, b_sup, b_inf, h, t)
            st_prop.deck_st = True
            deck_st_prop.add(st_prop)
        return deck_st_prop

    #For the Analysis Tool: return stiffeners as stiffeners
    elif as_prop == False:
        #create a list of deck stiffeners
        deck_stiffener_list = []
        num_of_plates = round(b_deck / b_sup)
        num_of_stiffeners = (num_of_plates-1)/2
        for i in range(int(num_of_stiffeners)):
            center_y = (0.5*b_deck - (2*i+1.5)*b_sup)
            stiffener_cs = add_stiffeners.create_stiffener_global(1, i+1, center_y, 0, 0, b_sup, b_inf, h, t)
            deck_stiffener_list.append(stiffener_cs)
        return deck_stiffener_list

#returns the minimal required inertial moment of the track plate according to EC-3 2, C.1.2.2.
def min_inertial_mom():
    a = data.input_data.get("a")/1000
    I = 226410 * a**4.4608
    return I

#function that creates deck stiffeners in the local coordinate system of the stiffener 
def create_deck_stiffener_local(b_sup, b_inf, h, t, t_deck):
    assert b_sup >= b_inf, "width out of bound or wrong way around"

    #assumption: b_sup is equal to distance between stiffeners
    #create points
    a = point.point(b_sup,0)
    b = point.point(-b_sup, 0)
    c = point.point(0.5*b_sup, 0)
    d = point.point(-0.5*b_sup, 0)
    e = point.point(-0.5*b_inf, h)
    f = point.point(0.5*b_inf, h)

    #create plates
    code_1 = plate_code.plate_code(1,0,0,0,0)
    line_1 = line.line(code_1, a, b, t_deck)
    code_2 = plate_code.plate_code(2,0,0,0,0)
    line_2 = line.line(code_2, d, e, t)
    code_3 = plate_code.plate_code(3,0,0,0,0)
    line_3 = line.line(code_3, e, f, t)
    code_4 = plate_code.plate_code(4,0,0,0,0)
    line_4 = line.line(code_4, f, c, t)

    deck_stiffener = crosssection.crosssection(b_sup, b_inf, h)
    #add the lines to itself
    deck_stiffener.addline(line_1)
    deck_stiffener.addline(line_2)
    deck_stiffener.addline(line_3)
    deck_stiffener.addline(line_4)

    return deck_stiffener
