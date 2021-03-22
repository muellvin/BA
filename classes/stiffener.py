#not really a class
#has methods for creating stiffeners of the type crosssection

import math
import shapely
from shapely.geometry import LineString, Point


#function that will be called by the optimizer
def add_stiffeners(crosssection, stiffeners_proposition):
    #important for the creation of the stiffener is the position and the moment of inertia along the plate where it is placed
    #assumptions: symmetric distribution of stiffeners along z axis
    #pl_position, same as plate_code
    #location: between 0 and 1:
        #for top/ bottom it is the distance to the symmetry axis as a ratio to the max (width/2)
        #for the sides it is the ratio of z value to the height of the cross-section
    #i_along is the moment of inertia along the plate to which it is added
    """code der im file stiffener mit der Methode get_i_along_stiffener, viele ausprobiert und mittels geometrischen beschränkungen entscheidet welche"""
    pass



#function creating a crosssection, which is the three lines of a stiffener at the place desired
def create_stiffener_global(pl_position, st_number, center_y, center_z, angle, width_top, width_bottom, height, t):
    y_corr = center_y - math.cos(angle)*width_top
    z_corr = center_z - math.sin(angle)*width_top
    assert width_top >= width_bottom, "width out of bound or wrong way around"
    half_width_diff = width_top - width_bottom
    length_side = math.sqrt(half_width_diff**2 + height**2)
    own_angle = math.atan(half_width_diff / height)

    #create plate 2
    a2 = point.point(y_corr,z_corr)
    b2 = point.point(y_corr + math.sin(own_angle-angle)*length_side, z_corr + math.cos(own_angle-angle)*length_side)
    code2 = plate_code.code(pl_position, 1, 0, st_number, 2)
    line2 = line.line(code2, a2, b2, t)


    #create plate 3
    a3 = b2
    b3 = point.point(a3.y + math.cos(angle)*width_bottom, a3.z + math.sin(angle)*width_bottom)
    code3 = plate_code.code(pl_position, 1, 0, st_number, 3)
    line3 = line.line(code3, a3, b3, t)

    #create plate 4
    a4 = b3
    b4 = point.point(y_corr + math.cos(angle)*width_top, z_corr + math.sin(angle)*width_top)
    code4 = plate_code.code(pl_position, 1, 0, st_number, 4)
    line4 = line.line(code4, a4, b4, t)

    stiffener_global = crosssection.crosssection()
    #add the lines to itself
    stiffener_global.lines.addline(line2)
    stiffener_global.lines.addline(line3)
    stiffener_global.lines.addline(line4)
    return stiffener_global

#function creating a crosssection, which is the three lines of a stiffener. it is in its own coordinate system -> for calculation of i_along
def create_stiffener_local(width_top, width_bottom, height, t):
    assert width_top >= width_bottom, "width out of bound or wrong way around"
    half_width_diff = width_top - width_bottom
    length_side = math.sqrt(half_width_diff**2 + height**2)
    own_angle = math.atan(half_width_diff / height)

    #create plate 2
    a2 = point.point(-width_top/2,0)
    b2 = point.point(a2.y + math.sin(own_angle)*length_side, math.cos(own_angle)*length_side)
    code2 = plate_code.code(0, 1, 0, 0, 2)
    line2 = line.line(code2, a2, b2, t)

    #create plate 3
    a3 = b2
    b3 = point.point(a3.y + width_bottom, a3.z)
    code3 = plate_code.code(0, 1, 0, 0, 3)
    line3 = line.line(code3, a3, b3, t)

    #create plate 4
    a4 = b3
    b4 = point.point(width_top/2, 0)
    code4 = plate_code.code(0, 1, 0, 0, 4)
    line4 = line.line(code4, a4, b4, t)

    stiffener_local = crosssection.crosssection()
    #add the lines to itself
    stiffener_local.lines.addline(line2)
    stiffener_local.lines.addline(line3)
    stiffener_local.lines.addline(line4)
    return stiffener_local


def get_i_along_stiffener(width_top, width_bottom, height, t):
    stiffener_local = create_stiffener_local(width_top, width_bottom, height, t)
    i_along = stiffener_local.get_i_y_tot()
    return i_along

def get_area_stiffener(b_sup, b_inf, h, t):
    stiffener_local = create_stiffener_local(b_sup, b_inf, h, t)
    area = stiffener_local.get_area()
    return area








    #this function should check weather the proposed stiffeners are feasable in the initial crosssection with the track_plate
    #as an argument it takes the initial crosssection and a list of all proposed stiffeners of type crosssection in the global coordinate system
def check_geometry(crosssection, stiffeners, stiffeners_proposition):
    #reorganize the stiffeners into own lists
    stiffeners1lines = []
    stiffeners2 = []
    stiffeners3 = []
    stiffeners4 = []


    for line in crosssection:
        if line.pl_type == 1:
            stiffeners1lines.append(line)
    for stiffener in stiffeners:
        if stiffener[0].code.pl_number == 2:
            stiffeners2.append(stiffener)
        elif stiffener[0].code.pl_number == 3:
            stiffeners3.append(stiffener)
        elif stiffener[0].code.pl_number == 4:
            stiffeners4.append(stiffener)
        else
            print("the lines of the stiffeners that were given to check_geometry do not contain codes")


    #find for each side the most left and the most right one
    min = random.choice(stiffeners1lines).code.st_number
    max = random.choice(stiffeners1lines).code.st_number
    top_right = None
    top_left = None
    for line in stiffeners1lines:
        if line.code.st_number <= min:
            top_left = line
            min = line.code.st_number
        elif line.code.st_number >= max:
            top_right = line
            max = line.code.st_number
    min = random.choice(stiffeners2)[0].code.st_number
    max = random.choice(stiffeners2)[0].code.st_number
    right_top = None
    right_bottom = None
    for stiffener in stiffeners2:
        if stiffener[0].code.st_number <= min:
            right_top = stiffener
            min = stiffener[0].code.st_number
        elif stiffener[0].code.st_number >= max:
            right_bottom = stiffener
            max = stiffener[0].code.st_number
    min = random.choice(stiffeners3)[0].code.st_number
    max = random.choice(stiffeners3)[0].code.st_number
    bottom_left = None
    bottom_right = None
    for stiffener in stiffeners2:
        if stiffener[0].code.st_number <= min:
            bottom_right = stiffener
            min = stiffener[0].code.st_number
        elif stiffener[0].code.st_number >= max:
            bottom_left = stiffener
            max = stiffener[0].code.st_number
    min = random.choice(stiffeners4)[0].code.st_number
    max = random.choice(stiffeners4)[0].code.st_number
    left_top = None
    left_bottom = None
    for stiffener in stiffeners4:
        if stiffener[0].code.st_number <= min:
            left_bottom = stiffener
            min = stiffener[0].code.st_number
        elif stiffener[0].code.st_number >= max:
            left_top = stiffener
        max = stiffener[0].code.st_number

    #points from track plate stiffeners
    top_left_4b = top_left.get_line(1,4).b
    top_left_4a = top_left.get_line(1,4).a
    st_num_top_left = top_left.get_line(1,4).code.st_number
    top_right_2b = top_right.get_line(1,2).b
    top_right_2a = top_right.get_line(1,2).a
    st_num_top_right = top_right.get_line(1,2).code.st_number

    #points from right side stiffeners
    right_top_4b = right_top.get_line(2,4).b
    right_top_4a = right_top.get_line(2,4).a
    st_num_right_top = right_top.get_line(2,4).code.st_number
    right_bottom_2b = right_bottom.get_line(2,2).b
    right_bottom_2a = right_bottom.get_line(2,2).a
    st_num_right_bottom = right_bottom.get_line(2,2).code.st_number

    #points from bottom side stiffeners
    bottom_right_4b = bottom_right.get_line(3,4).b
    bottom_right_4a = bottom_right.get_line(3,4).a
    st_num_bottom_right = bottom_right.get_line(3,4).code.st_number
    bottom_left_2b = bottom_left.get_line(3,2).b
    bottom_left_2a = bottom_left.get_line(3,2).a
    st_num_bottom_left = bottom_left.get_line(3,2).code.st_number

    #points from left side stiffeners
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

    for plate in crosssection:
        for point in plate:
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




    #check distances to corners of crosssection
    mindis_top_corner = 30
    mindis_side_top_corner = 30
    mindis_side_bottom_corner = 30
    mindis_bottom_corner = 30

    dis_top_left_corner = corner_top_left.y - top_left_4b.y
    if  dis < mindis_top_corner:
        print("track_plate stiffeners do not fit!!!")

    dis_top_right_corner = corner_top_right.y - top_right_2a.y
    if dis_top_right_corner > mindis_top_corner:
        print("track_plate stiffeners do not fit!!!")

    if right_top_4b.z < mindis_side_top_corner.z:
        corr = mindis_side_top_corner.z - right_top_4b.z
        stiffeners_proposition.get_proposed_stiffener(2, st_num_right_top).b_sup -= corr
        stiffeners_proposition.get_proposed_stiffener(2, st_num_right_top).b_inf -= corr

    if left_top_2a.z < mindis_side_top_corner.z:
        corr = mindis_side_top_corner.z - left_top_2a.z
        stiffeners_proposition.get_proposed_stiffener(4, st_num_left_top).b_sup -= corr
        stiffeners_proposition.get_proposed_stiffener(4, st_num_left_top).b_inf -= corr

    dis_right_bottom_corner = corner_bottom_right.z - right_bottom_2a.z
    if dis_bottom_right_corner < mindis_side_bottom_corner:
        corr = mindis_side_bottom_corner - dis_bottom_right_corner
        stiffeners_proposition.get_proposed_stiffener(2, st_num_right_bottom).b_sup -= corr
        stiffeners_proposition.get_proposed_stiffener(2, st_num_right_bottom).b_inf -= corr

    dis_left_bottom_corner = corner_bottom_left.z - left_bottom_4b.z
    if  dis_bottom_left_corner < mindis_side_bottom_corner:
        corr = mindis_side_bottom_corner - dis_bottom_left_corner
        stiffeners_proposition.get_proposed_stiffener(4, st_num_left_bottom).b_sup -= corr
    stiffeners_proposition.get_proposed_stiffener(4, st_num_left_bottom).b_inf -= corr

    dis_bottom_left_corner = corner_bottom_left.y - bottom_right_4b.y
    if corner_bottom_left.y - bottom_right_4b.y > mindis_bottom_corner:
        corr = mindis_bottom_corner - dis_bottom_left_corner
        stiffeners_proposition.get_proposed_stiffener(3, st_num_bottom_left).b_sup -= corr
        stiffeners_proposition.get_proposed_stiffener(3, st_num_bottom_left).b_inf -= corr

    dis_bottom_right_corner = corner_bottom_right.y - bottom_left_2a.y
    if dis_bottom_right_corner < mindis_bottom_corner:
        corr = mindis_bottom_corner - dis_bottom_right_corner
        stiffeners_proposition.get_proposed_stiffener(3, st_num_bottom_right).b_sup -= corr
        stiffeners_proposition.get_proposed_stiffener(3, st_num_bottom_right).b_inf -= corr



    #check distances between stiffeners
    mindis_between = 30

    st_number_min = right_top[0].code.st_number
    i = st_number_min
    st_number_max = right_bottom[0].code.st_number
    while i < st_number_max:
        upper = stiffener2.get_stiffener_line(2,i,2).a
        lower = stiffener2.get_stiffener_line(2,i+1,4).b
        distance = math.sqrt((abs(lower.y) - abs(upper.y))**2 + (abs(lower.z) - abs(upper.z))**2)
        if distance < mindis_between:
            corr = (mindis-distance)/2
            stiffeners_proposition.get_proposed_stiffener(2,i).b_sup -= corr
            stiffeners_proposition.get_proposed_stiffener(2,i+1).b_sup -= corr
            stiffeners_proposition.get_proposed_stiffener(2,i).b_inf -= corr
            stiffeners_proposition.get_proposed_stiffener(2,i+1).b_inf -= corr

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

    st_number_min = left_bottom[0].code.st_number
    i = st_number_min
    st_number_max = left_top[0].code.st_number

    while i < st_number_max:
        lower = stiffener4.get_stiffener_line(2,i,2).a
        upper = stiffener4.get_stiffener_line(2,i+1,4).b
        distance = math.sqrt((abs(lower.y) - abs(upper.y))**2 + (abs(lower.z) - abs(upper.z))**2)
        if distance < mindis_between:
            corr = (mindis-distance)/2
            stiffeners_proposition.get_proposed_stiffener(4,i).b_sup -= corr
            stiffeners_proposition.get_proposed_stiffener(4,i+1).b_sup -= corr
            stiffeners_proposition.get_proposed_stiffener(4,i).b_inf -= corr
            stiffeners_proposition.get_proposed_stiffener(4,i+1).b_inf -= corr



        #check distances in corners between stiffeners
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
    cut = False
    if dis_point_line(lines_top_left, lines_left_top) > max_dis:
        max_dis = dis_point_line(lines_top_left, lines_left_top)
    elif dis_point_line(lines_left_top, lines_top_left) > max_dis:
        max_dis = dis_point_line(points_left_top, lines_top_left)
    elif cut(lines_left_top, lines_top_left) == True:
        max_dis = (-1) * max_dis
        cut = True

"""this code is not totally correct, dunno how well it will work"""
    if max_dis < mindis:
        disdiff = mindis - max_dis
        #angle defined by the two corners, only the fourth quadrant is negative (if 4a is to the bottom right of 2b)
        dy = left_top_2b.y - top_left_4a.y
        dz = left_top_2b.z - top_left_4a.z
        corr_b_sup = 0
        corr_b_inf = 0
        corr_height = 0
        if dy >= 0:
            angle = math.atan(dz/dy)
        elif dy < 0:
            angle = math.atan(dz/dy) + math.pi

        if (math.pi/4) < angle < math.pi/2:
            corr_b_sup -= disdiff / math.tan(angle)
            corr_b_inf -= disdiff / math.tan(angle)
        elif (-math.pi/2) < angle < math.pi/4:
            corr_height -= disdiff
        else:
            corr_b_sup -= disdiff
            corr_b_inf -= disdiff

        stiffeners_proposition.get_proposed_stiffener(4, st_num_left_top).b_sup -= corr_b_sup
        stiffeners_proposition.get_proposed_stiffener(4, st_num_left_top).b_inf -= corr_b_inf
        stiffeners_proposition.get_proposed_stiffener(4, st_num_left_top).height -= corr_height
        stiffeners_proposition.get_proposed_stiffener(2, st_num_right_top).b_sup -= corr_b_sup
        stiffeners_proposition.get_proposed_stiffener(2, st_num_right_top).b_inf -= corr_b_inf
        stiffeners_proposition.get_proposed_stiffener(2, st_num_right_top).height -= corr_height



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
        max_dis = dis_point_line(lines_left_bottom, lines_bottom_left)
    elif dis_point_line(lines_bottom_left, lines_left_bottom) > max_dis:
        max_dis = dis_point_line(lines_bottom_left, lines_left_bottom)
    elif cut(lines_bottom_left, lines_left_bottom) == True:
        max_dis = (-1) * max_dis
        cut = True

"""this code is not totally correct, dunno how well it will work"""
    if max_dis < mindis:
        disdiff = mindis - max_dis
        #angle defined by the two corners, only the fourth quadrant is negative (if 4a is to the bottom right of 2b)
        dy = left_bottom_4a.y - bottom_left_2b.y
        dz = bottom_left_2b.z - left_bottom_4a.z
        corr_b_sup = 0
        corr_b_inf = 0
        corr_height = 0
        if dy >= 0:
            angle = math.atan(dz/dy)
        elif dy < 0:
            angle = math.atan(dz/dy) + math.pi

        if (math.pi/4) < angle < math.pi/2:
            corr_b_sup -= disdiff / math.tan(angle)
            corr_b_inf -= disdiff / math.tan(angle)
        elif (-math.pi/2) < angle < math.pi/4:
            corr_height -= disdiff
        else:
            corr_b_sup -= disdiff
            corr_b_inf -= disdiff

        stiffeners_proposition.get_proposed_stiffener(4, st_num_left_top).b_sup -= corr_b_sup
        stiffeners_proposition.get_proposed_stiffener(4, st_num_left_top).b_inf -= corr_b_inf
        stiffeners_proposition.get_proposed_stiffener(4, st_num_left_top).height -= corr_height
        stiffeners_proposition.get_proposed_stiffener(2, st_num_right_top).b_sup -= corr_b_sup
        stiffeners_proposition.get_proposed_stiffener(2, st_num_right_top).b_inf -= corr_b_inf
        stiffeners_proposition.get_proposed_stiffener(2, st_num_right_top).height -= corr_height



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





def dis_point_line(lines1, lines):
    #calculates the minimal width of a bar that fits between two corners created each by two lines
    points = []
    for line in lines1:
        points.append(line.a)
        points.append(line.b)

    dis = 1000
    for line in lines:
        for point in points:
            #dot product
            l_y = line.b.y - line.a.y
            l_z = line.b.z - line.a.z
            norm = math.sqrt(l_y**2 + l_z**2)
            dis_new = abs(1/norm *(l_y * point.y + l_z * point.z))
            if dis_new < dis:
                dis = dis_new
    return dis
