import math
from data_and_defaults import data
from data_and_defaults import defaults
from classes import stiffeners_proposition
from classes import proposed_stiffener
from assembly import add_stiffeners
from user_interface import form_values

#function that transforms stiffener input to proposed stiffeners
def input_to_prop(num_top, num_side, num_btm):
    cont = form_values.content
    st_list = stiffeners_proposition.stiffeners_proposition()
    side_st_data = []
    btm_st_data = []

    #side stiffeners
    for i in range(num_side):
        location = cont.get("location" + str(i+1))
        b_sup = cont.get("b_sup" + str(i+1))
        b_inf = cont.get("b_inf" + str(i+1))
        h = cont.get("h" + str(i+1))
        t = cont.get("t" + str(i+1))
        st_data = [location, b_sup, b_inf, h, t]
        side_st_data.append(st_data)

    side_st_data = sorted(side_st_data, key = lambda st: st[0])

    for i in range(num_side):
        location = side_st_data[i][0]
        b_sup = side_st_data[i][1]
        b_inf = side_st_data[i][2]
        h = side_st_data[i][3]
        t = side_st_data[i][4]
        i_along = add_stiffeners.get_i_along_stiffener(b_sup, b_inf, h, t)
        stiffener_right_i = proposed_stiffener.proposed_stiffener(2, int(num_top + num_side - i), location, \
        i_along, b_sup, b_inf, h, t)
        st_list.add(stiffener_right_i)
        stiffener_left_i = proposed_stiffener.proposed_stiffener(4, int(num_top + num_side + num_btm + i + 1), location, \
        i_along, b_sup, b_inf, h, t)
        st_list.add(stiffener_left_i)

    #bottom stiffeners
    middle_value = math.ceil(num_btm/2)
    for i in range(middle_value):
        location = cont.get("location" + str(i+31))
        b_sup = cont.get("b_sup" + str(i+31))
        b_inf = cont.get("b_inf" + str(i+31))
        h = cont.get("h" + str(i+31))
        t = cont.get("t" + str(i+31))
        st_data = [location, b_sup, b_inf, h, t]
        btm_st_data.append(st_data)

    btm_st_data = sorted(btm_st_data, key = lambda st: st[0])

    for i in range(middle_value):
        location = btm_st_data[i][0]
        b_sup = btm_st_data[i][1]
        b_inf = btm_st_data[i][2]
        h = btm_st_data[i][3]
        t = btm_st_data[i][4]
        i_along = add_stiffeners.get_i_along_stiffener(b_sup, b_inf, h, t)
        if num_btm%2 == 1 and i == 0:
            stiffener_bottom_middle = proposed_stiffener.proposed_stiffener(3, int(num_top +num_side + middle_value), location, \
            i_along, b_sup, b_inf, h, t)
            st_list.add(stiffener_bottom_middle)
        elif num_btm%2 ==1 and i!= 0:
            stiffener_bottom_right_i = proposed_stiffener.proposed_stiffener(3, int(num_top + num_side + middle_value - i), -location, \
            i_along, b_sup, b_inf, h, t)
            st_list.add(stiffener_bottom_right_i)
            stiffener_bottom_left_i = proposed_stiffener.proposed_stiffener(3, int(num_top + num_side + middle_value + i), location, \
            i_along, b_sup, b_inf, h, t)
            st_list.add(stiffener_bottom_left_i)
        elif num_btm%2 == 0:
            stiffener_bottom_right_i = proposed_stiffener.proposed_stiffener(3, int(num_top + num_side + num_btm/2-i), -location, \
            i_along, b_sup, b_inf, h, t)
            st_list.add(stiffener_bottom_right_i)
            stiffener_bottom_left_i = proposed_stiffener.proposed_stiffener(3, int(num_top + num_side + num_btm/2 + 1 + i), location, \
            i_along, b_sup, b_inf, h, t)
            st_list.add(stiffener_bottom_left_i)

    st_list.stiffeners = sorted(st_list.stiffeners, key = lambda st: st.st_number)
    data.stiffener_data = {}
    data.stiffener_data = st_list
    return

#function that makes stiffener propositions drawable
def prop_to_draw(cs):
    st_list_rest = []
    for st in data.stiffener_data.stiffeners:
        y,z = cs.get_coordinates(st.location, st.pl_position)
        if st.pl_position == 2:
            angle = math.pi + cs.get_angle(2)
        if st.pl_position == 3:
            angle = math.pi
        if st.pl_position == 4:
            angle = math.pi - cs.get_angle(2)
        stiffener_i = add_stiffeners.create_stiffener_global(st.pl_position, st.st_number, y, z, angle, \
        st.b_sup, st.b_inf, st.h, st.t)
        st_list_rest.append(stiffener_i)
    return st_list_rest
