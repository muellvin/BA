import math
from data_and_defaults import data

#migrate to input data
"""defaults cost"""
welding_cost = 40 #[CHF/m]
steel_cost = 2 #[CHF/kg]

optimize_for_cost_only = False
optimize_for_spec_ei = False
optimize_for_ratio = True



"""check_geometry defaults"""
mindis_top_corner = 100
mindis_side_top_corner = 100
mindis_side_bottom_corner = 100
mindis_bottom_corner = 100
mindis_between = 100
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
convergence_limit_local_buckling = 0.02
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
do_shear_lag = True
do_global_plate_buckling = True
do_column_plate_buckling = True

do_print_to_pdf = True
do_print_to_txt = True
do_print_to_terminal = True

do_deck_as_prop = True
