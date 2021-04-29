import defaults
import math
import shapely
import random
from classes import point
from classes import line
from classes import crosssection
from classes import plate_code
from shapely.geometry import LineString, Point
from classes import substantiate
from output import geometry_output
import defaults
from output import geometry_output




#cs ist empty (only 4 lines), stiffeners has all the
def check_geometry(cs, stiffeners, propositions):
    if defaults.do_height_only == True and defaults.do_width_only == True:
        conflict = True
        assert conflict == True, "cannot do only height and only width"

    if defaults.do_width_only == True:
        propositions = distances_to_corners(cs, stiffeners, propositions)
        propositions = distances_betw_stiffeners(cs, stiffeners, propositions)
        propositions = distances_stiffeners_to_corners(cs, stiffeners, propositions)

    #only check that has to be done in both do defaults
    propositions = distances_betw_stiffeners_in_corners(cs, stiffeners, propositions)

    return propositions




def distances_to_corners(cs, stiffeners, propositions)
    right_bottom = get_right_bottom_stiffener(stiffeners)
    right_bottom_2a = right_bottom.get_line(st_pl_position = 2).a
    right_top = get_right_top_stiffener(stiffeners)
    corner_bottom_right = get_bottom_right_corner(cs)
    corner_top_right = get_top_right_corner(cs)

    if right_bottom != None:
        dis_right_bottom_corner = corner_bottom_right.z - right_bottom_2a.z
        if dis_right_bottom_corner < defaults.mindis_side_bottom_corner:
            corr = defaults.mindis_side_bottom_corner - dis_right_bottom_corner
            propositions.get_proposed_stiffener(2, st_num_right_bottom).b_sup = right_bottom.b_sup - corr
            propositions.get_proposed_stiffener(4, st_num_left_bottom).b_sup = left_bottom.b_sup - corr
            propositions.get_proposed_stiffener(2, st_num_right_bottom).b_sup_corr = True
            propositions.get_proposed_stiffener(4, st_num_left_bottom).b_sup_corr = True
            propositions.get_proposed_stiffener(2, st_num_right_bottom).b_sup_corr_val = corr
            propositions.get_proposed_stiffener(4, st_num_left_bottom).b_sup_corr_val = corr
            print("side stiffeners too close to the bottom corners: ", dis_right_bottom_corner)
            geometry_ok = False

    if bottom_right != None:
        dis_bottom_left_corner = corner_bottom_left.y - bottom_left_2a.y
        if dis_bottom_left_corner < defaults.mindis_bottom_corner:
            corr = defaults.mindis_bottom_corner - dis_bottom_left_corner
            propositions.get_proposed_stiffener(3, st_num_bottom_left).b_sup = bottom_left.b_sup -corr
            propositions.get_proposed_stiffener(3, st_num_bottom_right).b_sup = bottom_right.b_sup - corr
            propositions.get_proposed_stiffener(3, st_num_bottom_left).b_sup_corr = True
            propositions.get_proposed_stiffener(3, st_num_bottom_right).b_sup_corr = True
            propositions.get_proposed_stiffener(3, st_num_bottom_left).b_sup_corr_val = corr
            propositions.get_proposed_stiffener(3, st_num_bottom_right).b_sup_corr_val = corr
            print("bottom stiffeners too close to the corners: ", dis_bottom_left_corner)
            geometry_ok = False





def get_top_right_corner(cs):
    for plate in cs.lines:
        points = []
        points.append(copy.deepcopy(plate.a))
        points.append(copy.deepcopy(plate.b))
    y_top_min = 0
    for point in points:
        if point.y <= y_top_min and point.z == 0:
            y_top_min = point.y
            top_right_corner = point
    return top_right_corner

def get_bottom_right_corner(cs):
    for plate in cs.lines:
        points = []
        points.append(copy.deepcopy(plate.a))
        points.append(copy.deepcopy(plate.b))
    y_bottom_min = 0
    z_bottom_max = 0
    for point in points:
        if point.y <= y_bottom_min and point.z >= z_bottom_max:
            y_bottom_min = point.y
            z_bottom_max = point.z
            bottom_right_corner = point
    return bottom_right_corner


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

"""def get_left_stiffeners(stiffeners):
    left_stiffeners = []
    for stiffener in stiffeners:
        if stiffener.lines[0].code.pl_position == 4:
            left_stiffeners.append(stiffener)
    return left_stiffeners"""


"""def get_top_left_stiffener(stiffeners):
    top_stiffeners = get_top_stiffeners(stiffeners)
    if top_stiffeners == []:
        return None
    top_left = top_stiffeners[0]
    for top_stiffener in top_stiffeners:
        if top_stiffener[0].code.st_number < top_left[0].code.st_number:
            top_left = top_stiffener
    return top_left"""

def get_top_right_stiffener(stiffeners):
    top_stiffeners = get_top_stiffeners(stiffeners)
    if top_stiffeners == []:
        return None
    top_right = top_stiffeners[0]
    for top_stiffener in top_stiffeners:
        if top_stiffener[0].code.st_number > top_right[0].code.st_number:
            top_right = top_stiffener
    return top_right

def get_right_top_stiffener(stiffeners):
    right_stiffeners = get_right_stiffeners(stiffeners)
    if right_stiffeners == []:
        return None
    right_top = right_stiffeners[0]
    for right_stiffener in right_stiffeners:
        if right_stiffener[0].code.st_number < right_top[0].code.st_number:
            right_top = right_stiffener
    return right_top
def get_right_bottom_stiffener(stiffeners):
    right_stiffeners = get_right_stiffeners(stiffeners)
    if right_stiffeners == []:
        return None
    right_bottom = right_stiffeners[0]
    for right_stiffener in right_stiffeners:
        if right_stiffener[0].code.st_number > right_bottom[0].code.st_number:
            right_bottom = right_stiffener
    return right_bottom

def get_bottom_right_stiffener(stiffeners):
    bottom_stiffeners = get_bottom_stiffeners(stiffeners)
    if bottom_stiffeners == []:
        return None
    bottom_right = bottom_stiffeners[0]
    for bottom_stiffener in bottom_stiffeners:
        if bottom_stiffener[0].code.st_number < bottom_right[0].code.st_number:
            bottom_right = bottom_stiffener
    return bottom_right

"""def get_bottom_left_stiffener(stiffeners):
    bottom_stiffeners = get_bottom_stiffeners(stiffeners)
    if bottom_stiffeners == []:
        return None
    bottom_left = bottom_stiffeners[0]
    for bottom_stiffener in bottom_stiffeners:
        if bottom_stiffener[0].code.st_number > bottom_left[0].code.st_number:
            bottom_left = bottom_stiffener
    return bottom_left

def get_left_bottom_stiffener(stiffeners):
    left_stiffeners = get_left_stiffeners(stiffeners)
    if left_stiffeners == []:
        return None
    left_bottom = left_stiffeners[0]
    for left_stiffener in left_stiffeners:
        if left_stiffener[0].code.st_number < left_bottom[0].code.st_number:
            left_bottom = left_stiffener
    return left_bottom
def get_bottom_left_stiffener(stiffeners):
    left_stiffeners = get_left_stiffeners(stiffeners)
    if left_stiffeners == []:
        return None
    bottom_left = left_stiffeners[0]
    for left_stiffener in left_stiffeners:
        if left_stiffener[0].code.st_number > bottom_left[0].code.st_number:
            bottom_left = left_stiffener
    return bottom_left"""
