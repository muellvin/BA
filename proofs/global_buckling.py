import math
import defaults
from proofs import stress_cal as stc
from ebplate import ebplate as ebp
from classes import line as ln
from classes import crosssection
from classes import point as pt
from output import geometry_output as go
from proofs import column_buckling as column
from proofs import global_plate_buckling as plate_global
import random
import data

def global_buckling(cs):
    cs = reduction_global_buckling(cs, 2)
    cs = reduction_global_buckling(cs, 3)
    cs = reduction_global_buckling(cs, 4)
    return cs

#create a cs with all plates of this side
def reduction_global_buckling(cs, side):
    plate_glob = crosssection.crosssection(0,0,0)
    for line in cs.lines:
        if line.code.pl_position == side:
            plate_glob.addline(line)

    chi_c, sigma_cr_c = column.column_buckling(plate_glob, side)
    rho_p, sigma_cr_p = plate_global.global_plate_buckling(cs, plate_glob)
    print("rho_p = " + str(rho_p))
    print("chi_c = " + str(chi_c))


    eta = sigma_cr_p/sigma_cr_c -1
    rho_c = (rho_p - chi_c) * eta * (2 - eta) + chi_c
    print("rho_c = " + str(rho_c))

    for line in cs.lines:
        if line.code.pl_position == side:
            self.chi_c = chi_c
            self.sigma_cr_c = sigma_cr_c
            self.rho_p = rho_p
            self.sigma_cr_p = sigma_cr_p
            line.rho_c = rho_c


    return cs
