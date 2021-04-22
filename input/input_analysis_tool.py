#einfach ein skript
import data
import defaults
from classes import stiffeners_proposition
from classes import proposed_stiffener
from classes import stiffener

def set_cs_geometry():
    print("Do you want to use defaults? y/n")
    string = str(input())
    if string == "y":
        data.input_data.update({"b_sup": defaults.cs_b_sup})
        data.input_data.update({"t_deck": defaults.cs_t_deck})
        data.input_data.update({"b_inf": defaults.cs_b_inf})
        data.input_data.update({"t_bottom": defaults.cs_t_bottom})
        data.input_data.update({"h": defaults.cs_h})
        data.input_data.update({"t_side": defaults.cs_t_side})
        data.input_data.update({"a": defaults.cs_a})
        data.input_data.update({"L_e": defaults.cs_L_e})
        data.input_data.update({"bending type": defaults.cs_bending_type})
        data.input_data.update({"cs position": defaults.cs_cs_position})

    else:
        print('Width of the top flange [mm] =', end = '')
        b_sup = float(input())
        data.input_data.update({"b_sup": b_sup})
        print('Thickness of the top flange [mm] =', end = '')
        t_deck = float(input())
        data.input_data.update({"t_deck": t_deck})

        print('\n Width of the bottom flange [mm] =', end = '')
        b_inf = float(input())
        data.input_data.update({"b_inf": b_inf})
        print('\n Thickness of the bottom flange [mm] =', end = '')
        t_bottom = float(input())
        data.input_data.update({"t_bottom": t_bottom})
        print('\n Value of h? [mm] =', end = '')
        h = float(input())
        data.input_data.update({"h": h})
        print('\n Thickness of sides? [mm] =', end = '')
        t_side = float(input())
        data.input_data.update({"t_side": t_side})

        print('\n Distance between transverse stiffeners? a [mm] =', end='')
        a = float(input())
        data.input_data.update({"a": a})
        print('\n Effective length of continuous beam? L_e [mm] =', end='')
        L_e = float(input())
        data.input_data.update({"L_e": L_e})
        print('\n What is the bending type? sagging bending / hogging bending: ', end='')
        bending_type = str(input())
        data.input_data.update({"bending type": bending_type})
        print('\n What is the position of the cross-section? end support / Cantilever / neither: ', end='')
        cs_position = str(input())
        data.input_data.update({"cs position": cs_position})


def set_stiffeners(number_st_top):
    stiffeners = stiffeners_proposition.stiffeners_proposition()
    print("\n How many stiffeners an each side? =", end = '')
    number_side = int(input())
    print("\n How many stiffeners an bottom side? =", end = '')
    number_bottom = int(input())

    #set the side ones
    st_list = []
    i = 1
    while i <= number_side:
        if i == 1:
            print("\n beginning with side stiffeners (trapezoid) from top to bottom")
        print("stiffener ", str(i))
        print("location [height ratio from bottom 0 to top 1] =", end='')
        location = float(input())
        print("Do you want to use defaults? y/n")
        string = str(input())
        if string =="y":
            b_sup = defaults.st_b_sup
            b_inf = defaults.st_b_inf
            h = defaults.st_h
            t = defaults.st_t
        else:
            print("\n b_sup [mm] =", end= '')
            b_sup = float(input())
            print("\n b_inf [mm] =", end = '')
            b_inf = float(input())
            print("\n h [mm] =", end= '')
            h = float(input())
            print("\n t [mm] =", end= '')
            t = float(input())
        i_along = stiffener.get_i_along_stiffener(b_sup, b_inf, h, t)

        stiffener_right_i = proposed_stiffener.proposed_stiffener(2, int(number_st_top + i), location, \
        i_along, b_sup, b_inf, t)
        st_list.append(stiffener_right_i)
        stiffener_left_i = proposed_stiffener.proposed_stiffener(4, int(number_st_top + number_side + number_bottom + i), location, \
        i_along, b_sup, b_inf, t)
        st_list.append(stiffener_left_i)
        i+=1

    i = 1
    if number_bottom%2 ==1:
        iterations = int(number_bottom/2)+1
    else:
        iterations = number_bottom/2
    while i <= iterations:
        if i == 1:
            print("\n now the stiffeners (trapezoid) on the bottom from inside to the outside")
        print("stiffener ", str(i))
        print("location [width ratio 0 middle 1 corner] =", end='')
        location = float(input())
        print("Do you want to use defaults? y/n")
        string = str(input())
        if string =="y":
            b_sup = defaults.st_b_sup
            b_inf = defaults.st_b_inf
            h = defaults.st_h
            t = defaults.st_t
        else:
            print("\n b_sup [mm] =", end= '')
            b_sup = float(input())
            print("\n b_inf [mm] =", end = '')
            b_inf = float(input())
            print("\n h [mm] =", end= '')
            h = float(input())
            print("\n t [mm] =", end= '')
            t = float(input())
        i_along = stiffener.get_i_along_stiffener(b_sup, b_inf, h, t)


        if number_bottom%2 == 1 and i == 1:
            stiffener_bottom_middle = proposed_stiffener.proposed_stiffener(3, int(number_st_top +number_side + iterations), location, \
            i_along, b_sup, b_inf, t)
            st_list.append(stiffener_bottom_middle)
        if number_bottom%2 ==1:
            stiffener_bottom_right_i = proposed_stiffener.proposed_stiffener(3, int(number_st_top + number_side + iterations + 1 - i), location, \
            i_along, b_sup, b_inf, t)
            st_list.append(stiffener_bottom_right_i)
            stiffener_bottom_left_i = proposed_stiffener.proposed_stiffener(3, int(number_st_top + number_side + iterations -1 + i), location, \
            i_along, b_sup, b_inf, t)
            st_list.append(stiffener_bottom_left_i)
        else:
            stiffener_bottom_right_i = proposed_stiffener.proposed_stiffener(3, int(number_st_top + number_side + iterations +1 - i), location, \
            i_along, b_sup, b_inf, t)
            st_list.append(stiffener_bottom_right_i)
            stiffener_bottom_left_i = proposed_stiffener.proposed_stiffener(3, int(number_st_top + number_side + iterations -1 + i), location, \
            i_along, b_sup, b_inf, t)
            st_list.append(stiffener_bottom_left_i)
        i+=1

    st_list = sorted(st_list, key = lambda st: st.st_number)
    data.stiffener_data = st_list


def set_forces():
    print('Value of M_Ed? [kNm]')
    M_Ed= 10**6 * float(input())
    data.input_data.update({"M_Ed": M_Ed})

    print('Value of V_Ed? [kN]')
    V_Ed = 10**3 * float(input())
    data.input_data.update({"V_Ed": V_Ed})

    print('Value of T_Ed? [kNm]')
    T_Ed = 10**6 * float(input())
    data.input_data.update({"T_Ed": T_Ed})
