from classes import crosssection
import math
import data
from classes import point


#EC 1993 1-5 (7) all combinations of stiffeners as a member have to be investigated
#
#according to the EC 1993 1-5 (1) the equivalent member can no longer be seen as supported on the sides
#
#according to A.2 (3) -> Illustration A.1
#the contributing widths are the ones defined by local buckling
#for both the stiffener and the neighbouring plates


def column(plate_glob, side):
    #add the lines to the right list
    stiffener_lines = []
    tpl_lines_list = []
    stiffeners_list = []

    for line in plate_glob.lines:
        if line.code.tpl_number == 0:
            stiffener_lines.append(line)
        elif line.code.pl_type == 0:
            tpl_lines_list.append(line)

    st_number_min = stiffener_lines[0].code.st_number
    st_number_max = stiffener_lines[0].code.st_number
    number_of_stiffeners = int(len(stiffener_lines)/3)

    for line in stiffener_lines:
        if line.code.st_number < st_number_min:
            st_number_min = line.code.st_number
        elif line.code.st_number > st_number_max:
            st_number_max = line.code.st_number

    for i in range(number_of_stiffeners):
        stiffeners_list.append(crosssection.crosssection(0, 0, 0))
        for line in stiffener_lines:
            if line.code.st_number == i+st_number_min:
                stiffeners_list[i].lines.append(line)
                stiffener_lines.remove(line)


    #sort the lists
    tpl_lines_list = sorted(tpl_lines_list, key = lambda line: line.code.tpl_number)
    stiffeners_list = sorted(stiffeners_list, key = lambda stiffener: stiffener.lines[0].code.st_number)


    #create sets
    tpl_st_lines_set = {}
    tpl_betw_lines_set = {}
    i = 1
    for line in tpl_lines:
        if i%2 == 0:
            st_number = st_number_min + int(i/2) - 1
            tpl_lines_set.add(st_number, line)
        else:
            st_number_before = st_number_min + int(i/2) - 1
            tpl_betw_lines_set.add(st_number_before, line)
        i += 1

    stiffeners_set = {}
    for stiffener in stiffeners_list:
        st_number = stiffener.lines[0].code.st_number
        stiffeners_set.add(st_number, stiffener)


    """A_sl,i and I_sl,i for every single column (one stiffener with the supporting plate widths on each side)"""
    columns = {}

    i = st_number_min
    while i < st_number_max:
        stiffener_i = stiffeners_set.get(i)
        plate_between = tpl_st_lines_set.get(i)
        plate_before = tpl_betw_lines_set.get(i-1)
        plate_after = tpl_betw_lines_set.get(i)

        #if the widths were not reduced (p1 is the same as p2) the whole plate is taken into account not only until one of p1 or p2
        if dis_points(plate_before.p1, plate_before.p2) < 0.05:
            plate_before_A = plate_before.get_area_tot()
            plate_before_I = plate_before.get_i_along_tot()
            sigma_border_before = plate_before.sigma_a_red
            border_before = plate_before.a
        else:
            plate_before_A = plate_before.get_area_red2()
            plate_before_I = plate_before.get_i_along_red2()
            sigma_border_before = plate_before.sigma_a_red
            border_before = plate_before.p2

        if dis_points(plate_after.p1, plate_after.p2) < 0.05:
            plate_after_A = plate_after.get_area_tot()
            plate_after_I = plate_after.get_i_along_tot()
            sigma_border_after = plate_after.sigma_b_red
            border_after = plate_after.b
        else:
            plate_after_A = plate_after.get_area_red1()
            plate_after_I = plate_after.get_i_along_red1())
            sigma_border_after = plate_after.sigma_b_red
            border_after = plate_after.p1


        #EC 1993 1-5 4.5.3 (3)
        A_sl_i = stiffener_i.get_area_red() + plate_before_A + plate_after_A
        I_sl_i = stiffener_i.get_i_along_red() + plate_before_I + plate_after_I
        sigma_cr_sl_i = (math.pi**2 * data.constants.get("E") * I_sl_i) / (A_sl_i * data.input_data.get("l"))


        ######calculation of sigma_cr_c################
        #span of column
        b = dis_points(border_before, border_after)
        #stress ratio across the whole cross-section of the column
        stress_ratio = min(sigma_border_before, sigma_border_after) / max(sigma_border_before, sigma_border_after)

        #assure the column is under pressure (positive) somewhere
        if sigma_border_before > 0 or sigma_border_after > 0:
            b_c = b * 1/(1-stress_ratio)
        else:
            b_c = 0

        tpl_st_center = point.point(tpl_st_lines_set.get(i).get_center_y_tot(), tpl_st_lines_set_get(i).get_center_z_tot())

        if sigma_border_before < sigma_border_after:
            b_sl_1 = dis_points(border_before, tpl_st_center)
        if sigma_border_before > sigma_border_after:
            b_sl_1 = dis_points(border_after, tpl_st_center)

        sigma_cr_c = sigma_cr_sl_i * b_c / b_sl_1




        column_i = column_class(i, A_sl_i, I_sl_i, sigma_cr_c)
        columns.add(st_number, column_i)


        i += 1



def dis_points(a, b):
    return math.sqrt((a.y - b.y)**2 + (a.z - b.z)**2)

class column_class():
    def __init__(self,st_number, A, I, sigma_cr_sl):
        self.st_number = st_number
        self.A = A
        self.I = I
        self.sigma_cr_sl = sigma_cr_sl
