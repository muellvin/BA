from classes import point as pt
from classes import line as ln
from classes import crosssection as cs
from classes import stiffener as st
from classes import plate_code as plcd
import math
import data


def deck(b_deck):
    #returns the a list of optimal deck stiffeners
    min_Iy = min_inertial_mom()
    #choose correct value according to EC 3-2
    t_deck = 14
    data.input_data.update({"t_deck": t_deck})
    #set maximum default values and step size for range
    h_max = 300
    h_step = 5
    #must be >6mm according to EC 3-2
    t_range = [7,9,11,13,15,17,20]

    #b_sup, b_inf, h, t, mass
    best = [0,0,0,0,10**8]

    #iterate through all the possible solutions, in order to find viable ones
    for t in t_range:
        b_sup_theor = min(25*t, 300)
        print(b_sup_theor)
        num_of_plates = math.ceil(b_deck / b_sup_theor)
        if num_of_plates % 2 == 0:
            num_of_plates += 1
        assert num_of_plates % 2 == 1, "You are stupid!"
        num_of_stiffeners = (num_of_plates-1)/2
        b_sup = b_deck / num_of_plates

        #assume the stiffener angle to be pi/3
        for h in range(30, h_max, h_step):
            b_inf = b_sup - 2*h / math.tan(math.pi/3)
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
    print(b_sup, b_inf, h, t)
    #create a list of deck stiffeners
    deck_stiffener_list = []
    num_of_plates = round(b_deck / b_sup)
    num_of_stiffeners = (num_of_plates-1)/2
    print(num_of_stiffeners)
    for i in range(int(num_of_stiffeners)):
        center_y = (0.5*b_deck - (2*i+1.5)*b_sup)
        print(center_y)
        stiffener = st.create_stiffener_global(1, i+1, center_y, 0, 0, b_sup, b_inf, h, t)
        deck_stiffener_list.append(stiffener)

    return deck_stiffener_list


def min_inertial_mom():
    #returns the minimal required inertial moment of the track plate according to EC-3 2
    #This inertial momenent is calculated with the track plate
    """Lower Inertial moments for stiffeners in the corners should be considered"""
    #Minimal value of track plate thickness should be considered somewhere
    a = 3.5
    I = 226410 * a**4.4608
    return I

def create_deck_stiffener_local(b_sup, b_inf, h, t, t_deck):
    assert b_sup >= b_inf, "width out of bound or wrong way around"

    #assumption: b_sup is equal to distance between stiffeners
    #create points
    a = pt.point(b_sup,0)
    b = pt.point(-b_sup, 0)
    c = pt.point(0.5*b_sup, 0)
    d = pt.point(-0.5*b_sup, 0)
    e = pt.point(-0.5*b_inf, h)
    f = pt.point(0.5*b_inf, h)

    #create plates
    code_1 = plcd.plate_code(1,0,0,0,0)
    line_1 = ln.line(code_1, a, b, t_deck)
    code_2 = plcd.plate_code(2,0,0,0,0)
    line_2 = ln.line(code_2, d, e, t)
    code_3 = plcd.plate_code(3,0,0,0,0)
    line_3 = ln.line(code_3, e, f, t)
    code_4 = plcd.plate_code(4,0,0,0,0)
    line_4 = ln.line(code_4, f, c, t)

    deck_stiffener = cs.crosssection(b_sup, b_inf, h)
    #add the lines to itself
    deck_stiffener.addline(line_1)
    deck_stiffener.addline(line_2)
    deck_stiffener.addline(line_3)
    deck_stiffener.addline(line_4)

    return deck_stiffener
