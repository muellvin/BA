import math
import defaults
from proofs import stress_cal
from proofs import column_buckling
from proofs import global_plate_buckling

from ebplate import ebplate as ebp
from classes import line as ln
from classes import crosssection
from classes import point as pt
from output import geometry_output as go
from proofs import column_buckling as column
from proofs import global_plate_buckling as plate_global
import random
import data
import defaults

def global_buckling(cs):
    cs = reduction_global_buckling(cs, 2)
    cs = reduction_global_buckling(cs, 3)
    cs = reduction_global_buckling(cs, 4)
    return cs

#create a cs with all plates of this side
def reduction_global_buckling(cs, side):
    print("\n------------------------ reduction_global_buckling for side "+str(side)+" ---------------------------------")
    plate_glob = crosssection.crosssection(0,0,0)
    for line in cs.lines:
        if line.code.pl_position == side:
            plate_glob.addline(line)

    chi_c = 1
    rho_p = 1
    sigma_cr_c = 1
    sigma_cr_p = 1
    eta = 1

    if defaults.do_column_plate_buckling == True:
        chi_c, sigma_cr_c = column_buckling.column_buckling(plate_glob, side)
    if defaults.do_global_plate_buckling == True:
        rho_p, sigma_cr_p = global_plate_buckling.global_plate_buckling(cs, plate_glob)

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

    rho_c = (rho_p - chi_c) * eta * (2 - eta) + chi_c
    print("rho_c = " + str(rho_c))

    plate_a = cs.get_plate_a(side)
    plate_b = cs.get_plate_b(side)
    for line in cs.lines:
        if line.code.pl_position == side:
            line.chi_c = chi_c
            line.sigma_cr_c = sigma_cr_c
            line.rho_p = rho_p
            line.sigma_cr_p = sigma_cr_p
            line.rho_c_a = rho_c
            line.rho_c_b = rho_c
            if line == plate_a:
                line.rho_c_a = 1
            if line == plate_b:
                line.rho_c_b = 1


    return cs
