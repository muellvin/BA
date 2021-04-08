import math
import defaults
import stresscal as stc
from ebplate import ebplate as ebp

def global_plate_buckling(cs, stiffened_plate):
    #all methods still to be correctly implemented

    #identify the border plates a and b and numbers of end stiffeners
    plate_a = None
    plate_b = None
    max_tpl = random.choice(stiffened_plate.lines).code.tpl_number
    min_tpl = random.choice(stiffened_plate.lines).code.tpl_number
    max_stn = 0
    min_stn = 1000

    for plate in stiffened_plate.lines:
        if plate.code.tpl_number <= min_tpl:
            plate_a = plate
        if plate.code.tpl_number >= max_tpl:
            plate_b = plate
        if plate.code.st_number <= min_stn and plate.code.st_number != 0:
            min_stn = plate.code.st_number
        if plate.code.st_number >= max_stn and plate.code.st_number != 0:
            max_stn = plate.code.st_number

    sigma_a = stc.get_sigma_a(cs, plate_a, data.input_data.get("M_Ed"))
    sigma_b = stc.get_sigma_b(cs, plate_b, data.input_data.get("M_Ed"))
    psi = min(sigma_a, sigma_b) / max(sigma_a, sigma_b)

    #get plate geometry
    h = 0
    for plate in stiffened_plate.lines:
        if plate.code.pl_type == 0:
            h += plate.get_length_tot()
    t = plate_a.t
    b = defaults.plate_length

    #coordinate transformation (a+b)/2 is the new origin and baseplate is horizontal
    #set new origin
    for plate in stiffened_plate.lines:
        plate.a.y -= 0.5*(plate_a.a.y + plate_b.b.y)
        plate.a.z -= 0.5*(plate_a.a.z + plate_b.b.z)
        plate.b.y -= 0.5*(plate_a.a.y + plate_b.b.y)
        plate.b.z -= 0.5*(plate_a.a.z + plate_b.b.z)

    #find rotation angle
    if plate_a.a.z == plate_b.b.z:
        #horizontal plate
        angle = 0
    if plate_a.a.y == plate_b.b.y:
        #vertical plate
        angle = math.pi/2
    else:
        #inclined plate
        pass

    #perform rotation
    for plate in stiffened_plate.lines:
        plate.a.y =
        plate.a.z =
        plate.b.y =
        plate.b.z =

    #claculate A and I of stiffened plate
    A_tot = stiffened_plate.get_area_tot()
    I_tot = stiffened_plate.get_i_y_tot()

    #create a list of all stiffeners
    stiffener_list = []
    plate_num_list = []
    for st_number in range(min_stn, max_stn+1, 1):
        stiffener_list[st_number - min_stn] = cs.crosssection()
        corresp_tpl = 0
        for plate in stiffened_plate:
            if plate.code.st_number == st_number:
                stiffener_list[st_number - min_stn].addline(plate)
                if plate.code_tpl_number =! 0:
                    corresp_tpl = plate.code_tpl_number
                    plate_num_list[st_number - min_stn] = corresp_tpl
        for plate in stiffened_plate:
            if plate.code.tpl_number == corresp_tpl -1 or plate.code.tpl_number == corresp_tpl +1:
                stiffener_list[st_number - min_stn].addline(plate)

    #calculate adimensional parameters for each stiffener
    #tbd
    stiffeners_ebp = []
    for i in range(len(stiffener_list)):
        #extract the useful plates
        stiffener = stiffener_list[i]
        corresp_tpl = plate_num_list[i]
        center_plate = None
        top_plate = None
        bottom_plate = None
        for plate in stiffener.lines:
            if plate.code.tpl_number == corresp_tpl:
                center_plate = plate
            elif plate.code.tpl_number == corresp_tpl+1:
                bottom_plate = plate
            elif plate.code.tpl_number == corresp_tpl-1:
                top_plate = plate
        #find distance to point a
        delta_z = center_plate.cal_center_z() - plate_a.a.z
        delta_y = center_plate.cal_center_y() - plate_y.a.y
        distance = math.sqrt(delta_z **2 + delta_y **2)
        #calculate delta
        delta = delta()
        #calculate gamma
        gamma = gamma()
        #calculate theta
        theta = theta()
        stiffeners_ebp[counter] = (distance, delta, gamma, theta)

    #finding critical buckling load
    phi_cr_p = ebp.ebplate(b,h,t,sigma_a, sigma_b, stiffeners_ebp)
    sigma_max = max(sigma_a, sigma_b)
    sigma_cr_p = sigma_max * phi_cr_p

    #calculating plate slenderness
    #correct beta_a_c still to be implemented
    A_c_eff_loc = 1
    A_c = 1
    beta_a_c = A_c_eff_loc / A_c
    lambda_p_glob_bar = math.sqrt(beta_a_c * data.constants.get("fy") / sigma_cr_p)

    #calculate rho_glob for plate buckling
    #assumption: cs parts always supported on both sides
    rho_glob = 0
    #held on both sides
    if lamdbda_p_glob_bar <= 0.673:
        rho_glob = 1.0
    elif lambda_p_glob_bar > 0.673 and (3 + psi) >= 0:
        rho_glob = (lambda_p_loc_bar - 0.055 * (3 + psi)) / lambda_p_glob_bar**2
        if rho_glob > 1.0
            rho_glob = 1.0
    else:
        print("plate slenderness or stress ratio out of range")
        pass

    return rho_glob
