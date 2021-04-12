#not really a class
#has methods for creating stiffeners of the type crosssection

import math
import shapely
import random
from classes import point
from classes import line
from classes import crosssection
from classes import plate_code
from shapely.geometry import LineString, Point
from classes import substantiate as ss
from output import geometry_output as go
import defaults
from output import geometry_output as go
from classes import check_geometry


def add_stiffener_set(initial_cs, proposition):
    iterations = 0
    geometry_ok = False

    while geometry_ok == False and iterations < 5:
        iterations += 1
        stiffener_list = ss.substantiate(initial_cs, proposition)
        geometry_ok = check_geometry.check_geometry(initial_cs, stiffener_list, proposition)
        #cs = merge(initial_cs, stiffener_list)
        #go.print_cs(cs)

    next_cs = merge(initial_cs, stiffener_list)
    return next_cs


#This functions merges a cross section and a list of stiffeners
"""we need initial_cs to always have the updated thickness of the trapezoid plates!!!!"""
def merge(initial_cs, stiffener_list):
    stiffeners1 = []
    stiffeners2 = []
    stiffeners3 = []
    stiffeners4 = []
    for stiffener in stiffener_list:
        pos = stiffener.lines[0].code.pl_position
        if pos == 1:
            stiffeners1.append(stiffener)
        elif pos == 2:
            stiffeners2.append(stiffener)
        elif pos == 3:
            stiffeners3.append(stiffener)
        elif pos == 4:
            stiffeners4.append(stiffener)

    #side 1
    new_tpl_lines_1 = []
    if stiffeners1 != []:
        assert True, "Is this case really needed?"
        old_plate_1 = initial_cs.get_pl_line(1)
        tpl_number_1_min = initial_cs.get_pl_line(1).code.tpl_number
        initial_cs.lines.remove(initial_cs.get_pl_line(1))
        t_1 = old_plate_1.t
        side = 1

        print(len(stiffeners1))
        print(stiffeners1[0].lines[0].code.st_number)
        st_number_1_min = stiffeners1[0].lines[0].code.st_number
        st_number_1_max = st_number_1_min
        for stiffener in stiffeners1:
            this_st_number = stiffener.lines[0].code.st_number
            if this_st_number < st_number_1_min:
                st_number_1_min = this_st_number
            elif this_st_number > st_number_1_max:
                st_number_1_max = this_st_number

        i = st_number_1_min
        j = tpl_number_1_min
        next_tpl_a = None

        while i <= st_number_1_max:
            new_plate_1_a = old_plate_1.a
            new_plate_1_b = stiffener.get_line(side, 4).b
            new_plate_2_a = new_plate_1_b
            new_plate_2_b = stiffener.get_line(side, 2).a
            next_tpl_a = new_plate_2_b
            code_1 = [side, 0, j, 0, 0]
            code_2 = [side, 0, j+1, 0, 0]
            new_plate_1 = line.line(code_1, new_plate_1_a, new_plate_1_b, t_1)
            new_plate_2 = line.line(code_2, new_plate_2_a, new_plate_2_b, t_1)
            new_tpl_lines_1.append(new_plate_1)
            new_tpl_lines_1.append(new_plate_2)
            j += 1
            i += 1
        code_3 = [side, 0, j+2, 0, 0]
        new_plate_3 = line.line(code_3, next_tpl_a, old_plate_1.b, t_1)
        new_tpl_lines_1.append(new_plate_3)

    #side 2
    new_tpl_lines_2 = []
    if stiffeners2 != []:
        old_plate_2 = initial_cs.get_pl_line(2)
        tpl_number_2_min = initial_cs.get_pl_line(2).code.tpl_number
        initial_cs.lines.remove(initial_cs.get_pl_line(2))
        t_2 = old_plate_2.t
        side = 2

        st_number_2_min = stiffeners2[0].lines[0].code.st_number
        st_number_2_max = st_number_2_min
        for stiffener in stiffeners2:
            this_st_number = stiffener.lines[0].code.st_number
            if this_st_number < st_number_2_min:
                st_number_2_min = this_st_number
            elif this_st_number > st_number_2_max:
                st_number_2_max = this_st_number

        i = st_number_2_min
        j = tpl_number_2_min
        next_tpl_a = None

        while i <= st_number_2_max:
            new_plate_1_a = old_plate_2.a
            new_plate_1_b = stiffener.get_line(side, 4).b
            new_plate_2_a = new_plate_1_b
            new_plate_2_b = stiffener.get_line(side, 2).a
            next_tpl_a = new_plate_2_b
            code_1 = plate_code.plate_code(side, 0, j, 0, 0)
            code_2 = plate_code.plate_code(side, 0, j+1, 0, 0)
            new_plate_1 = line.line(code_1, new_plate_1_a, new_plate_1_b, t_2)
            new_plate_2 = line.line(code_2, new_plate_2_a, new_plate_2_b, t_2)
            new_tpl_lines_2.append(new_plate_1)
            new_tpl_lines_2.append(new_plate_2)
            j += 1
            i += 1
        code_3 = plate_code.plate_code(side, 0, j+2, 0, 0)
        new_plate_3 = line.line(code_3, next_tpl_a, old_plate_2.b, t_2)
        new_tpl_lines_2.append(new_plate_3)


    #side 3
    new_tpl_lines_3 = []
    if stiffeners3 != []:
        old_plate_3 = initial_cs.get_pl_line(3)
        tpl_number_3_min = initial_cs.get_pl_line(3).code.tpl_number
        initial_cs.lines.remove(initial_cs.get_pl_line(3))
        t_3 = old_plate_3.t
        side = 3

        st_number_3_min = stiffeners3[0].lines[0].code.st_number
        st_number_3_max = st_number_3_min
        for stiffener in stiffeners3:
            this_st_number = stiffener.lines[0].code.st_number
            if this_st_number < st_number_3_min:
                st_number_3_min = this_st_number
            elif this_st_number > st_number_3_max:
                st_number_3_max = this_st_number

        i = st_number_3_min
        j = tpl_number_3_min
        next_tpl_a = None

        while i <= st_number_3_max:
            new_plate_1_a = old_plate_3.a
            new_plate_1_b = stiffener.get_line(side, 4).b
            new_plate_2_a = new_plate_1_b
            new_plate_2_b = stiffener.get_line(side, 2).a
            next_tpl_a = new_plate_2_b
            code_1 = plate_code.plate_code(side, 0, j, 0, 0)
            code_2 = plate_code.plate_code(side, 0, j+1, 0, 0)
            new_plate_1 = line.line(code_1, new_plate_1_a, new_plate_1_b, t_3)
            new_plate_2 = line.line(code_2, new_plate_2_a, new_plate_2_b, t_3)
            new_tpl_lines_3.append(new_plate_1)
            new_tpl_lines_3.append(new_plate_2)
            j += 1
            i += 1
        code_3 = plate_code.plate_code(side, 0, j+2, 0, 0)
        new_plate_3 = line.line(code_3, next_tpl_a, old_plate_3.b, t_2)
        new_tpl_lines_3.append(new_plate_3)


    #side 4
    new_tpl_lines_4 = []
    if stiffeners4 != []:
        old_plate_4 = initial_cs.get_pl_line(4)
        tpl_number_4_min = initial_cs.get_pl_line(4).code.tpl_number
        initial_cs.lines.remove(initial_cs.get_pl_line(4))
        t_4 = old_plate_4.t
        side = 4

        st_number_4_min = stiffeners4[0].lines[0].code.st_number
        st_number_4_max = st_number_4_min
        for stiffener in stiffeners4:
            this_st_number = stiffener.lines[0].code.st_number
            if this_st_number < st_number_4_min:
                st_number_4_min = this_st_number
            elif this_st_number > st_number_4_max:
                st_number_4_max = this_st_number

        i = st_number_4_min
        j = tpl_number_4_min
        next_tpl_a = None

        while i <= st_number_4_max:
            new_plate_1_a = old_plate_4.a
            new_plate_1_b = stiffener.get_line(side, 4).b
            new_plate_2_a = new_plate_1_b
            new_plate_2_b = stiffener.get_line(side, 2).a
            next_tpl_a = new_plate_2_b
            code_1 = plate_code.plate_code(side, 0, j, 0, 0)
            code_2 = plate_code.plate_code(side, 0, j+1, 0, 0)
            new_plate_1 = line.line(code_1, new_plate_1_a, new_plate_1_b, t_4)
            new_plate_2 = line.line(code_2, new_plate_2_a, new_plate_2_b, t_4)
            new_tpl_lines_4.append(new_plate_1)
            new_tpl_lines_4.append(new_plate_2)
            j += 1
            i += 1
        code_4 = plate_code.plate_code(side, 0, j+2, 0, 0)
        new_plate_4 = line.line(code_4, next_tpl_a, old_plate_4.b, t_2)
        new_tpl_lines_4.append(new_plate_4)

    for plate in new_tpl_lines_2:
        initial_cs.addline(plate)
    for plate in new_tpl_lines_3:
        initial_cs.addline(plate)
    for plate in new_tpl_lines_4:
        initial_cs.addline(plate)

    for stiffener in stiffener_list:
        for i in range(len(stiffener.lines)):
            initial_cs.addline(stiffener.lines[i])

    return initial_cs




#function creating a crosssection, which is the three lines of a stiffener at the place desired
def create_stiffener_global(pl_position, st_number, center_y, center_z, angle, width_top, width_bottom, height, t):
    y_corr = center_y - math.cos(angle)*width_top*0.5
    z_corr = center_z - math.sin(angle)*width_top*0.5
    assert width_top >= width_bottom, "width out of bound or wrong way around"
    half_width_diff = (width_top - width_bottom)/2
    length_side = math.sqrt(half_width_diff**2 + height**2)
    if half_width_diff > 0:
        own_angle = math.atan(height/half_width_diff)
    else:
        own_angle = math.pi/2

    #create plate 2
    a2 = point.point(y_corr,z_corr)
    b2 = point.point(y_corr + math.cos(own_angle+angle)*length_side, z_corr + math.sin(own_angle+angle)*length_side)
    code2 = plate_code.plate_code(pl_position, 1, 0, st_number, 2)
    line2 = line.line(code2, a2, b2, t)


    #create plate 3
    a3 = b2
    b3 = point.point(a3.y + math.cos(angle)*width_bottom, a3.z + math.sin(angle)*width_bottom)
    code3 = plate_code.plate_code(pl_position, 1, 0, st_number, 3)
    line3 = line.line(code3, a3, b3, t)

    #create plate 4
    a4 = b3
    b4 = point.point(y_corr + math.cos(angle)*width_top, z_corr + math.sin(angle)*width_top)
    code4 = plate_code.plate_code(pl_position, 1, 0, st_number, 4)
    line4 = line.line(code4, a4, b4, t)

    stiffener_global = crosssection.crosssection(width_top, width_bottom, height)
    #add the lines to itself
    stiffener_global.addline(line2)
    stiffener_global.addline(line3)
    stiffener_global.addline(line4)
    return stiffener_global

#function creating a crosssection, which is the three lines of a stiffener. it is in its own coordinate system -> for calculation of i_along
def create_stiffener_local(width_top, width_bottom, height, t):
    #assert width_top >= width_bottom, "width out of bound or wrong way around"
    half_width_diff = width_top - width_bottom
    length_side = math.sqrt(half_width_diff**2 + height**2)
    own_angle = math.atan(half_width_diff / height)

    #create plate 2
    a2 = point.point(-width_top/2,0)
    b2 = point.point(a2.y + math.sin(own_angle)*length_side, math.cos(own_angle)*length_side)
    code2 = plate_code.plate_code(0, 1, 0, 0, 2)
    line2 = line.line(code2, a2, b2, t)

    #create plate 3
    a3 = b2
    b3 = point.point(a3.y + width_bottom, a3.z)
    code3 = plate_code.plate_code(0, 1, 0, 0, 3)
    line3 = line.line(code3, a3, b3, t)

    #create plate 4
    a4 = b3
    b4 = point.point(width_top/2, 0)
    code4 = plate_code.plate_code(0, 1, 0, 0, 4)
    line4 = line.line(code4, a4, b4, t)

    stiffener_local = crosssection.crosssection(width_top, width_bottom, height)
    #add the lines to itself
    stiffener_local.addline(line2)
    stiffener_local.addline(line3)
    stiffener_local.addline(line4)
    return stiffener_local


def get_i_along_stiffener(width_top, width_bottom, height, t):
    stiffener_local = create_stiffener_local(width_top, width_bottom, height, t)
    i_along = stiffener_local.get_i_y_tot()
    return i_along

def get_area_stiffener(b_sup, b_inf, h, t):
    stiffener_local = create_stiffener_local(b_sup, b_inf, h, t)
    area = stiffener_local.get_area_tot()
    return area
