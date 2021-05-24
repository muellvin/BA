import math
import shapely
import random
import copy
from data_and_defaults import defaults
from classes import point
from classes import line
from classes import crosssection
from classes import plate_code


#cs ist empty (only 4 lines)
#stiffeners is a list of crosssections
#propositions is the only file that is changed and given back
def check_geometry(cs, stiffeners, propositions):
    geometry_ok = True
    propositions, ok1 = distances_to_corners(cs, stiffeners, propositions)
    propositions, ok2 = distances_betw_stiffeners(cs, stiffeners, propositions)
    geometry_ok = ( ok1 == ok2  == True )

    return propositions, geometry_ok




def distances_to_corners(cs, stiffeners, propositions):
    ok1 = True

    #get original values for minimal distances
    mindis_side_top_corner = 0
    mindis_side_bottom_corner = 0
    mindis_bottom_corner = 0

    top_right = get_top_right_stiffener(stiffeners)
    if top_right != None:
        mindis_side_top_corner = top_right.h/math.sin(cs.get_line(pl_position = 2).get_angle_y())

    right_top = get_right_top_stiffener(stiffeners)
    if right_top != None:
        right_top_4b = right_top.get_line(st_pl_position = 4).b
        right_top_4a = right_top.get_line(st_pl_position = 4).a
        st_num_right_top = right_top.get_line(st_pl_position = 4).code.st_number

    right_bottom = get_right_bottom_stiffener(stiffeners)
    if right_bottom != None:
        right_bottom_2b = right_bottom.get_line(st_pl_position = 2).b
        right_bottom_2a = right_bottom.get_line(st_pl_position = 2).a
        st_num_right_bottom = right_bottom.get_line(st_pl_position = 2).code.st_number
        mindis_bottom_corner = right_bottom.h/math.sin(cs.get_line(pl_position = 2).get_angle_y())

    bottom_right = get_bottom_right_stiffener(stiffeners)
    if bottom_right != None:
        bottom_right_4b = bottom_right.get_line(st_pl_position = 4).b
        bottom_right_4a = bottom_right.get_line(st_pl_position = 4).a
        st_num_bottom_right = bottom_right.get_line(st_pl_position = 4).code.st_number
        mindis_side_bottom_corner = bottom_right.h/math.sin(cs.get_line(pl_position = 2).get_angle_y())

    bottom_left = get_bottom_left_stiffener(stiffeners)
    if bottom_left != None:
        bottom_left_2b = bottom_left.get_line(st_pl_position = 2).b
        bottom_left_2a = bottom_left.get_line(st_pl_position = 2).a
        st_num_bottom_left = bottom_left.get_line(st_pl_position = 2).code.st_number

    left_bottom = get_left_bottom_stiffener(stiffeners)
    if left_bottom != None:
        left_bottom_4b = left_bottom.get_line(st_pl_position = 4).b
        left_bottom_4a = left_bottom.get_line(st_pl_position = 4).a
        st_num_left_bottom = left_bottom.get_line(st_pl_position = 4).code.st_number

    left_top = get_left_top_stiffener(stiffeners)
    if left_top != None:
        left_top_2b = left_top.get_line(st_pl_position = 2).b
        left_top_2a = left_top.get_line(st_pl_position = 2).a
        st_num_left_top = left_top.get_line(st_pl_position = 2).code.st_number



    corner_bottom_right = get_bottom_right_corner(cs)
    corner_top_right = get_top_right_corner(cs)

    if right_top != None:
        sign = 1
        if right_top_4b.z < corner_top_right.z:
            sign = -1
        dis_right_top_corner = sign*math.sqrt((corner_top_right.z - right_top_4b.z)**2 + (corner_top_right.y - right_top_4b.y)**2)
        if dis_right_top_corner < max(mindis_side_top_corner, defaults.mindis_side_top_corner):
            corr = max(mindis_side_top_corner, defaults.mindis_side_top_corner) - dis_right_top_corner
            propositions.get_proposed_stiffener(2, st_num_right_top).b_sup = right_top.b_sup - corr
            propositions.get_proposed_stiffener(4, st_num_left_top).b_sup = right_top.b_sup - corr
            propositions.get_proposed_stiffener(2, st_num_right_top).b_sup_corr = True
            propositions.get_proposed_stiffener(4, st_num_left_top).b_sup_corr = True
            propositions.get_proposed_stiffener(2, st_num_right_top).b_sup_corr_val = corr
            propositions.get_proposed_stiffener(4, st_num_left_top).b_sup_corr_val = corr
            print("side stiffeners too close to the top corners: ", dis_right_top_corner)
            ok1 = False

    if right_bottom != None:
        sign = 1
        if right_bottom_2a.z > corner_bottom_right.z:
            sign = -1
        dis_right_bottom_corner = sign*math.sqrt((corner_bottom_right.z - right_bottom_2a.z)**2 +(corner_bottom_right.y - right_bottom_2a.y)**2)
        if dis_right_bottom_corner < max(mindis_side_bottom_corner, defaults.mindis_side_bottom_corner):
            corr = max(mindis_side_bottom_corner, defaults.mindis_side_bottom_corner) - dis_right_bottom_corner
            propositions.get_proposed_stiffener(2, st_num_right_bottom).b_sup = right_bottom.b_sup - corr
            propositions.get_proposed_stiffener(4, st_num_left_bottom).b_sup = left_bottom.b_sup - corr
            propositions.get_proposed_stiffener(2, st_num_right_bottom).b_sup_corr = True
            propositions.get_proposed_stiffener(4, st_num_left_bottom).b_sup_corr = True
            propositions.get_proposed_stiffener(2, st_num_right_bottom).b_sup_corr_val = corr
            propositions.get_proposed_stiffener(4, st_num_left_bottom).b_sup_corr_val = corr
            print("side stiffeners too close to the bottom corners: ", dis_right_bottom_corner)
            ok1 = False

    #something about this part of the code is very strange ...
    if bottom_right != None:
        sign = 1
        if bottom_right_4b.y < corner_bottom_right.y:
            sign = -1
        dis_bottom_right_corner = sign*math.sqrt((corner_bottom_right.y - bottom_right_4b.y)**2 +(corner_bottom_right.z - bottom_right_4b.z)**2)
        if dis_bottom_right_corner < max(mindis_bottom_corner, defaults.mindis_bottom_corner):
            corr = max(mindis_bottom_corner, defaults.mindis_bottom_corner) - dis_bottom_right_corner
            propositions.get_proposed_stiffener(3, st_num_bottom_left).b_sup = bottom_left.b_sup -corr
            propositions.get_proposed_stiffener(3, st_num_bottom_right).b_sup = bottom_right.b_sup - corr
            propositions.get_proposed_stiffener(3, st_num_bottom_left).b_sup_corr = True
            propositions.get_proposed_stiffener(3, st_num_bottom_right).b_sup_corr = True
            propositions.get_proposed_stiffener(3, st_num_bottom_left).b_sup_corr_val = corr
            propositions.get_proposed_stiffener(3, st_num_bottom_right).b_sup_corr_val = corr
            print("bottom stiffeners too close to the corners: ", dis_bottom_right_corner)
            ok1 = False

    return propositions, ok1





def distances_betw_stiffeners(cs, stiffeners, propositions):
    ok2 = True

    stiffeners1 = []
    stiffeners2 = []
    stiffeners3 = []
    stiffeners4 = []
    for stiffener in stiffeners:
        if stiffener.lines[0].code.pl_position == 1:
            stiffeners1.append(stiffener)
        elif stiffener.lines[0].code.pl_position== 2:
            stiffeners2.append(stiffener)
        elif stiffener.lines[0].code.pl_position == 3:
            stiffeners3.append(stiffener)
        elif stiffener.lines[0].code.pl_position == 4:
            stiffeners4.append(stiffener)
        else:
            print("the lines of the stiffeners that were given to check_geometry do not contain codes")

    #sort the list of stiffeners according to st_number
    stiffeners1 = sorted(stiffeners1, key = lambda stiffener: stiffener.lines[0].code.st_number)
    stiffeners2 = sorted(stiffeners2, key = lambda stiffener: stiffener.lines[0].code.st_number)
    stiffeners3 = sorted(stiffeners3, key = lambda stiffener: stiffener.lines[0].code.st_number)
    stiffeners4 = sorted(stiffeners4, key = lambda stiffener: stiffener.lines[0].code.st_number)

    right_top = get_right_top_stiffener(stiffeners)
    if right_top != None:
        right_top_4b = right_top.get_line(st_pl_position = 4).b
        right_top_4a = right_top.get_line(st_pl_position = 4).a
        st_num_right_top = right_top.get_line(st_pl_position = 4).code.st_number

    right_bottom = get_right_bottom_stiffener(stiffeners)
    if right_bottom != None:
        right_bottom_2b = right_bottom.get_line(st_pl_position = 2).b
        right_bottom_2a = right_bottom.get_line(st_pl_position = 2).a
        st_num_right_bottom = right_bottom.get_line(st_pl_position = 2).code.st_number

    bottom_right = get_bottom_right_stiffener(stiffeners)
    if bottom_right != None:
        bottom_right_4b = bottom_right.get_line(st_pl_position = 4).b
        bottom_right_4a = bottom_right.get_line(st_pl_position = 4).a
        st_num_bottom_right = bottom_right.get_line(st_pl_position = 4).code.st_number

    bottom_left = get_bottom_left_stiffener(stiffeners)
    if bottom_left != None:
        bottom_left_2b = bottom_left.get_line(st_pl_position = 2).b
        bottom_left_2a = bottom_left.get_line(st_pl_position = 2).a
        st_num_bottom_left = bottom_left.get_line(st_pl_position = 2).code.st_number

    left_bottom = get_left_bottom_stiffener(stiffeners)
    if left_bottom != None:
        left_bottom_4b = left_bottom.get_line(st_pl_position = 4).b
        left_bottom_4a = left_bottom.get_line(st_pl_position = 4).a
        st_num_left_bottom = left_bottom.get_line(st_pl_position = 4).code.st_number

    left_top = get_left_top_stiffener(stiffeners)
    if left_top != None:
        left_top_2b = left_top.get_line(st_pl_position = 2).b
        left_top_2a = left_top.get_line(st_pl_position = 2).a
        st_num_left_top = left_top.get_line(st_pl_position = 2).code.st_number


    if right_top != None and right_bottom != None and right_top != right_bottom:
        st_number_min = right_top.lines[0].code.st_number
        st_number_max = right_bottom.lines[0].code.st_number
        for i in range(st_number_min, st_number_max, 1):
            upper = stiffeners2[i-st_number_min].get_line(pl_position = 2, st_number = i, st_pl_position = 2).a
            lower = stiffeners2[i+1-st_number_min].get_line(pl_position = 2,st_number = i+1,st_pl_position = 4).b
            overlap = lower.z < upper.z
            print(overlap)
            distance = math.sqrt((abs(lower.y) - abs(upper.y))**2 + (abs(lower.z) - abs(upper.z))**2)
            corr = 0
            if overlap == True:
                corr = (defaults.mindis_between+distance)/2
            else:
                corr = (defaults.mindis_between-distance)/2
            #needs correction
            if distance < defaults.mindis_between or overlap == True:
                st_1 = propositions.get_proposed_stiffener(2,i)
                st_2 = propositions.get_proposed_stiffener(2,i+1)
                corr_old_1 = st_1.b_sup_corr_val
                corr_old_2 = st_2.b_sup_corr_val
                #no change to the stiffener yet
                if corr_old_1 == 0:
                    st_1.b_sup = stiffeners2[i-st_number_min].b_sup - corr
                    st_1.b_sup_corr = True
                    st_1.b_sup_corr_val = corr
                #there has been a correction but not enough
                if corr_old_1 < corr:
                    st_1.b_sup += corr_old_1 - corr
                    st_1.b_sup_corr = True
                    st_1.b_sup_corr_val = corr
                if corr_old_2 == 0:
                    st_2.b_sup = stiffeners2[i+1-st_number_min].b_sup - corr
                    st_2.b_sup_corr = True
                    st_2.b_sup_corr_val = corr
                if corr_old_2 < corr:
                    st_2.b_sup += corr_old_2 - corr
                    st_2.b_sup_corr = True
                    st_2.b_sup_corr_val = corr
                ok2 = False
                print("stiffeners on the right side are too close to each other ", end ='')
                if overlap == True:
                    print("with overlap: ", distance)
                else:
                    print("without overlap: ", distance)

    if left_top != None and left_bottom != None and left_top != left_bottom:
        st_number_min = left_bottom.lines[0].code.st_number
        st_number_max = left_top.lines[0].code.st_number
        for i in range(st_number_min, st_number_max, 1):
            lower = stiffeners4[i-st_number_min].get_line(pl_position = 4, st_number = i, st_pl_position = 2).a
            upper = stiffeners4[i+1-st_number_min].get_line(pl_position = 4, st_number = i+1,st_pl_position = 4).b
            overlap = upper.z > lower.z
            distance = math.sqrt((abs(lower.y) - abs(upper.y))**2 + (abs(lower.z) - abs(upper.z))**2)
            corr = 0
            if overlap == True:
                corr = (defaults.mindis_between+distance)/2
            else:
                corr = (defaults.mindis_between-distance)/2
            if distance < defaults.mindis_between or overlap == True:
                st_1 = propositions.get_proposed_stiffener(4,i)
                st_2 = propositions.get_proposed_stiffener(4,i+1)
                corr_old_1 = st_1.b_sup_corr_val
                corr_old_2 = st_2.b_sup_corr_val
                if corr_old_1 == 0:
                    st_1.b_sup = stiffeners4[i-st_number_min].b_sup - corr
                    st_1.b_sup_corr = True
                    st_1.b_sup_corr_val = corr
                if corr_old_1 < corr:
                    st_1.b_sup += corr_old_1 - corr
                    st_1.b_sup_corr = True
                    st_1.b_sup_corr_val = corr
                if corr_old_2 == 0:
                    st_2.b_sup = stiffeners4[i+1-st_number_min].b_sup - corr
                    st_2.b_sup_corr = True
                    st_2.b_sup_corr_val = corr
                if corr_old_2 < corr:
                    st_2.b_sup += corr_old_2 - corr
                    st_2.b_sup_corr = True
                    st_2.b_sup_corr_val = corr
                ok2 = False
                print("stiffeners on the left side are too close to each other ", end ='')
                if overlap == True:
                    print("with overlap: ", distance)
                else:
                    print("without overlap: ", distance)

    if bottom_right != None and bottom_left != None and bottom_left != bottom_right:
        st_number_min = bottom_right.lines[0].code.st_number
        st_number_max = bottom_left.lines[0].code.st_number
        for i in range(st_number_min, st_number_max, 1):
            right = stiffeners3[i-st_number_min].get_line(pl_position = 3,st_number = i,st_pl_position = 2).a
            left = stiffeners3[i+1-st_number_min].get_line(pl_position = 3,st_number = i+1, st_pl_position = 4).b
            y_shift = 100000
            overlap = right.y + y_shift > left.y + y_shift
            distance = abs((right.y + y_shift) - (left.y + y_shift))
            corr = 0
            if overlap == False:
                corr = (defaults.mindis_between-distance)/2
            elif overlap == True:
                corr = (defaults.mindis_between+distance)/2
            if distance < defaults.mindis_between or overlap == True:
                st_1 = propositions.get_proposed_stiffener(3,i)
                st_2 = propositions.get_proposed_stiffener(3,i+1)
                corr_old_1 = st_1.b_sup_corr_val
                corr_old_2 = st_2.b_sup_corr_val
                if corr_old_1 == 0:
                    st_1.b_sup = stiffeners3[i-st_number_min].b_sup - corr
                    st_1.b_sup_corr = True
                    st_1.b_sup_corr_val = corr
                if corr_old_1 < corr:
                    st_1.b_sup += corr_old_1 - corr
                    st_1.b_sup_corr = True
                    st_1.b_sup_corr_val = corr
                if corr_old_2 == 0:
                    st_2.b_sup = stiffeners3[i+1-st_number_min].b_sup - corr
                    st_2.b_sup_corr = True
                    st_2.b_sup_corr_val = corr
                if corr_old_2 < corr:
                    st_2.b_sup += corr_old_2 - corr
                    st_2.b_sup_corr = True
                    st_2.b_sup_corr_val = corr
                ok2 = False
                print("bottom stiffeners are too close to each other ", end = '')
                if overlap == True:
                    print("with overlap: ", distance)
                else:
                    print("without overlap: ", distance)
    return propositions, ok2






def distances_betw_st_inc_top(cs, stiffeners, propositions, do_height):
    ok3 = True
    right_top = get_right_top_stiffener(stiffeners)
    top_right = get_top_right_stiffener(stiffeners)
    left_top = get_left_top_stiffener(stiffeners)



    if top_right != None and right_top != None:
        right_top_4b = right_top.get_line(st_pl_position = 4).b
        right_top_4a = right_top.get_line(st_pl_position = 4).a
        st_num_right_top = right_top.get_line(st_pl_position = 4).code.st_number
        top_right_2b = top_right.get_line(st_pl_position = 2).b
        st_num_top_right = top_right.get_line(st_pl_position = 2).code.st_number
        left_top_2b = left_top.get_line(st_pl_position = 2).b
        left_top_2a = left_top.get_line(st_pl_position = 2).a
        st_num_left_top = left_top.get_line(st_pl_position = 2).code.st_number



        st_left_top = propositions.get_proposed_stiffener(4, st_num_left_top)
        st_right_top = propositions.get_proposed_stiffener(2, st_num_right_top)

        #y z coordinate system with top_right_2a as origin
        #n t coordinate system showing normal and tangentially away from right_top (n normal)
        #   with right_top_4a as origin
        dis_line = line.line([0,0,0,0,0], top_right_2b, right_top_4a, 1)
        dis = dis_line.get_length_tot()
        dis_angle_y = dis_line.get_angle_y()
        dis_dy = dis_line.b.y - dis_line.a.y
        dis_dz = dis_line.b.z - dis_line.a.z

        #general check weather this might even be a problem
        if dis > 500 and right_top_4a.z > top_right_2b.z:
            return propositions, ok3

        st_angle_y = right_top.get_line(st_pl_position = 3).get_angle_y()
        #n: a line normal to the st bottom line points to positive y and negative z
        #parallel to height of stiffener right top
        n_dy = math.cos(st_angle_y)
        n_dz = - math.sin(st_angle_y)
        #t: a line tangential shows in the same direction as the stiffener
        #parallel to width
        t_dy = -math.sin(st_angle_y)
        t_dz = -math.cos(st_angle_y)


        #dis_line projected onto n t coordinate system
        dis_n = (n_dy * dis_dy) + (n_dz * dis_dz)
        dis_t = (t_dy * dis_dy) + (t_dy * dis_dy)

        if dis > defaults.mindis_across_top and dis_n > 0 and dis_t > 0:
            ok3 = True
        elif dis_n > defaults.mindis_across_top:
            ok3 = True
        elif dis_t > defaults.mindis_across_top:
            ok3 = True
        elif do_height == True:
            ok3 = False
        #if we get here, changes have to be made
            h_corr = defaults.mindis_across_top - dis_n
            st_left_top.h = left_top.h - h_corr
            st_left_top.h_corr = True
            st_left_top.h_corr_val = h_corr
            st_right_top.h = right_top.h - h_corr
            st_right_top.h_corr = True
            st_right_top.h_corr_val = h_corr
        elif do_height == False:
            ok3 = False
            """correction for width"""
            #has to be written: problem correction of b_inf -> maybe already b_sup

    return propositions, ok3






def get_top_right_corner(cs):
    points = []
    for plate in cs.lines:
        points.append(copy.deepcopy(plate.a))
        points.append(copy.deepcopy(plate.b))
    y_top_min = 0
    for point in points:
        if point.y <= y_top_min and point.z == 0:
            y_top_min = point.y
            top_right_corner = point
    return top_right_corner

def get_bottom_right_corner(cs):
    return cs.get_line(pl_position = 3).a
    #points = []
    #for plate in cs.lines:
    #    points.append(copy.deepcopy(plate.a))
    #    points.append(copy.deepcopy(plate.b))
    #y_bottom_min = 0
    #z_bottom_max = 0
    #for point in points:
    #    if point.y <= y_bottom_min and point.z >= z_bottom_max:
    #        y_bottom_min = point.y
    #        z_bottom_max = point.z
    #        bottom_right_corner = point
    #return bottom_right_corner




def get_top_stiffeners(stiffeners):
    top_stiffeners = []
    for stiffener in stiffeners:
        if stiffener.lines[0].code.pl_position == 1:
            top_stiffeners.append(stiffener)
    return top_stiffeners

def get_right_stiffeners(stiffeners):
    right_stiffeners = []
    for stiffener in stiffeners:
        if stiffener.lines[0].code.pl_position == 2:
            right_stiffeners.append(stiffener)
    return right_stiffeners

def get_bottom_stiffeners(stiffeners):
    bottom_stiffeners = []
    for stiffener in stiffeners:
        if stiffener.lines[0].code.pl_position == 3:
            bottom_stiffeners.append(stiffener)
    return bottom_stiffeners

def get_left_stiffeners(stiffeners):
    left_stiffeners = []
    for stiffener in stiffeners:
        if stiffener.lines[0].code.pl_position == 4:
            left_stiffeners.append(stiffener)
    return left_stiffeners


def get_top_left_stiffener(stiffeners):
    top_stiffeners = get_top_stiffeners(stiffeners)
    if top_stiffeners == []:
        return None
    top_left = top_stiffeners[0]
    for top_stiffener in top_stiffeners:
        if top_stiffener.lines[0].code.st_number < top_left.lines[0].code.st_number:
            top_left = top_stiffener
    return top_left

def get_top_right_stiffener(stiffeners):
    top_stiffeners = get_top_stiffeners(stiffeners)
    if top_stiffeners == []:
        return None
    top_right = top_stiffeners[0]
    for top_stiffener in top_stiffeners:
        if top_stiffener.lines[0].code.st_number > top_right.lines[0].code.st_number:
            top_right = top_stiffener
    return top_right

def get_right_top_stiffener(stiffeners):
    right_stiffeners = get_right_stiffeners(stiffeners)
    if right_stiffeners == []:
        return None
    right_top = right_stiffeners[0]
    for right_stiffener in right_stiffeners:
        if right_stiffener.lines[0].code.st_number < right_top.lines[0].code.st_number:
            right_top = right_stiffener
    return right_top
def get_right_bottom_stiffener(stiffeners):
    right_stiffeners = get_right_stiffeners(stiffeners)
    if right_stiffeners == []:
        return None
    right_bottom = right_stiffeners[0]
    for right_stiffener in right_stiffeners:
        if right_stiffener.lines[0].code.st_number > right_bottom.lines[0].code.st_number:
            right_bottom = right_stiffener
    return right_bottom

def get_bottom_right_stiffener(stiffeners):
    bottom_stiffeners = get_bottom_stiffeners(stiffeners)
    if bottom_stiffeners == []:
        return None
    bottom_right = bottom_stiffeners[0]
    for bottom_stiffener in bottom_stiffeners:
        if bottom_stiffener.lines[0].code.st_number < bottom_right.lines[0].code.st_number:
            bottom_right = bottom_stiffener
    return bottom_right

def get_bottom_left_stiffener(stiffeners):
    bottom_stiffeners = get_bottom_stiffeners(stiffeners)
    if bottom_stiffeners == []:
        return None
    bottom_left = bottom_stiffeners[0]
    for bottom_stiffener in bottom_stiffeners:
        if bottom_stiffener.lines[0].code.st_number > bottom_left.lines[0].code.st_number:
            bottom_left = bottom_stiffener
    return bottom_left

def get_left_bottom_stiffener(stiffeners):
    left_stiffeners = get_left_stiffeners(stiffeners)
    if left_stiffeners == []:
        return None
    left_bottom = left_stiffeners[0]
    for left_stiffener in left_stiffeners:
        if left_stiffener.lines[0].code.st_number < left_bottom.lines[0].code.st_number:
            left_bottom = left_stiffener
    return left_bottom
def get_left_top_stiffener(stiffeners):
    left_stiffeners = get_left_stiffeners(stiffeners)
    if left_stiffeners == []:
        return None
    left_top = left_stiffeners[0]
    for left_stiffener in left_stiffeners:
        if left_stiffener.lines[0].code.st_number > left_top.lines[0].code.st_number:
            left_top = left_stiffener
    return left_top
