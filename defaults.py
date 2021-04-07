import math

"""geometry defaults"""
cs_b_sup = 4000
cs_b_inf = 2000
cs_h = 1500




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
b_inf_minimal = 50
b_inf_step = 20
b_inf_maximal = 500
b_sup_minimal = 150
b_sup_step = 20
b_sup_maximal = 500
b_sup_minimal = 50
h_minimal = 100
h_step = 10
h_maximal = 500
t_range = [5,7,9,11,13,15,17,20]
max_angle = math.pi/12*5 #75 grad


"""buckling defaults"""
#convergence limit for m_rd_el in effective width iterations of local buckling
convergence_limit = 0.005
plate_length = 4000

"""do_modules"""
do_check_geometry = True
do_check_stiffeners_in_corners_top = True
do_check_stiffeners_in_corners_bottom = False
