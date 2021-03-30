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

mindis_across_top = 100
mindis_across_bottom = 100
cutoffangle = math.pi*2/3


"""stiffener (substantiate) defaults"""
b_inf_max_geo = 500
b_inf_minimal = 50
b_inf_step = 20
b_sup_max_geo = 500
b_sup_minimal = 100
b_sup_step = 20
b_sup_minimal = 50
h_max_geo = 200
h_min = 100
h_step = 10
t_range = [5,7,9,11,13,15,17,20]
max_angle = math.pi/12*5


"""do_modules"""
do_check_geometry = True
do_check_stiffeners_in_corners = True
