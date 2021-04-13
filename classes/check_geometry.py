import defaults
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

    #this function should check weather the proposed stiffeners are feasable in the initial crosssection with the track_plate
    #as an argument it takes the initial crosssection and a list of all proposed stiffeners of type crosssection in the global coordinate system
    #as well as the stiffener_proposition list which then will be adjusted according to the geometry such that it might fit
def check_geometry(crosssection_cs, stiffeners, stiffeners_proposition):

    if defaults.do_check_geometry == False:
        return True

    geometry_ok = True


    """reorganize the stiffeners into own lists"""
    lines1 = []
    stiffeners1 = []
    stiffeners2 = []
    stiffeners3 = []
    stiffeners4 = []

    for line in crosssection_cs.lines:
        if line.code.pl_position == 1 and line.code.tpl_number == 0:
            lines1.append(line)

    for i in range(int(len(lines1)/3)):
        stiffeners1.append(crosssection.crosssection(0, 0, 0))
        for line in lines1:
            if line.code.st_number == i+1:
                stiffeners1[i].lines.append(line)
                lines1.remove(line)


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
        min = random.choice(stiffeners1).lines[0].code.st_number
        max = random.choice(stiffeners1).lines[0].code.st_number
        for stiffener in stiffeners1:
            if stiffener.lines[0].code.st_number <= min:
                top_left = stiffener
                min = stiffener.lines[0].code.st_number
            if stiffener.lines[0].code.st_number >= max:
                top_right = stiffener
                max = stiffener.lines[0].code.st_number

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
        for stiffener in stiffeners3:
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

    for plate in crosssection_cs.lines:
        points = []
        points.append(plate.a)
        points.append(plate.b)
        for point in points:
            if point.y >= y_top_max and point.z == 0:
                y_top_max = point.y
                corner_top_left = point
            elif point.y <= y_top_min and point.z == 0:
                y_top_min = point.y
                corner_top_right = point
            elif point.y >= y_bottom_max and point.z >= z_bottom_max:
                y_bottom_max = point.y
                z_bottom_max = point.z
                corner_bottom_left = point
            elif point.y <= y_bottom_min and point.z >= z_bottom_max:
                y_bottom_min = point.y
                z_bottom_max = point.z
                corner_bottom_right = point




    """check distances to corners of crosssection"""

    if right_bottom != None and left_bottom != None:
        dis_right_bottom_corner = corner_bottom_right.z - right_bottom_2a.z
        if dis_right_bottom_corner < defaults.mindis_side_bottom_corner:
            corr = defaults.mindis_side_bottom_corner - dis_right_bottom_corner
            stiffeners_proposition.get_proposed_stiffener(2, st_num_right_bottom).b_sup = right_bottom.b_sup - corr
            stiffeners_proposition.get_proposed_stiffener(4, st_num_left_bottom).b_sup = left_bottom.b_sup - corr
            stiffeners_proposition.get_proposed_stiffener(2, st_num_right_bottom).b_sup_corr = True
            stiffeners_proposition.get_proposed_stiffener(4, st_num_left_bottom).b_sup_corr = True
            stiffeners_proposition.get_proposed_stiffener(2, st_num_right_bottom).b_sup_corr_val = corr
            stiffeners_proposition.get_proposed_stiffener(4, st_num_left_bottom).b_sup_corr_val = corr
            print("side stiffeners too close to the bottom corners: ", dis_right_bottom_corner)
            geometry_ok = False

    if bottom_left != None and bottom_right != None:
        dis_bottom_left_corner = corner_bottom_left.y - bottom_left_2a.y
        if dis_bottom_left_corner < defaults.mindis_bottom_corner:
            corr = defaults.mindis_bottom_corner - dis_bottom_left_corner
            stiffeners_proposition.get_proposed_stiffener(3, st_num_bottom_left).b_sup = bottom_left.b_sup -corr
            stiffeners_proposition.get_proposed_stiffener(3, st_num_bottom_right).b_sup = bottom_right.b_sup - corr
            stiffeners_proposition.get_proposed_stiffener(3, st_num_bottom_left).b_sup_corr = True
            stiffeners_proposition.get_proposed_stiffener(3, st_num_bottom_right).b_sup_corr = True
            stiffeners_proposition.get_proposed_stiffener(3, st_num_bottom_left).b_sup_corr_val = corr
            stiffeners_proposition.get_proposed_stiffener(3, st_num_bottom_right).b_sup_corr_val = corr
            print("bottom stiffeners too close to the corners: ", dis_bottom_left_corner)
            geometry_ok = False






    """check distances between stiffeners"""

    if right_top != None and right_bottom != None and right_top != right_bottom:
        st_number_min = right_top.lines[0].code.st_number
        st_number_max = right_bottom.lines[0].code.st_number
        for i in range(st_number_min, st_number_max, 1):
            upper = stiffeners2[i-st_number_min].get_stiffener_line(2,i,2).a
            lower = stiffeners2[i+1-st_number_min].get_stiffener_line(2,i+1,4).b
            overlap = lower.z < upper.z
            distance = math.sqrt((abs(lower.y) - abs(upper.y))**2 + (abs(lower.z) - abs(upper.z))**2)
            corr = 0
            if overlap == True:
                corr = (defaults.mindis_between+distance)/2
            else:
                corr = (defaults.mindis_between-distance)/2
            #needs correction
            if distance < defaults.mindis_between:
                st_1 = stiffeners_proposition.get_proposed_stiffener(2,i)
                st_2 = stiffeners_proposition.get_proposed_stiffener(2,i+1)
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
                geometry_ok = False
                print("stiffeners on the right side are too close to each other ", end ='')
                if overlap == True:
                    print("with overlap: ", distance)
                else:
                    print("without overlap: ", distance)

    if left_top != None and left_bottom != None and left_top != left_bottom:
        st_number_min = left_bottom.lines[0].code.st_number
        st_number_max = left_top.lines[0].code.st_number
        for i in range(st_number_min, st_number_max, 1):
            lower = stiffeners4[i-st_number_min].get_stiffener_line(4,i,2).a
            upper = stiffeners4[i+1-st_number_min].get_stiffener_line(4,i+1,4).b
            overlap = upper.z > lower.z
            distance = math.sqrt((abs(lower.y) - abs(upper.y))**2 + (abs(lower.z) - abs(upper.z))**2)
            corr = 0
            if overlap == True:
                corr = (defaults.mindis_between+distance)/2
            else:
                corr = (defaults.mindis_between-distance)/2
            if distance < defaults.mindis_between:
                st_1 = stiffeners_proposition.get_proposed_stiffener(4,i)
                st_2 = stiffeners_proposition.get_proposed_stiffener(4,i+1)
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
                geometry_ok = False
                print("stiffeners on the left side are too close to each other ", end ='')
                if overlap == True:
                    print("with overlap: ", distance)
                else:
                    print("without overlap: ", distance)

    if bottom_right != None and bottom_left != None and bottom_left != bottom_right:
        st_number_min = bottom_right.lines[0].code.st_number
        st_number_max = bottom_left.lines[0].code.st_number
        for i in range(st_number_min, st_number_max, 1):
            right = stiffeners3[i-st_number_min].get_stiffener_line(3,i,2).a
            left = stiffeners3[i+1-st_number_min].get_stiffener_line(3,i+1,4).b
            y_shift = 100000
            overlap = right.y + y_shift > left.y + y_shift
            distance = abs((right.y + y_shift) - (left.y + y_shift))
            corr = 0
            if overlap == False:
                corr = (defaults.mindis_between-distance)/2
            elif overlap == True:
                corr = (defaults.mindis_between+distance)/2
            if distance < defaults.mindis_between:
                st_1 = stiffeners_proposition.get_proposed_stiffener(3,i)
                st_2 = stiffeners_proposition.get_proposed_stiffener(3,i+1)
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
                geometry_ok = False
                print("bottom stiffeners are too close to each other ", end = '')
                if overlap == True:
                    print("with overlap: ", distance)
                else:
                    print("without overlap: ", distance)




    #"Temporary Return statement for testing"
    #print("geometry_ok")
    #print(geometry_ok)


    """check distances in corners between stiffeners"""
    if defaults.do_check_stiffeners_in_corners_top == True and left_top != None and top_left != None:
        #the two edges are each defined by two lines
        #top corners (using symmetry, just doing left one)
        lines_left_top = []
        lines_left_top.append(left_top.get_line(4,2))
        lines_left_top.append(left_top.get_line(4,3))
        lines_top_left = []
        lines_top_left.append(top_left.get_line(1,4))
        lines_top_left.append(top_left.get_line(1,3))


        change_height = False
        change_b_inf = False
        cut = False
        corrections_needed = False
        #angle defining border III and IV
        cutoffangle = defaults.cutoffangle
        #angle between bottom plate of left top stiffener and the y axis
        stangle = float(left_top.get_line(4, 3).get_angle_y())
        #distance between the two croner points of the stiffeners
        dis = dis_lines_lines(lines_left_top, lines_top_left)[0]
        #angle of this distance to the y axis
        disangle = dis_lines_lines(lines_left_top, lines_top_left)[1]

        corr_b_inf = 0
        corr_height = 0
        situation = 0


        #situation I
        if top_left_4a.y > left_top_2a.y and top_left_4a.z > left_top_2a.z:
            situation = 1
            #angle between the dis and the stiffener bottom line of left top
            angle_between_st_dis = disangle - stangle
            disdiff = dis + defaults.mindis_across_top
            disdiff_norm = disdiff*math.cos(angle_between_st_dis)
            corr_height = disdiff_norm
            cut = True
            change_height = True
            corrections_needed = True
            geometry_ok = False
        #situation II (may be that bottom line of left top still cuts)
        elif left_top_2b.z < top_left_4a.z:
            situation = 2
            #angle between the dis and the stiffener bottom line of left top
            angle_between_st_dis = disangle - stangle
            disdiff = defaults.mindis_across_top - dis
            dis_norm = disdiff*math.cos(angle_between_st_dis)
            if 0 < dis_norm < defaults.mindis_across_top:
                corr_height = defaults.mindis_across_top - dis_norm
                change_height = True
                corrections_needed = True
                geometry_ok = False
        #situation III
        elif disangle < cutoffangle and left_top_2a.y > top_left_4a.y:
            situation = 3
            #angle between the dis and the stiffener bottom line of left top
            angle_between_st_dis = disangle + stangle
            disdiff = defaults.mindis_across_top - dis
            disdiff_norm = disdiff*math.cos(angle_between_st_dis)
            if 0 < disdiff_norm < defaults.mindis_across_top:
                corr_height = disdiff_norm
                change_height = True
                corrections_needed = True
                geometry_ok = False
        #situation IV
        elif left_top_2a.y > top_left_4a.y:
            situation = 4
            angle_between_st_dis = disangle + stangle
            disdiff = defaults.mindis_across_top - dis
            disdiff_parallel = disdiff*math.sin(angle_between_st_dis)
            if 0 < disdiff_parallel < default.mindis_across_top:
                corr_b_inf = disdiff_parallel
                change_b_inf = True
                corrections_needed = True
                geometry_ok = False
        #situation V
        else:
            situation = 5
            disdiff = defaults.mindis_across_top - dis
            angle_between_st_dis = disangle + stangle
            disdiff_norm = disdiff*math.cos(angle_between_st_dis)
            if 0 < disdiff_norm < defaults.mindis_across_top:
                corr_height = disdiff_norm
                change_height = True
                corrections_needed = True
                geometry_ok = False







        if corrections_needed == True:
            #temporal output
            angle_deg = disangle/(2*math.pi)*360
            print("situation: ",situation)
            print("top: disangle=",angle_deg)
            print("top: distance=",dis)

            print("Stiffeners in top corners are too close: ",math.floor(dis)," should be ",defaults.mindis_across_top," -> shorten by val: b_inf-=",math.floor(corr_b_inf)," height-=",math.floor(corr_height))

            st_left_top = stiffeners_proposition.get_proposed_stiffener(4, st_num_left_top)
            st_left_top_b_inf_corr_old = st_left_top.b_inf_corr_val
            st_left_top_h_corr_old = st_left_top.height_corr_val


            #heights are only adjusted in case of this problem (no check for previous corrections necessary)
            st_left_top.height = left_top.h - corr_height
            st_left_top.height_corr = True
            st_left_top.height_corr_val = corr_height


            if st_left_top_b_inf_corr_old == 0:
                st_left_top.b_inf = left_top.b_inf - corr_b_inf
                st_left_top.b_inf_corr = True
                st_left_top.b_inf_corr_val = corr_b_inf
            if st_left_top_b_inf_corr_old < corr_b_inf:
                st_left_top.b_inf += st_left_top_b_inf_corr_old  - corr_b_inf
                st_left_top.b_inf_corr = True
                st_left_top.b_inf_corr_val = corr_b_inf



            st_right_top = stiffeners_proposition.get_proposed_stiffener(2, st_num_right_top)
            st_right_top_b_inf_corr_old = st_right_top.b_inf_corr_val
            st_right_top_h_corr_old = st_right_top.height_corr_val


            #heights are only adjusted in case of this problem (no check for previous corrections necessary)
            st_right_top.height = right_top.h - corr_height
            st_right_top.height_corr = True
            st_right_top.height_corr_val = corr_height


            if st_right_top_b_inf_corr_old == 0:
                st_right_top.b_inf = right_top.b_inf - corr_b_inf
                st_right_top.b_inf_corr = True
                st_right_top.b_inf_corr_val = corr_b_inf
            if st_right_top_b_inf_corr_old < corr_b_inf:
                st_right_top.b_inf += st_right_top_b_inf_corr_old  - corr_b_inf
                st_right_top.b_inf_corr = True
                st_right_top.b_inf_corr_val = corr_b_inf






    if defaults.do_check_stiffeners_in_corners_bottom == True and left_bottom != None and bottom_left != None:

        #bottom (using symmetry, just doing left one)
        lines_left_bottom = []
        lines_left_bottom.append(left_bottom.get_line(4,3))
        lines_left_bottom.append(left_bottom.get_line(4,4))
        lines_bottom_left = []
        lines_bottom_left.append(bottom_left.get_line(3,2))
        lines_bottom_left.append(bottom_left.get_line(3,3))

        max_dis = 0
        disangle = 0
        cut = False

        if lines_left_bottom != [] and lines_bottom_left != []:
            if dis_lines_lines(lines_left_bottom, lines_bottom_left)[0] > max_dis:
                max_dis = dis_lines_lines(lines_left_bottom, lines_bottom_left)[0]
                disangle = dis_lines_lines(lines_left_bottom, lines_bottom_left)[1]
            elif dis_lines_lines(lines_bottom_left, lines_left_bottom)[0] > max_dis:
                max_dis = dis_lines_lines(lines_bottom_left, lines_left_bottom)[0]
                disangle = dis_lines_lines(lines_bottom_left, lines_left_bottom)[1]
            elif cut(lines_bottom_left, lines_left_bottom) == True:
                max_dis = (-1) * max_dis
                cut = True
        else:
            max_dis = 1000

        if max_dis < defaults.mindis_across_bottom:
            geometry_ok = False
            disdiff = defaults.mindis_across_bottom - max_dis

            stangle = (math.pi/2 - float(left_bottom.get_line(4,3).get_angle_y()))
            angle = disangle + stangle
            corr_b_inf = disdiff*math.cos(angle)/2
            corr_height = disdiff*math.sin(angle)/2

            print("Stiffeners in bottom corners are too close: ",math.floor(max_dis)," should be ",defaults.mindis_across_bottom," ---> shorten by val: b_inf-=",math.floor(corr_b_inf)," height-=",math.floor(corr_height))

            st_left_bottom = stiffeners_proposition.get_proposed_stiffener(4, st_num_left_bottom)
            st_bottom_left = stiffeners_proposition.get_proposed_stiffener(3, st_num_bottom_left)
            st_left_bottom_b_inf_corr_old = st_left_bottom.b_inf_corr_val
            st_bottom_left_b_inf_corr_old = st_bottom_left.b_inf_corr_val
            st_left_bottom_h_corr_old = st_left_bottom.height_corr_val
            st_bottom_left_h_corr_old = st_bottom_left.height_corr_val

            #heights are only adjusted in case of this problem
            st_left_bottom.height = left_bottom.h - corr_height
            st_left_bottom.height_corr = True
            st_left_bottom.height_corr_val = corr_height
            st_bottom_left.height = bottom_left.h - corr_height
            st_bottom_left.height_corr = True
            st_bottom_left.height_corr_val = corr_height

            if st_left_bottom_b_inf_corr_old == 0:
                st_left_bottom.b_inf = left_bottom.b_inf - corr_b_inf
                st_left_bottom.b_inf_corr = True
                st_left_bottom.b_inf_corr_val = corr_b_inf
            if st_left_bottom_b_inf_corr_old < corr_b_inf:
                st_left_bottom.b_inf += st_left_bottom_b_inf_corr_old  - corr_b_inf
                st_left_bottom.b_inf_corr = True
                st_left_bottom.b_inf_corr_val = corr_b_inf

            if st_bottom_left_b_inf_corr_old == 0:
                st_bottom_left.b_inf = bottom_left.b_inf - corr_b_inf
                st_bottom_left.b_inf_corr = True
                st_bottom_left.b_inf_corr_val = corr_b_inf
            if st_bottom_left_b_inf_corr_old < corr_b_inf:
                st_bottom_left.b_inf += st_bottom_left_b_inf_corr_old - corr_b_inf
                st_bottom_left.b_inf_corr = True
                st_bottom_left.b_inf_corr_val = corr_b_inf



            st_right_bottom = stiffeners_proposition.get_proposed_stiffener(2, st_num_right_bottom)
            st_bottom_right = stiffeners_proposition.get_proposed_stiffener(3, st_num_bottom_right)
            st_right_bottom_b_inf_corr_old = st_right_bottom.b_inf_corr_val
            st_bottom_right_b_inf_corr_old = st_bottom_right.b_inf_corr_val
            st_right_bottom_h_corr_old = st_right_bottom.height_corr_val
            st_bottom_right_h_corr_old = st_bottom_right.height_corr_val

            #heights are only adjusted in case of this problem
            st_right_bottom.height = right_bottom.h - corr_height
            st_right_bottom.height_corr = True
            st_right_bottom.height_corr_val = corr_height
            st_bottom_right.height = bottom_right.h - corr_height
            st_bottom_right.height_corr = True
            st_bottom_right.height_corr_val = corr_height

            if st_right_bottom_b_inf_corr_old == 0:
                st_right_bottom.b_inf = right_bottom.b_inf - corr_b_inf
                st_right_bottom.b_inf_corr = True
                st_right_bottom.b_inf_corr_val = corr_b_inf
            if st_right_bottom_b_inf_corr_old < corr_b_inf:
                st_right_bottom.b_inf += st_right_bottom_b_inf_corr_old  - corr_b_inf
                st_right_bottom.b_inf_corr = True
                st_right_bottom.b_inf_corr_val = corr_b_inf

            if st_bottom_right_b_inf_corr_old == 0:
                st_bottom_right.b_inf = bottom_right.b_inf - corr_b_inf
                st_bottom_right.b_inf_corr = True
                st_bottom_right.b_inf_corr_val = corr_b_inf
            if st_bottom_right_b_inf_corr_old < corr_b_inf:
                st_bottom_right.b_inf += st_bottom_right_b_inf_corr_old - corr_b_inf
                st_bottom_right.b_inf_corr = True
                st_bottom_right.b_inf_corr_val = corr_b_inf




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





def dis_lines_lines(lines1, lines2):
    #to find the corner of lines1
    points1 = []
    for lines in lines1:
        points1.append(lines.a)
        points1.append(lines.b)
    seen = set()
    corner1 = 0
    for x in points1:
        if x not in seen:
            seen.add(x)
        if x in seen:
            corner1 = x

    #to find the corner of lines2
    points2 = []
    for lines in lines2:
        points2.append(lines.a)
        points2.append(lines.b)
    seen = set()
    corner2 = 0
    for x in points2:
        if x not in seen:
            seen.add(x)
        if x in seen:
            corner2 = x

    help_line = line.line([0,0,0,0,0], corner1, corner2, 1)
    dis = help_line.get_length_tot()
    angle = help_line.get_angle_y()



    """
    smallest = 10000
    angle = 0
    for line in lines2:
        #calculates the minimal width of a bar that fits between two corners created each by two lines
        #list of points in lines1
        #lines2 stays a list of lines
        #unit vector of line from a to b (one is corner, but not important weather in plus or minus direction)
        l_y = line.b.y - line.a.y
        l_z = line.b.z - line.a.z
        length = math.sqrt(l_y**2 + l_z**2)
        #unit vector perpendicular to line
        l_y_norm = -l_y / length
        l_z_norm = -l_z / length

        for point in points1:
            #dot product
            #vector from corner to point
            d_y = point.y - corner.y
            d_z = point.z - corner.z
            dis_new = abs((l_y_norm * d_y + l_z_norm * d_z))

            if dis_new < smallest:
                dis = dis_new
                if d_y != 0:
                    angle = math.atan(d_z / d_y)
                    if angle < 0:
                        angle += math.pi
                    elif angle > math.pi / 2:
                        angle -= math.pi
                else:
                    angle = math.pi/2
                smallest = dis_new"""

    dis_angle = [dis, angle]
    return dis_angle
