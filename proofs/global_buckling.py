import math


def global_plate_buckling(stiffened_plate):
    #all methods still to be correctly implemented

    #finding critical buckling load
    phi_cr_p = ebplate()
    sigma_max = get_sigma_max()
    sigma_cr_p = sigma_max * phi_cr_p

    #calculating plate slenderness
    A_c_eff_loc = 0
    A_c = 0
    beta_a_c = A_c_eff_loc / A_c
    lambda_p_glob_bar = math.sqrt(beta_a_c * data.constants.get("fy") / sigma_cr_p)

    #calculate rho_glob for plate buckling
    #assumption: cs parts always supported on both sides
    rho_glob = 0
    #held on both sides
    if lamdbda_p_glob_bar <= 0.673:
        rho_loc = 1.0
    elif lambda_p_glob_bar > 0.673 and (3 + plate.psi) >= 0:
        rho_loc = (lambda_p_loc_bar - 0.055 * (3 + plate.psi)) / lambda_p_loc_bar**2
        if rho_loc > 1.0
            rho_loc = 1.0
    else:
        print("plate slenderness or stress ratio out of range")
        pass

    return rho_glob
