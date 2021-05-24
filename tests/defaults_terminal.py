"""default cs"""
cs_b_sup = 4000
cs_t_deck = 5
cs_b_inf = 3000
cs_t_bottom = 5
cs_h = 1500
cs_t_side = 5
cs_a = 5000
cs_L_e = 10000
#cs_bending_type = "sagging bending"
cs_cs_position = "neither"
def set_cs_defaults():
    data.input_data.update({"b_sup": cs_b_sup})
    data.input_data.update({"t_deck": cs_t_deck})
    data.input_data.update({"b_inf": cs_b_inf})
    data.input_data.update({"t_bottom": cs_t_bottom})
    data.input_data.update({"h": cs_h})
    data.input_data.update({"t_side": cs_t_side})
    data.input_data.update({"a": cs_a})
    data.input_data.update({"L_e": cs_L_e})
    #data.input_data.update({"bending type": cs_bending_type})
    data.input_data.update({"cs position": cs_cs_position})


"""default crosssectional forces"""
cs_M_Ed = 10**2
cs_V_Ed = 100
cs_T_Ed = 0
def set_forces_defaults():
    data.input_data.update({"M_Ed": cs_M_Ed})
    data.input_data.update({"V_Ed": cs_V_Ed})
    data.input_data.update({"T_Ed": cs_T_Ed})


"""default stiffener"""
st_b_sup = 300
st_b_inf = 200
st_h = 200
st_t = 5
