from classes import crosssection
from classes import point
from classes import line
import math
import data



#EC 1993 1-5 (7)  stiffeners as a member have to be investigated as they can be of different form
#
#according to the EC 1993 1-5 (1) the equivalent member can no longer be seen as supported on the sides
#
#according to A.2 (3) -> Illustration A.1
#the contributing widths are the ones defined by local buckling

#does not write attributes thus does not need cs
def column_buckling(plate_glob, side):
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
            tpl_lines_set.update({st_number: line})
        else:
            st_number_before = st_number_min + int(i/2) - 1
            tpl_betw_lines_set.update({st_number_before: line})
        i += 1

    stiffeners_set = {}
    for stiffener in stiffeners_list:
        st_number = stiffener.lines[0].code.st_number
        stiffeners_set.update({st_number, stiffener})




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
            plate_before_eff = line.line(border_before, plate_before.b)
        else:
            plate_before_A = plate_before.get_area_red2()
            plate_before_I = plate_before.get_i_along_red2()
            sigma_border_before = plate_before.sigma_a_red
            border_before = plate_before.p2
            plate_before_eff = line.line(border_before, plate_before.b)

        if dis_points(plate_after.p1, plate_after.p2) < 0.05:
            plate_after_A = plate_after.get_area_tot()
            plate_after_I = plate_after.get_i_along_tot()
            sigma_border_after = plate_after.sigma_b_red
            border_after = plate_after.b
            plate_after_eff = line.line(plate_after.a, border_after)
        else:
            plate_after_A = plate_after.get_area_red1()
            plate_after_I = plate_after.get_i_along_red1()
            sigma_border_after = plate_after.sigma_b_red
            border_after = plate_after.p1
            plate_after_eff = line.line(plate_after.a, border_after)


        #EC 1993 1-5 4.5.3 (3)
        A_sl = stiffener_i.get_area_tot() + plate_before_A + plate_after_A
        A_sl_eff = stiffener_i.get_area_red() + plate_before_A + plate_after_A
        I_sl = stiffener_i.get_i_along_tot(stiffener_i.get_line(pl_position = side, pl_type = 0)) + plate_before_I + plate_after_I
        sigma_cr_sl = (math.pi**2 * data.constants.get("E") * I_sl) / (A_sl * data.input_data.get("a"))


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

        sigma_cr_c = sigma_cr_sl * b_c / b_sl_1

        #excentrisities
        st_center = point.point(stiffener_i.get_center_y_tot(), stiffener_i.get_center_z_tot())

        sl_cs = crosssection.crossection(0,0,0)
        for line in stiffener_i.lines:
            sl_cs.addline(line)
        sl_cs.addline(plate_before_eff)
        sl_cs.addline(plate_after_eff)

        sl_center = point.point(sl_cs.get_center_y_tot(), sl_cs.get_center_z_tot())

        e2 = dis_line_point(tpl_st_lines_set.get(i), sl_center)
        e1 = dis_line_point(tpl_st_lines_set.get(i), st_center) - e2

        column = column_class(i, A_sl, A_sl_eff, I_sl, sigma_cr_c, e1, e2)
        columns.add(st_number, column)

        i += 1

    Chi_c = 1
    sigma_cr_c = 1

    #searches for the single column buckling mechanism with the smallest Chi_c
    for column in columns:
        Chi_c_column = column_buckling_Chi_c(column)
        if Chi_c_column < Chi_c:
            Chi_c = Chi_c_column
            sigma_cr_c = column.sigma_cr_c

    return Chi_c, sigma_cr_c


def column_buckling_Chi_c(column):
    beta_A_c = column.A_sl_eff / column.A_sl
    lambda_c_bar = math.sqrt(beta_A_c * data.constants.get("f_y") / column.sigma_cr_c)

    i = math.sqrt(column.I_sl/column.A_sl)
    e = max(column.e1, column.e2)
    alpha = 0.34 #curve b for closed stiffeners
    alpha_e = alpha + 0.09/(e/i)

    Phi_c = 0.5*(1+alpha_e*(lambda_c_bar - 0.2) + lambda_c_bar**2)
    Chi_c = 1 / (Phi_c + math.sqrt(Phi_c**2 - lambda_c_bar**2))

    return Chi_c



def dis_points(a, b):
    return math.sqrt((a.y - b.y)**2 + (a.z - b.z)**2)

def dis_line_point(line, point):
    line_vector_y = 1/line.get_length_tot() * (line.b.y - line.a.y)
    line_vector_z = 1/line.get_length_tot() * (line.b.z - line.a.z)
    norm_vector_y = - line_vector_z
    norm_vector_z = line_vector_y

    point_vector_y = point.y - line.a.y
    point_vector_z = point.z - line.a.z

    #dot product
    dis = point_vector_y * norm_vector_y + point_vector_z * norm_vector_z

    return dis



class column_class():
    def __init__(self,st_number, A_sl, A_sl_eff, I_sl, sigma_cr_c, e1, e2):
        self.st_number = st_number
        self.A_sl = A_sl
        self.A_sl_eff = A_sl_eff
        self.I_sl = I_sl
        self.sigma_cr_c = sigma_cr_c
