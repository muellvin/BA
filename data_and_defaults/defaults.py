import math
from data_and_defaults import data

""""deck defaults"""
t_deck = 14

"""optimization defaults"""
#do not add too many values, otherwise the calculation will take very long
t_range = [5,10,15]
I_range = [10**6, 10**7]
#do not set higher than 3
num_side_stiffeners_max = 2
#do not set higher than 7
num_bottom_stiffeners_max = 4


"""check_geometry defaults"""
mindis_top_corner = 100
mindis_side_top_corner = 100
mindis_side_bottom_corner = 100
mindis_bottom_corner = 100
mindis_between = 100
mindis_across_top = 500
mindis_across_bottom = 100
cutoffangle = math.pi/3


"""substantiate defaults"""
b_inf_maximal = 500
b_inf_minimal = 0
b_inf_step = 50
b_sup_maximal = 500
b_sup_minimal = 50
b_sup_step = 50
h_maximal = 300
h_minimal = 40
h_step = 20
t_range = [5,8,10,12,15,18]
max_angle = math.pi/12*5 #75 grad



"""buckling defaults"""
#effective width parameter
effective_width_parameter = 10
#eta should be changed if fy > 460 MPa
eta = 1.0

"""optimization_defaults"""


"""convergence defaults"""
#convergence limit for when width reduction due to shear lag is calculated plastically
convergence_limit_shear_lag = 0.05
#convergence limit for m_rd_el in effective width iterations of local buckling
convergence_limit_local_buckling = 0.02
#convergence limit for m_rd_pl_eff in interactions
convergence_limit_m_rd_pl_eff = 0.05

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
