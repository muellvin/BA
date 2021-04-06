
import data
import stress_cal
import math


def local_buckling(cs):
    set_sigma_red(cs)
    for line in cs.lines:
        local_buckling_plate(line)


def set_sigma_red(cs):
    M_Ed = data.input_data.get("M_Ed")
    for line in cs.lines:
        line.sigma_a_red = stress_cal.sigma_a_red(cs, line, M_Ed)
        line.sigma_b_red = stress_cal.sigma_b_red(cs, line, M_Ed)
        #set the stress ratio = sigma min / sigma max
        #correct for EC having tension as negative by inverting the ratio to be sigma max / sigma min
        if line.sigma_a_red < line.sigma_b_red:
            line.psi = line.sigma_b_red / line.sigma_a_red


def local_buckling_plate(plate):
    #all plates are supported on both sides -> Table 4.1
    k_sigma_loc = 0
    if plate.psi == 1:
        k_sigma_loc = 4
    elif 0 < plate.psi < 1:
        k_sigma_loc = 8.2/(1.05 + plate.psi)
    elif plate.psi == 0:
        k_sigma_loc = 7.81
    elif -1 < plate.psi < 0:
        k_sigma_loc = 7.81 - 6.29*plate.psi + 9.78 * plate.psi**2
    elif plate.psi == -1:
        k_sigma_loc = 23.9
    elif -3 < plate.psi < -1:
        k_sigma_loc = 5.98*(1-plate.psi)**2

    sigma_E = (math.pi**2 * data.constants.get("E") * plate.t**2) / (12 * (1-data.constans.get("nu")**2) * plate.get_length_tot()**2)
