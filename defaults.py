import math
import data

"""path defaults"""
sys_path = None
ebp_path = None


"""default cs"""
cs_b_sup = 4000
cs_t_deck = 5
cs_b_inf = 3000
cs_t_bottom = 5
cs_h = 1500
cs_t_side = 5
cs_a = 10000
cs_L_e = 15000
cs_bending_type = "sagging bending"
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
    data.input_data.update({"bending type": cs_bending_type})
    data.input_data.update({"cs position": cs_cs_position})


"""default crosssectional forces"""
cs_M_Ed = -10**8
cs_V_Ed = 100000
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


"""defaults cost"""
welding_cost = 40 #[CHF/m]
steel_cost = 1.5 #[CHF/kg]

optimize_for_cost_only = False
optimize_for_spec_ei = False

weight_cost = -1000
weight_ei = 1
# target value will be maximized
optimize_for_target_function = True


"""check_geometry defaults"""
mindis_top_corner = 100
mindis_side_top_corner = 100
mindis_side_bottom_corner = 100
mindis_bottom_corner = 100
mindis_between = 30
mindis_across_top = 500
mindis_across_bottom = 100
cutoffangle = math.pi/3


"""stiffener (substantiate) defaults"""
b_inf_minimal = 10
b_inf_step = 50
b_inf_maximal = 500
b_sup_minimal = 1
b_sup_step = 50
b_sup_maximal = 500
b_sup_minimal = 50
h_minimal = 1
h_step = 10
h_maximal = 300
t_range = [5,7,9,11,13,15,17,20]
max_angle = math.pi/12*5 #75 grad



"""buckling defaults"""
#convergence limit for m_rd_el in effective width iterations of local buckling
convergence_limit_local_buckling = 0.005
plate_length = 4000
effective_width_parameter = 10
#eta should be changed if fy > 460 MPa
eta = 1.0
#convergence limit for when width reduction due to shear lag is calculated plastically
convergence_limit_shear_lag = 0.05


"""do module defaults"""
#check_geometry
do_check_geometry = True
do_check_stiffeners_in_corners_top = False
do_check_stiffeners_in_corners_bottom = False
do_height_only = True
do_width_only = False

do_shear_lag_plastically = False
do_shear_lag = False
do_global_plate_buckling = False
do_column_plate_buckling = False

do_print = True
do_print_to_txt = True
do_print_to_terminal = True

do_deck_as_prop = True



do_deck_as_prop = True



def cs_defaults_tostring():
    line1 = "defaults for crosssection geometry: \n"
    line2 = "b_sup ="+str(cs_b_sup)+"\n"
    line3 = "b_inf ="+str(cs_b_inf)+"\n"
    line4 = "h ="+str(cs_h)+"\n"
    string = line1 + line2 + line3 + line4
    return string
def check_geometry_defaults_tostring():
    line1 = "geometry check defaults: tbd \n"
    return line1
def stiffener_defaults_tostring():
    line1 = "defaults for stiffener geometry: tbd \n"
    return line1
def buckling_defaults_tostring():
    line1 = "defaults for buckling proofs: tbd \n"
    return line1
def cs_analysis_tool_defaults_tostring():
    line1 = "defaults for the cross-section analysis tool: \n"
    line2 = "print text = "+str(do_print)+" to txt "+str(do_print_to_txt)+"\n"
