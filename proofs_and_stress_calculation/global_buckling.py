import math
import sys
from proofs_and_stress_calculation import stress_cal
from proofs_and_stress_calculation import column_buckling
from proofs_and_stress_calculation import global_plate_buckling
from classes import line
from classes import crosssection
from classes import point
from data_and_defaults import data
from data_and_defaults import defaults
sys.path.insert(0, './user_interface')
from output import printing


#function performing the buckling proof for each plate except the deck plate
def global_buckling(cs):
    cs = reduction_global_buckling(cs, 2)
    cs = reduction_global_buckling(cs, 3)
    cs = reduction_global_buckling(cs, 4)
    return cs


def reduction_global_buckling(cs, side):
    string = "\n   Side "+str(side)
    printing.printing(string, terminal = True)

    #extract the respective plate
    plate_glob = crosssection.crosssection(0,0,0)
    line_min = cs.get_line(pl_position = side, pl_type = 0)
    line_max = line_min
    for plate in cs.lines:
        if plate.code.pl_position == side:
            plate_glob.addline(plate)
            if plate.code.tpl_number != 0 and plate.code.tpl_number < line_min.code.tpl_number:
                line_min = plate
            if plate.code.tpl_number != 0 and plate.code.tpl_number > line_max.code.tpl_number:
                line_max = plate

    #initialize buckling factors
    chi_c = 1
    rho_p = 1
    sigma_cr_c = 1
    sigma_cr_p = 1
    all_tension = False
    plate_stiffened = True

    #case 1: the whole plate is under tension
    if line_min.sigma_a_red < 0 and line_max.sigma_b_red < 0:
        rho_c = 1
        all_tension = True

    #case 2: unstiffened plate
    elif len(plate_glob.lines) == 1:
        rho_c = 1
        plate_stiffened = False

    #case 3: stiffened plate partly compressed
    else:
        #perform global buckling proof, EC3 1-5, 4.5.2
        if defaults.do_global_plate_buckling == True:
            rho_p, sigma_cr_p = global_plate_buckling.global_plate_buckling(cs, plate_glob)
        else:
            rho_p = 1
            sigma_cr_p = 0

        #perform column buckling proof, EC3 1-5, 4.5.3
        if defaults.do_column_plate_buckling == True:
            height_zero_pressure = cs.get_center_z_red()
            if data.input_data.get("M_Ed") < 0:
                height_max_pressure = data.input_data.get("h")
            else:
                height_max_pressure = 0

            chi_c, sigma_cr_c = column_buckling.column_buckling(plate_glob, side, height_zero_pressure, height_max_pressure)
        else:
            chi_c = 1
            sigma_cr_c = 1

        #interaction according to EC3, 1-5, 4.5.4
        if defaults.do_column_plate_buckling == True and defaults.do_column_plate_buckling == True:
            eta = sigma_cr_p/sigma_cr_c -1
            if eta > 1:
                eta = 1
            elif eta < 0:
                eta = 0
        elif defaults.do_column_plate_buckling == True and defaults.do_column_plate_buckling == False:
            eta = 0
        elif defaults.do_column_plate_buckling == False and defaults.do_column_plate_buckling == True:
            eta = 1
        else:
            eta = 1

        rho_c = (rho_p - chi_c) * eta * (2 - eta) + chi_c


    line1 = "\n      4.5.4 Interaction between plate and column buckling"
    line2 = "\n           all_tension: " + str(all_tension)
    line3 = "\n           rho_c = " + str(rho_c)
    string = line1 + line2 + line3
    printing.printing(string, terminal = True)


    #EC 1-5 (4.5) edge plates not reduced by rho_c
    plate_a = cs.get_plate_a(side)
    plate_b = cs.get_plate_b(side)

    #set values to the cross section 
    for plate in cs.lines:
        if plate.code.pl_position == side:
            plate.chi_c = chi_c
            plate.sigma_cr_c = sigma_cr_c
            plate.rho_p = rho_p
            plate.sigma_cr_p = sigma_cr_p
            plate.rho_c_a = rho_c
            plate.rho_c_b = rho_c
            if plate == plate_a:
                plate.rho_c_a = 1
            if plate == plate_b:
                plate.rho_c_b = 1


    return cs
