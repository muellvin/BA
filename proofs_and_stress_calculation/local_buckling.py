import math
import sys
from data_and_defaults import data
from data_and_defaults import defaults
from proofs_and_stress_calculation import stress_cal
sys.path.insert(0, './user_interface')
from output import printing


def local_buckling(cs):
    string = "\n   Iteratively changing the widths until M_Rd_el_eff converges to a limit of "+str(defaults.convergence_limit_local_buckling)
    printing.printing(string, terminal = True)

    cs = cal_sigma_psi_red(cs)
    change = 1
    i = 1
    while change > defaults.convergence_limit_local_buckling:
        m_rd_el_eff_old = cs.get_m_rd_el_eff()
        for line in cs.lines:
            cs = local_buckling_plate(cs, line)
        cs = cal_sigma_psi_red(cs)
        m_rd_el_eff_new = cs.get_m_rd_el_eff()
        change = abs(abs( m_rd_el_eff_new / m_rd_el_eff_old ) - 1)

        i += 1
    return cs


#function calculating the normal stresses at points a and b of every plate and setting these attributes as well as the stress ratio
def cal_sigma_psi_red(cs):
    M_Ed = data.input_data.get("M_Ed")
    for line in cs.lines:
        line.sigma_a_red = stress_cal.get_sigma_a_red(cs, line, M_Ed)
        line.sigma_b_red = stress_cal.get_sigma_b_red(cs, line, M_Ed)
        line.sigma_p1_red = stress_cal.get_sigma_p1_red(cs, line, M_Ed)
        line.sigma_p2_red = stress_cal.get_sigma_p2_red(cs, line, M_Ed)
        #set the stress ratio = sigma min / sigma max
        line.psi = min(line.sigma_a_red, line.sigma_b_red) / max(line.sigma_a_red, line.sigma_b_red)

        if line.sigma_a_red < 0 and line.sigma_b_red < 0:
            line.psi = 1
    return cs


def local_buckling_plate(cs, line_to_do):
    plate = None
    for line in cs.lines:
        if line == line_to_do:
            plate = line

    only_tension = plate.sigma_a_red < 0 and plate.sigma_b_red < 0
    deck = plate.code.pl_position == 1

    #all plates are supported on both sides (internal compression elements) -> Table 4.1
    #plate buckling coefficient
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
    else:
        #the only other case is if psi is smaller than -3 because when psi was set
        #if there is only tension (the only way to have a psi greater than 1) we set psi to 1
        only_tension = True

    if only_tension != True and deck != True:
        #EC A.1
        sigma_E_loc = (math.pi**2 * data.constants.get("E") * plate.t**2) / (12 * (1-data.constants.get("nu")**2) * plate.get_length_tot()**2)
        #elastic critical plate buckling stress

        sigma_cr_p_loc = k_sigma_loc * sigma_E_loc

        #EC 4.4 (2)

        lambda_p_loc_bar = math.sqrt(data.constants.get("f_y") / sigma_cr_p_loc)
        #held on both sides -> EC 4.4 (2)
        rho_loc = 0
        #held on both sides
        if lambda_p_loc_bar <= 0.673:
            rho_loc = 1.0
        elif lambda_p_loc_bar > 0.673 and (3 + plate.psi) >= 0:
            rho_loc = (lambda_p_loc_bar - 0.055 * (3 + plate.psi)) / lambda_p_loc_bar**2
            if rho_loc > 1.0:
                rho_loc = 1.0
        else:
            print("plate slenderness or stress ratio out of range")
            pass

        plate.rho_loc = rho_loc

        #again in table 4.1 the effective widths
        b_eff = 0
        b_e1 = 0
        b_e2 = 0


        if plate.psi == 1:
            b_eff = plate.rho_loc * plate.get_length_tot()
            b_e1 =  b_e2 = 0.5 * b_eff
        elif 0 <= plate.psi < 1:
            b_eff = plate.rho_loc * plate.get_length_tot()
            b_e1 = 2 / (5-plate.psi) * b_eff
            b_e2 = b_eff - b_e1
        elif plate.psi < 0:
            b_eff = plate.rho_loc * plate.get_length_tot() / (1 - plate.psi)
            b_e1 = 0.4 * b_eff
            b_e2 = 0.6 * b_eff
            #add the part that is under tension
            b_e2 = b_e2 + plate.get_length_tot() * (-plate.psi)/(1-plate.psi)
        else:
            print("Psi value out of range, found at widths")

        if plate.sigma_a_red > plate.sigma_b_red:
            plate.p1.y = plate.a.y + b_e1/plate.get_length_tot()*(plate.b.y - plate.a.y)
            plate.p1.z = plate.a.z + b_e1/plate.get_length_tot()*(plate.b.z - plate.a.z)
            plate.p2.y = plate.b.y + b_e2/plate.get_length_tot()*(plate.a.y - plate.b.y)
            plate.p2.z = plate.b.z + b_e2/plate.get_length_tot()*(plate.a.z - plate.b.z)
        else:
            plate.p1.y = plate.a.y + b_e2/plate.get_length_tot()*(plate.b.y - plate.a.y)
            plate.p1.z = plate.a.z + b_e2/plate.get_length_tot()*(plate.b.z - plate.a.z)
            plate.p2.y = plate.b.y + b_e1/plate.get_length_tot()*(plate.a.y - plate.b.y)
            plate.p2.z = plate.b.z + b_e1/plate.get_length_tot()*(plate.a.z - plate.b.z)

    return cs
