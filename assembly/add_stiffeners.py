import math
import shapely
import random
import copy
from classes import point
from classes import line
from classes import crosssection
from classes import plate_code
from assembly import substantiate
from assembly import merge
from assembly import check_geometry
from data_and_defaults import defaults


#initial cs is empty (only four lines)
def add_stiffener_set(initial_cs, propositions, optimizer):
    iterations = 0
    stiffener_list = None
    geometry_ok = False

    assert optimizer == "a" or optimizer == "b", "Wrong input for optimizer."

    if propositions.stiffeners == []:
        return initial_cs

    if optimizer == "a":
        stiffener_list = substantiate.substantiate(initial_cs, propositions, optimizer)
        if stiffener_list == False:
            print("\n\n Substantiate finished with FALSE")
            return False

    if optimizer == "b":
        while geometry_ok == False and iterations <= 1:
            iterations += 1
            stiffener_list = substantiate.substantiate(initial_cs, propositions, optimizer)
            if stiffener_list == False:
                print("\n\n Substantiate finished with FALSE")
                return False
            proposition, geometry_ok = check_geometry.check_geometry(initial_cs, stiffener_list, propositions)
            print(geometry_ok)

    print("\n\n Substantiate finished with success")
    if geometry_ok == False:
        return False

    next_cs = merge.merge(copy.deepcopy(initial_cs), stiffener_list)
    next_cs.st_props = proposition
    return next_cs



#function creating a crosssection, which is the three lines of a stiffener at the place desired
def create_stiffener_global(pl_position, st_number, center_y, center_z, angle, b_sup, b_inf, h, t):
    y_corr = center_y - math.cos(angle)*b_sup*0.5
    z_corr = center_z - math.sin(angle)*b_sup*0.5
    assert b_sup >= b_inf, "width out of bound or wrong way around"
    half_width_diff = (b_sup - b_inf)/2
    length_side = math.sqrt(half_width_diff**2 + h**2)
    if half_width_diff > 0:
        own_angle = math.atan(h/half_width_diff)
    else:
        own_angle = math.pi/2

    #create plate 2
    a2 = point.point(y_corr,z_corr)
    b2 = point.point(y_corr + math.cos(own_angle+angle)*length_side, z_corr + math.sin(own_angle+angle)*length_side)
    code2 = plate_code.plate_code(pl_position, 1, 0, st_number, 2)
    line2 = line.line(code2, a2, b2, t)


    #create plate 3
    a3 = point.point(y_corr + math.cos(own_angle+angle)*length_side, z_corr + math.sin(own_angle+angle)*length_side)
    b3 = point.point(a3.y + math.cos(angle)*b_inf, a3.z + math.sin(angle)*b_inf)
    code3 = plate_code.plate_code(pl_position, 1, 0, st_number, 3)
    line3 = line.line(code3, a3, b3, t)

    #create plate 4
    a4 = point.point(a3.y + math.cos(angle)*b_inf, a3.z + math.sin(angle)*b_inf)
    b4 = point.point(y_corr + math.cos(angle)*b_sup, z_corr + math.sin(angle)*b_sup)
    code4 = plate_code.plate_code(pl_position, 1, 0, st_number, 4)
    line4 = line.line(code4, a4, b4, t)

    stiffener_global = crosssection.crosssection(b_sup, b_inf, h)
    #add the lines to itself
    stiffener_global.addline(line2)
    stiffener_global.addline(line3)
    stiffener_global.addline(line4)
    return stiffener_global

#function creating a crosssection, which is the three lines of a stiffener. it is in its own coordinate system -> for calculation of i_along
def create_stiffener_local(b_sup, b_inf, h, t):
    #assert b_sup >= b_inf, "width out of bound or wrong way around"
    half_width_diff = b_sup - b_inf
    length_side = math.sqrt(half_width_diff**2 + h**2)
    own_angle = math.atan(half_width_diff / h)

    #create plate 2
    a2 = point.point(-b_sup/2,0)
    b2 = point.point(a2.y + math.sin(own_angle)*length_side, math.cos(own_angle)*length_side)
    code2 = plate_code.plate_code(0, 1, 0, 0, 2)
    line2 = line.line(code2, a2, b2, t)

    #create plate 3
    a3 = b2
    b3 = point.point(a3.y + b_inf, a3.z)
    code3 = plate_code.plate_code(0, 1, 0, 0, 3)
    line3 = line.line(code3, a3, b3, t)

    #create plate 4
    a4 = b3
    b4 = point.point(b_sup/2, 0)
    code4 = plate_code.plate_code(0, 1, 0, 0, 4)
    line4 = line.line(code4, a4, b4, t)

    stiffener_local = crosssection.crosssection(b_sup, b_inf, h)
    #add the lines to itself
    stiffener_local.addline(line2)
    stiffener_local.addline(line3)
    stiffener_local.addline(line4)
    return stiffener_local


def get_i_along_stiffener(b_sup, b_inf, h, t):
    stiffener_local = create_stiffener_local(b_sup, b_inf, h, t)
    i_along = stiffener_local.get_i_y_tot()
    return i_along

def get_area_stiffener(b_sup, b_inf, h, t):
    stiffener_local = create_stiffener_local(b_sup, b_inf, h, t)
    area = stiffener_local.get_area_tot()
    return area
