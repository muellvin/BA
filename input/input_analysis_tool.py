#einfach ein skript
import data
import defaults
from classes import stiffeners_proposition
from classes import proposed_stiffener
from classes import stiffener


def set_defaults():
    pass

def set_cs_geometry():

    print("\nDefining the geometry of the cross-section")
    print("Do you want to use defaults? y/n: ", end='')
    string = str(input())
    if string == "y":
        defaults.set_cs_defaults()

    else:
        print('\nWidth of the top flange [mm] =', end = '')
        b_sup = float(input())
        data.input_data.update({"b_sup": b_sup})
        print('\nThickness of the top flange [mm] =', end = '')
        t_deck = float(input())
        data.input_data.update({"t_deck": t_deck})

        print('\nWidth of the bottom flange [mm] =', end = '')
        b_inf = float(input())
        data.input_data.update({"b_inf": b_inf})
        print('\nThickness of the bottom flange [mm] =', end = '')
        t_bottom = float(input())
        data.input_data.update({"t_bottom": t_bottom})
        print('\nValue of h? [mm] =', end = '')
        h = float(input())
        data.input_data.update({"h": h})
        print('\nThickness of sides? [mm] =', end = '')
        t_side = float(input())
        data.input_data.update({"t_side": t_side})
        print('\nDistance between transverse stiffeners? a [mm] =', end='')
        a = float(input())
        data.input_data.update({"a": a})
        print('\nEffective length of continuous beam? L_e [mm] =', end='')
        L_e = float(input())
        data.input_data.update({"L_e": L_e})
        print('\nWhat is the bending type? sagging bending / hogging bending: ', end='')
        bending_type = str(input())
        data.input_data.update({"bending type": bending_type})
        print('\nWhat is the position of the cross-section? end support / Cantilever / neither: ', end='')
        cs_position = str(input())
        data.input_data.update({"cs position": cs_position})


def set_stiffeners(number_st_top):
    stiffeners = stiffeners_proposition.stiffeners_proposition()
    print("\nHow many stiffeners an each side? =", end = '')
    number_side = int(input())
    print("\nHow many stiffeners an bottom side? =", end = '')
    number_bottom = int(input())

    #set the side ones
    st_list = stiffeners_proposition.stiffeners_proposition()
    i = 1
    while i <= number_side:
        if i == 1:
            if number_side ==1:
                print("\nSide Stiffener: ", end='')
            else:
                print("\nSide stiffeners from bottom to top", end='')
        print("\nstiffener ", str(i), end='')
        print("\nlocation [height ratio from bottom 0 to top 1] =", end='')
        location = float(input())
        print("\nDo you want to use defaults? y/n: ", end='')
        string = str(input())
        if string =="y":
            b_sup = defaults.st_b_sup
            b_inf = defaults.st_b_inf
            h = defaults.st_h
            t = defaults.st_t
        else:
            print("\nb_sup [mm] =", end= '')
            b_sup = float(input())
            print("\nb_inf [mm] =", end = '')
            b_inf = float(input())
            print("\nh [mm] =", end= '')
            h = float(input())
            print("\nt [mm] =", end= '')
            t = float(input())
        i_along = stiffener.get_i_along_stiffener(b_sup, b_inf, h, t)

        stiffener_right_i = proposed_stiffener.proposed_stiffener(2, int(number_st_top + number_side + 1 - i), location, \
        i_along, b_sup, b_inf, h, t)
        print(stiffener_right_i.st_number)
        st_list.add(stiffener_right_i)
        stiffener_left_i = proposed_stiffener.proposed_stiffener(4, int(number_st_top + number_side + number_bottom + i), location, \
        i_along, b_sup, b_inf, h, t)
        print(stiffener_left_i.st_number)
        st_list.add(stiffener_left_i)
        i+=1

    i = 1
    if number_bottom%2 ==1:
        iterations = int(number_bottom/2)+1
    else:
        iterations = number_bottom/2
    while i <= iterations:
        if i == 1:
            if iterations ==1:
                print("\nBottom stiffener: ",end='')
            else:
                print("\nBottom stiffeners from inside to the outside", end='')
        print("\nstiffener ", str(i), end='')
        if i == 1 and number_bottom%2 == 1:
            location = 0
        else:
            print("\nlocation [width ratio 0 middle 1 corner] =", end='')
            location = float(input())
        print("\nDo you want to use defaults? y/n: ", end='')
        string = str(input())
        if string =="y":
            b_sup = defaults.st_b_sup
            b_inf = defaults.st_b_inf
            h = defaults.st_h
            t = defaults.st_t
        else:
            print("\nb_sup [mm] =", end= '')
            b_sup = float(input())
            print("\nb_inf [mm] =", end = '')
            b_inf = float(input())
            print("\nh [mm] =", end= '')
            h = float(input())
            print("\nt [mm] =", end= '')
            t = float(input())
        i_along = stiffener.get_i_along_stiffener(b_sup, b_inf, h, t)


        if number_bottom%2 == 1 and i == 1:
            print("middle: ", iterations)
            stiffener_bottom_middle = proposed_stiffener.proposed_stiffener(3, int(number_st_top +number_side + iterations), location, \
            i_along, b_sup, b_inf, h, t)
            st_list.add(stiffener_bottom_middle)
        elif number_bottom%2 ==1 and i!= 1:
            print("right", iterations -int(number_bottom/2)-2 + i)
            stiffener_bottom_right_i = proposed_stiffener.proposed_stiffener(3, int(number_st_top + number_side + iterations -int(number_bottom/2)-2 + i), -location, \
            i_along, b_sup, b_inf, h, t)
            st_list.add(stiffener_bottom_right_i)
            print("left", iterations +int(number_bottom/2)+2 - i)
            stiffener_bottom_left_i = proposed_stiffener.proposed_stiffener(3, int(number_st_top + number_side + iterations +int(number_bottom/2)+2 - i), location, \
            i_along, b_sup, b_inf, h, t)
            st_list.add(stiffener_bottom_left_i)
        elif number_bottom%2 == 0:
            print("right", i)
            stiffener_bottom_right_i = proposed_stiffener.proposed_stiffener(3, int(number_st_top + number_side + i), -location, \
            i_along, b_sup, b_inf, h, t)
            st_list.add(stiffener_bottom_right_i)
            print("left",number_bottom+ 1-i)
            stiffener_bottom_left_i = proposed_stiffener.proposed_stiffener(3, int(number_st_top + number_side+ number_bottom + 1 - i), location, \
            i_along, b_sup, b_inf, h, t)
            st_list.add(stiffener_bottom_left_i)
        i+=1

    st_list.stiffeners = sorted(st_list.stiffeners, key = lambda st: st.st_number)
    for st in st_list.stiffeners:
        print(st.st_number)
    data.stiffener_data = st_list


def set_forces():
    print("\nDefining the cross-sectional forces: ",end='')
    print("\nDo you want to use default vaules? y/n :",end='')
    string = str(input())
    if string == "y":
        defaults.set_forces_defaults()
    else:
        print('Value of M_Ed? [kNm]')
        M_Ed= 10**6 * float(input())
        data.input_data.update({"M_Ed": M_Ed})
        print('Value of V_Ed? [kN]')
        V_Ed = 10**3 * float(input())
        data.input_data.update({"V_Ed": V_Ed})
        print('Value of T_Ed? [kNm]')
        T_Ed = 10**6 * float(input())
        data.input_data.update({"T_Ed": T_Ed})
