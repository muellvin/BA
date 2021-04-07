import math
import defaults
import stresscal as stc
from ebplate import ebplate as ebp

def global_plate_buckling(cs, stiffened_plate):
    #all methods still to be correctly implemented

    #identify the border plates a and b
    plate_a = None
    plate_b = None
    max = random.choice(stiffened_plate.lines).code.tpl_number
    min = random.choice(stiffened_plate.lines).code.tpl_number
    for plate in stiffened_plate.lines:
        if plate.code.tpl_number <= min:
            plate_a = plate
        elif plate.code.tpl_number >= max:
            plate_b = plate

    sigma_a = stc.get_sigma_a(cs, plate_a, data.input_data.get("M_Ed"))
    sigma_b = stc.get_sigma_b(cs, plate_b, data.input_data.get("M_Ed"))

    #get plate geometry
    h = 0
    for plate in stiffened_plate.lines:
        if plate.code.pl_type == 0:
            h += plate.get_length_tot()
    t = plate_a.t
    b = defaults.plate_length

    #create a list of all stiffeners
    #tbd

    #calculate adimensional parameters for each stiffener
    #tbd

    #finding critical buckling load
    phi_cr_p = ebp.ebplate(b,h,t,sigma_a, sigma_b, stiffeners_ebp)
    sigma_max = max(sigma_a, sigma_b)
    sigma_cr_p = sigma_max * phi_cr_p

    #calculating plate slenderness
    A_c_eff_loc = 1
    A_c = 1
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
