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


def add_stiffener_set(initial_cs, proposition):
    iterations = 0
    geometry_ok = False

    while geometry_ok == False:
        iterations += 1
        stiffener_list = ss.substantiate(initial_cs, proposition)
        geometry_ok = check_geometry(initial_cs, stiffener_list, proposition)

        if iterations > 5:
            geometry_ok == True

    next_cs = merge(initial_cs, stiffener_list)
    return next_cs


#This functions merges a cross section and a list of stiffeners
"""we need initial_cs to always have the updated thickness of the trapezoid plates!!!!"""
def merge(initial_cs, stiffener_list):
    stiffeners2 = []
    stiffeners3 = []
    stiffeners4 = []
    for stiffener in stiffener_list:
        pos = stiffener.lines[0].code.pl_position
        if pos == 2:
            stiffeners2.append(stiffener)
        elif pos == 3:
            stiffeners3.append(stiffener)
        elif pos == 4:
            stiffeners4.append(stiffener)

    #side 2
    new_tpl_lines_2 = []
    if stiffeners_2 != []:
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
    own_angle = math.atan(height/half_width_diff)

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









    #this function should check weather the proposed stiffeners are feasable in the initial crosssection with the track_plate
    #as an argument it takes the initial crosssection and a list of all proposed stiffeners of type crosssection in the global coordinate system
    #as well as the stiffener_proposition list which then will be adjusted according to the geometry such that it might fit
def check_geometry(crosssection, stiffeners, stiffeners_proposition):


    geometry_ok = True


    """reorganize the stiffeners into own lists"""
    lines1 = []
    stiffeners1 = []
    stiffeners2 = []
    stiffeners3 = []
    stiffeners4 = []

    for line in crosssection.lines:
        if line.code.pl_position == 1 and line.code.tpl_number == 0:
            lines1.append(line)

    for i in range(int(len(lines1)/3)):
        stiffeners1[i] = crosssection.crosssection()
        for line in lines1:
            if line.code.st_number == i+1:
                stiffeners[i].append(line)


    for stiffener in stiffeners:
        if stiffener.lines[0].code.pl_position== 2:
            stiffeners2.append(stiffener)
        elif stiffener.lines[0].code.pl_position == 3:
            stiffeners3.append(stiffener)
        elif stiffener.lines[0].code.pl_position == 4:
            stiffeners4.append(stiffener)
        else:
            print("the lines of the stiffeners that were given to check_geometry do not contain codes")

    #sort the list of stiffeners according to st_number
    #this should be implemented right here in the input, because it is required by check_geometry

    """find for each side the most left and the most right one"""
    top_left = None
    top_right = None
    left_top = None
    right_top = None
    bottom_left = None
    bottom_right = None
    right_bottom = None
    left_bottom = None


    if stiffeners1 != []:
        min = random.choice(stiffeners1).code.st_number
        max = random.choice(stiffeners1).code.st_number
        for line in stiffeners1lines:
            if line.code.st_number <= min:
                top_left = line
                min = line.code.st_number
            if line.code.st_number >= max:
                top_right = line
                max = line.code.st_number

    if stiffeners2 != []:
        min = random.choice(stiffeners2).lines[0].code.st_number
        max = random.choice(stiffeners2).lines[0].code.st_number
        for stiffener in stiffeners2:
            if stiffener.lines[0].code.st_number <= min:
                right_top = stiffener
                min = stiffener.lines[0].code.st_number
            if stiffener.lines[0].code.st_number >= max:
                right_bottom = stiffener
                max = stiffener.lines[0].code.st_number

    if stiffeners3 != []:
        min = random.choice(stiffeners3).lines[0].code.st_number
        max = random.choice(stiffeners3).lines[0].code.st_number
        for stiffener in stiffeners2:
            if stiffener.lines[0].code.st_number <= min:
                bottom_right = stiffener
                min = stiffener.lines[0].code.st_number
            if stiffener.lines[0].code.st_number >= max:
                bottom_left = stiffener
                max = stiffener.lines[0].code.st_number

    if stiffeners4 != []:
        min = random.choice(stiffeners4).lines[0].code.st_number
        max = random.choice(stiffeners4).lines[0].code.st_number
        for stiffener in stiffeners4:
            if stiffener.lines[0].code.st_number <= min:
                left_bottom = stiffener
                min = stiffener.lines[0].code.st_number
            if stiffener.lines[0].code.st_number >= max:
                left_top = stiffener
            max = stiffener.lines[0].code.st_number

    #points from track plate stiffeners
    top_left_4a = None
    top_left_4b = None
    top_right_2a = None
    top_right_2b = None

    if top_left != None:
        top_left_4b = top_left.get_line(1,4).b
        top_left_4a = top_left.get_line(1,4).a
        st_num_top_left = top_left.get_line(1,4).code.st_number
    if top_right != None:
        top_right_2b = top_right.get_line(1,2).b
        top_right_2a = top_right.get_line(1,2).a
        st_num_top_right = top_right.get_line(1,2).code.st_number

    #points from right side stiffeners
    right_top_4a = None
    right_top_4b = None
    right_bottom_2a = None
    right_bottom_2b = None

    if right_top != None and right_bottom != None:
        right_top_4b = right_top.get_line(2,4).b
        right_top_4a = right_top.get_line(2,4).a
        st_num_right_top = right_top.get_line(2,4).code.st_number
        right_bottom_2b = right_bottom.get_line(2,2).b
        right_bottom_2a = right_bottom.get_line(2,2).a
        st_num_right_bottom = right_bottom.get_line(2,2).code.st_number

    #points from bottom side stiffeners
    bottom_right_4a = None
    bottom_right_4b = None
    bottom_left_2a = None
    bottom_left_2b = None

    if bottom_right != None and bottom_left != None:
        bottom_right_4b = bottom_right.get_line(3,4).b
        bottom_right_4a = bottom_right.get_line(3,4).a
        st_num_bottom_right = bottom_right.get_line(3,4).code.st_number
        bottom_left_2b = bottom_left.get_line(3,2).b
        bottom_left_2a = bottom_left.get_line(3,2).a
        st_num_bottom_left = bottom_left.get_line(3,2).code.st_number

    #points from left side stiffeners
    left_top_2a = None
    left_top_2b = None
    left_bottom_4a = None
    left_bottom_4b = None

    if left_top != None and left_bottom != None:
        left_bottom_4b = left_bottom.get_line(4,4).b
        left_bottom_4a = left_bottom.get_line(4,4).a
        st_num_left_bottom = left_bottom.get_line(4,4).code.st_number
        left_top_2b = left_top.get_line(4,2).b
        left_top_2a = left_top.get_line(4,2).a
        st_num_left_top = left_top.get_line(4,2).code.st_number


    #corners of the crosssection
    corner_top_right = None
    corner_top_left = None
    corner_bottom_right = None
    corner_bottom_left = None

    y_top_max = 0
    y_top_min = 0
    z_bottom_max = 0
    y_bottom_max = 0
    y_bottom_min = 0

    for plate in crosssection.lines:
        points = []
        points.append(plate.a)
        points.append(plate.b)
        for point in points:
            if point.y >= y_top_max and point.z == 0:
                y_top_max = point.y
                corner_top_left = point
                print("1")
            elif point.y <= y_top_min and point.z == 0:
                y_top_min = point.y
                corner_top_right = point
                print("2")
            elif point.y >= y_bottom_max and point.z >= z_bottom_max:
                y_bottom_max = point.y
                z_bottom_max = point.z
                corner_bottom_left = point
                print("4")
            elif point.y <= y_bottom_min and point.z >= z_bottom_max:
                y_bottom_min = point.y
                z_bottom_max = point.z
                corner_bottom_right = point
                print("3")

    """check distances to corners of crosssection"""
    mindis_top_corner = 30
    mindis_side_top_corner = 30
    mindis_side_bottom_corner = 30
    mindis_bottom_corner = 30

    if top_left != None:
        dis_top_left_corner = corner_top_left.y - top_left_4b.y
        if  dis < mindis_top_corner:
            print("track_plate stiffeners do not fit!!!")
            geometry_ok = False

    if top_right != None:
        dis_top_right_corner = corner_top_right.y - top_right_2a.y
        if dis_top_right_corner > mindis_top_corner:
            print("track_plate stiffeners do not fit!!!")
            geometry_ok = False

    if right_top != None and left_top != None:
        if right_top_4b.z < mindis_side_top_corner:
            corr = mindis_side_top_corner - right_top_4b.z
            stiffeners_proposition.get_proposed_stiffener(2, st_num_right_top).b_sup = right_top.b_sup - corr
            stiffeners_proposition.get_proposed_stiffener(2, st_num_right_top).b_inf = right_top.b_sup - corr
            stiffeners_proposition.get_proposed_stiffener(4, st_num_left_top).b_sup = left_top.b_sup - corr
            stiffeners_proposition.get_proposed_stiffener(4, st_num_left_top).b_inf = left_top.b_sup - corr
            geometry_ok = False

    if right_bottom != None and left_bottom != None:
        dis_right_bottom_corner = corner_bottom_right.z - right_bottom_2a.z
        if dis_right_bottom_corner < mindis_side_bottom_corner:
            corr = mindis_side_bottom_corner - dis_right_bottom_corner
            stiffeners_proposition.get_proposed_stiffener(2, st_num_right_bottom).b_sup = right_bottom.b_sup - corr
            stiffeners_proposition.get_proposed_stiffener(2, st_num_right_bottom).b_inf = right_bottom.b_inf - corr
            stiffeners_proposition.get_proposed_stiffener(4, st_num_left_bottom).b_sup = left_bottom.b_sup - corr
            stiffeners_proposition.get_proposed_stiffener(4, st_num_left_bottom).b_inf = left_bottom.b_inf - corr
            geometry_ok = False

    if bottom_left != None and bottom_right != None:
        dis_bottom_left_corner = corner_bottom_left.y - bottom_right_4b.y
        if corner_bottom_left.y - bottom_right_4b.y > mindis_bottom_corner:
            corr = mindis_bottom_corner - dis_bottom_left_corner
            stiffeners_proposition.get_proposed_stiffener(3, st_num_bottom_left).b_sup = bottom_left.b_sup -corr
            stiffeners_proposition.get_proposed_stiffener(3, st_num_bottom_left).b_inf = bottom_left.b_inf - corr
            stiffeners_proposition.get_proposed_stiffener(3, st_num_bottom_right).b_sup = bottom_right.b_sup - corr
            stiffeners_proposition.get_proposed_stiffener(3, st_num_bottom_right).b_inf = bottom_right.b_inf - corr
            geometry_ok = False


    """check distances between stiffeners"""
    #what is if stiffeners overlap?
    #Distances are only calculated in absolute values ...
    mindis_between = 30

    if right_top != None and right_bottom != None and right_top != right_bottom:
        st_number_min = right_top.lines[0].code.st_number
        st_number_max = right_bottom.lines[0].code.st_number
        for i in range(st_number_min, st_number_max, 1):
            upper = stiffeners2[i-st_number_min].get_stiffener_line(2,i,2).a
            lower = stiffeners2[i+1-st_number_min].get_stiffener_line(2,i+1,4).b
            distance = math.sqrt((abs(lower.y) - abs(upper.y))**2 + (abs(lower.z) - abs(upper.z))**2)
            print("Distance")
            print(distance)
            if distance < mindis_between:
                corr = (mindis_between-distance)/2
                print("Corr")
                print(corr)
                print("b_sup")
                print(stiffeners2[i-st_number_min].b_sup)
                stiffeners_proposition.get_proposed_stiffener(2,i).b_sup = stiffeners2[i-st_number_min].b_sup - corr
                print(stiffeners_proposition.get_proposed_stiffener(2,i).b_sup)
                stiffeners_proposition.get_proposed_stiffener(2,i+1).b_sup = stiffeners2[i+1-st_number_min].b_sup - corr
                stiffeners_proposition.get_proposed_stiffener(2,i).b_inf = stiffeners2[i-st_number_min].b_inf - corr
                stiffeners_proposition.get_proposed_stiffener(2,i+1).b_inf = stiffeners2[i+1-st_number_min].b_inf - corr
                geometry_ok = False

    #this part of the code still should be improved according to the other two parts
    #this will be done when the code for the sideplate works
    if bottom_right != None and bottom_left != None:
        st_number_min = bottom_right[0].code.st_number
        i = st_number_min
        st_number_max = bottom_left[0].code.st_number
        while i < st_number_max:
            right = stiffener3.get_stiffener_line(2,i,2).a
            left = stiffener3.get_stiffener_line(2,i+1,4).b
            distance = math.sqrt((abs(right.y) - abs(left.y))**2 + (abs(right.z) - abs(left.z))**2)
            if distance < mindis_between:
                corr = (mindis-distance)/2
                stiffeners_proposition.get_proposed_stiffener(3,i).b_sup -= corr
                stiffeners_proposition.get_proposed_stiffener(3,i+1).b_sup -= corr
                stiffeners_proposition.get_proposed_stiffener(3,i).b_inf -= corr
                stiffeners_proposition.get_proposed_stiffener(3,i+1).b_inf -= corr
                geometry_ok = False

    if left_top != None and left_bottom != None:
        st_number_min = left_bottom.lines[0].code.st_number
        st_number_max = left_top.lines[0].code.st_number
        for i in range(st_number_min, st_number_max, 1):
            lower = stiffeners4[i-st_number_min].get_stiffener_line(4,i,2).a
            upper = stiffeners4[i+1-st_number_min].get_stiffener_line(4,i+1,4).b
            distance = math.sqrt((abs(lower.y) - abs(upper.y))**2 + (abs(lower.z) - abs(upper.z))**2)
            if distance < mindis_between:
                corr = (mindis_between-distance)/2
                stiffeners_proposition.get_proposed_stiffener(4,i).b_sup = stiffeners4[i-st_number_min].b_sup - corr
                stiffeners_proposition.get_proposed_stiffener(4,i+1).b_sup = stiffeners4[i+1-st_number_min].b_sup - corr
                stiffeners_proposition.get_proposed_stiffener(4,i).b_inf = stiffeners4[i-st_number_min].b_inf - corr
                stiffeners_proposition.get_proposed_stiffener(4,i+1).b_inf = stiffeners4[i+1-st_number_min].b_inf - corr
                geometry_ok = False



    """check distances in corners between stiffeners"""
    if left_top != None and top_left != None:
        mindis = 30
        #the two edges are each defined by two lines
        #top corners (using symmetry, just doing left one)
        lines_left_top = []
        lines_left_top.append(left_top.get_line(4,2))
        lines_left_top.append(left_top.get_line(4,3))
        lines_top_left = []
        lines_top_left.append(top_left.get_line(1,4))
        lines_top_left.append(top_left.get_line(1,3))

        max_dis = 0
        angle = 0
        cut = False
        if dis_point_line(lines_top_left, lines_left_top) > max_dis:
            max_dis, angle = dis_lines_lines(lines_top_left, lines_left_top)
        elif dis_point_line(lines_left_top, lines_top_left) > max_dis:
            max_dis, angle = dis_lines_lines(points_left_top, lines_top_left)
        elif cut(lines_left_top, lines_top_left) == True:
            max_dis = (-1) * max_dis
            cut = True

        if max_dis < mindis:
            geometry_ok = False
            disdiff = mindis - max_dis

            corr_b_sup = 0
            corr_b_inf = 0
            corr_height = 0

            angle -= (math.pi/2 - left_top.get_line(4, 3),get_angle())
            corr_b_sup -= disdiff*math.cos(angle)
            corr_b_inf -= disdiff*math.cos(angle)
            corr_height -= disdiff*math.sin(angle)


            stiffeners_proposition.get_proposed_stiffener(4, st_num_left_top).b_sup -= corr_b_sup
            stiffeners_proposition.get_proposed_stiffener(4, st_num_left_top).b_inf -= corr_b_inf
            stiffeners_proposition.get_proposed_stiffener(4, st_num_left_top).height -= corr_height
            stiffeners_proposition.get_proposed_stiffener(2, st_num_right_top).b_sup -= corr_b_sup
            stiffeners_proposition.get_proposed_stiffener(2, st_num_right_top).b_inf -= corr_b_inf
            stiffeners_proposition.get_proposed_stiffener(2, st_num_right_top).height -= corr_height


    if left_bottom != None and bottom_left != None:
        mindis = 30
        #bottom (using symmetry, just doing left one)
        lines_left_bottom = []
        lines_left_bottom.append(left_bottom.get_line(4,3))
        lines_left_bottom.append(left_bottom.get_line(4,4))
        lines_top_left = []
        lines_bottom_left.append(bottom_left.get_line(3,1))
        lines_bottom_left.append(bottom_left.get_line(3,2))

        max_dis = 0
        cut = False
        if dis_point_line(lines_left_bottom, lines_bottom_left) > max_dis:
            max_dis, angle = dis_lines_lines(lines_left_bottom, lines_bottom_left)
        elif dis_point_line(lines_bottom_left, lines_left_bottom) > max_dis:
            max_dis, angle = dis_lines_lines(lines_bottom_left, lines_left_bottom)
        elif cut(lines_bottom_left, lines_left_bottom) == True:
            max_dis = (-1) * max_dis
            cut = True

        if max_dis < mindis:
            geometry_ok = False
            disdiff = mindis - max_dis

            corr_b_sup = 0
            corr_b_inf = 0
            corr_height = 0

            angle += (math.pi/2 - left_bottom.get_line(4,3).get_angle())
            corr_b_sup -= disdiff*math.cos(angle)
            corr_b_inf -= disdiff*math.cos(angle)
            corr_height -= disdiff*math.sin(angle)

            stiffeners_proposition.get_proposed_stiffener(4, st_num_left_top).b_sup -= corr_b_sup
            stiffeners_proposition.get_proposed_stiffener(4, st_num_left_top).b_inf -= corr_b_inf
            stiffeners_proposition.get_proposed_stiffener(4, st_num_left_top).height -= corr_height
            stiffeners_proposition.get_proposed_stiffener(2, st_num_right_top).b_sup -= corr_b_sup
            stiffeners_proposition.get_proposed_stiffener(2, st_num_right_top).b_inf -= corr_b_inf
            stiffeners_proposition.get_proposed_stiffener(2, st_num_right_top).height -= corr_height

    return geometry_ok












def cut(lines1, lines2):
    a11 = (lines1[0].a.y, lines1[0].a.z)
    b11 = (lines1[0].b.y, lines1[0].b.z)
    a12 = (lines1[1].a.y, lines1[1].a.z)
    b12 = (lines1[1].b.y, lines1[1].b.z)
    a21 = (lines2[0].a.y, lines2[0].a.z)
    b21 = (lines2[0].b.y, lines2[0].b.z)
    a22 = (lines2[1].a.y, lines2[1].a.z)
    b22 = (lines2[1].b.y, lines2[1].b.z)
    line11 = LineString([a11, b11])
    line12 = LineString([a12, b12])
    line21 = LineString([a21, b21])
    line22 = LineString([a22, b22])
    int1 = line11.intersection(line21)
    int2 = line11.intersection(line22)
    int3 = line12.intersection(line21)
    int4 = line12.intersection(line22)
    if int1 == None and int2 == None and int3 == None and int4 == None:
        return False
    else:
        return True





def dis_lines_lines(lines1, lines):
    #calculates the minimal width of a bar that fits between two corners created each by two lines
    points = []
    for line in lines1:
        points.append(line.a)
        points.append(line.b)

    dis = 1000
    angle = 0
    for line in lines:
        for point in points:
            #dot product
            l_y = line.b.y - line.a.y
            l_z = line.b.z - line.a.z
            norm = math.sqrt(l_y**2 + l_z**2)
            dis_new = abs(1/norm *(l_y * point.y + l_z * point.z))
            if dis_new < dis:
                dis = dis_new
                angle = math.atan(l_z / l_y)

    return dis, angle
