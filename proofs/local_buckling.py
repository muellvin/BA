
import data
import defaults
import stress_cal
import math


def local_buckling(cs):
    cal_sigma_psi_red(cs)
    change = 1
    while change > defaults.convergence_limit:
        m_rd_el_eff_old = cs.get_m_rd_el_eff()
        for line in cs.lines:
            local_buckling_plate(line)
        cal_sigma_psi_red(cs)
        m_rd_el_eff_new = cs.get_m_rd_el_eff()
        change = abs(abs( m_rd_el_eff_new / m_rd_el_eff_old ) - 1)


#function calculating the normal stresses at points a and b of every plate and setting these attributes as well as the stress ratio
def cal_sigma__psi_red(cs):
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
    else:
        print("Psi value out of range, found at k sigma loc")
        pass

    #EC A.1
    sigma_E_loc = (math.pi**2 * data.constants.get("E") * plate.t**2) / (12 * (1-data.constants.get("nu")**2) * plate.get_length_tot()**2)
    sigma_cr_p_loc = k_sigma_loc * sigma_E_loc

    #EC 4.4 (2)
    lambda_p_loc_bar = math.sqrt(data.constants.get("fy") / sigma_cr_p_loc)
    #held on both sides -> EC 4.4 (2)
    rho_loc = 0
    #held on both sides
    if lamdbda_p_loc_bar <= 0.673:
        rho_loc = 1.0
    elif lambda_p_loc_bar > 0.673 and (3 + plate.psi) >= 0:
        rho_loc = (lambda_p_loc_bar - 0.055 * (3 + plate.psi)) / lambda_p_loc_bar**2
        if rho_loc > 1.0
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

    plate.p1.y = plate.a.y + b_e1/plate.get_length_tot()*(plate.b.y - plate.a.y)
    plate.p1.z = plate.a.z + b_e1/plate.get_length_tot()*(plate.b.z - plate.a.z)
    plate.p2.y = plate.b.y + b_e2/plate.get_length_tot()*(plate.a.y - plate.b.y)
    plate.p2.z = plate.b.z + b_e2/plate.get_length_tot()*(plate.a.z - plate.b.z)
