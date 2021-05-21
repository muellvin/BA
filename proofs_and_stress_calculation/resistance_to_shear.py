import math
import copy
from data_and_defaults import defaults
from data_and_defaults import data
from proofs_and_stress_calculation import stress_cal
from ebplate import ebplate
from classes import crosssection
from user_interface/output import printing

def resistance_to_shear(plate_glob, V_Ed_plate):
    string = "\n   5. Resistance to shear"
    printing.printing(string, terminal = True)

    #get values of constants
    f_y = data.constants.get("f_y")
    gamma_M1 = data.constants.get("gamma_M1")
    eta = defaults.eta
    side = plate_glob.lines[0].code.pl_position
    a = defaults.plate_length

    #import important geometry parameters
    h_w = 0
    for plate in plate_glob.lines:
        if plate.code.pl_type == 0:
            h_w += plate.get_length_tot()
    t = plate_glob.get_line(pl_type = 0).t


    stiffened = True
    if len(plate_glob.lines) == 1:
        stiffened = False

    #calculate k_tau
    k_tau = 0
    if stiffened == False:
        line1 = "\n      unstiffened plate; (A.5)"
        if a / h_w >= 1:
            k_tau = 5.34 + 4*(h_w/a)**2

            line2 = "\n      k_tau: "+str(k_tau)
        else:
            k_tau = 4.0 + 5.34 * (h_w/a)**2
            line2 = "\n      k_tau: "+str(k_tau)
        string = line1 + line2
        printing.printing(string, terminal = True)

    else:
        line1 = "\n      stiffened plate; EBPlate"
        plate_a = None
        plate_b = None
        min_tpl = -1
        max_tpl = -1
        max_stn = 0
        min_stn = 1000
        stiffened_plate = copy.deepcopy(plate_glob)
        for plate in stiffened_plate.lines:
            if plate.code.pl_type == 0:
                if min_tpl == -1 and max_tpl == -1:
                    min_tpl = plate.code.tpl_number
                    max_tpl = plate.code.tpl_number
                if plate.code.tpl_number <= min_tpl:
                    plate_a = plate
                if plate.code.tpl_number >= max_tpl:
                    plate_b = plate
            else:
                if plate.code.st_number <= min_stn and plate.code.st_number != 0:
                    min_stn = plate.code.st_number
                if plate.code.st_number >= max_stn and plate.code.st_number != 0:
                    max_stn = plate.code.st_number

        assert plate_a != None and plate_b != None, "For-Loop failed."

        move_z = 0.5*(plate_a.a.z + plate_b.b.z)
        move_y = 0.5*(plate_a.a.y + plate_b.b.y)

        for plate in stiffened_plate.lines:
            plate.a.y -= move_y
            plate.a.z -= move_z
            plate.b.y -= move_y
            plate.b.z -= move_z

        #find rotation angle
        if plate_a.a.z == plate_b.b.z:
            #horizontal plate
            angle = 0
        if plate_a.a.y == plate_b.b.y:
            #vertical plate
            angle = math.pi/2
        else:
            #inclined plate
            angle = - math.atan((plate_b.b.z-plate_a.a.z)/(plate_b.b.y-plate_a.a.y))

        #perform rotation
        for plate in stiffened_plate.lines:
            ay = plate.a.y
            az = plate.a.z
            by = plate.b.y
            bz = plate.b.z
            plate.a.y = math.cos(angle)*ay - math.sin(angle)*az
            plate.a.z = math.sin(angle)*ay + math.cos(angle)*az
            plate.b.y = math.cos(angle)*by - math.sin(angle)*bz
            plate.b.z = math.sin(angle)*by + math.cos(angle)*bz

        stiffener_list = []
        stiffeners_ebp = []
        for st_number in range(min_stn, max_stn+1, 1):
            i = st_number - min_stn
            stiffener_list.insert(i, crosssection.crosssection(0,0,0))
            #find three plates of stiffener
            for plate in stiffened_plate.lines:
                if plate.code.st_number == st_number:
                    stiffener_list[st_number - min_stn].addline(plate)
            b_inf = stiffener_list[i].get_line(st_pl_position = 3).get_length_tot()
            b_sup = stiffener_list[i].get_line(st_pl_position = 1).get_length_tot()
            diff = (0.5*(b_sup - b_inf))
            #print("diff")
            #print(diff)
            diag = stiffener_list[i].get_line(st_pl_position = 2).get_length_tot()
            #print("diag")
            #print(diag)
            h = math.sqrt(diag**2-diff**2)
            t_stiff = stiffener_list[i].get_line(st_pl_position = 3).t
            center_y = stiffener_list[i].get_center_y_tot()
            distance = abs(center_y-plate_a.a.y)
            stiffeners_ebp.insert(i, (distance, h, b_sup, b_inf, t_stiff))
        tau = V_Ed_plate / (t*h_w)
        sigma_E = 190000*(t/h_w)**2
        if abs(tau) > 0.1 and 3 <= t:
            k_tau = ebplate.ebplate_shear(a, h_w, t, tau, stiffeners_ebp) * tau / sigma_E
            line2 = "\n      k_tau: "+str(k_tau)

        elif t<3:
            eta_3 = 10**-2
            line2 = "\n      plate too thin; eta_3: "+ str(eta_3)
            return eta_3
        else:
            eta_3 = 1
            line2 = "\n      tau too small; eta_3: "+ str(1)
            return eta_3
        string = line1 + line2
        printing.printing(string, terminal = True)

    #pre_evaluation
    proof_required = True
    if stiffened == False:
        eval = 72 / eta * math.sqrt(235/f_y)
        if h_w/t < eval:
            proof_required = False
    else:
        eval = 31 / eta * math.sqrt(235 *k_tau/f_y)
        if h_w/t < eval:
            proof_required = False

    V_Rd = f_y*h_w*t/(math.sqrt(3)*gamma_M1)
    #calculate reduction factor chi_w if required
    if proof_required == True:
        #calculate tau_cr
        sigma_E = 190000*(t/h_w)**2
        print(k_tau)
        print(sigma_E)
        tau_cr = k_tau * sigma_E
        #can formula 5.6 be used here as well?
        #and what about formula 5.7? This needs to be considered as well...
        lambda_w_bar_1 = 0.76 * math.sqrt(f_y / tau_cr) # formula 5.3
        lambda_w_bar_2 = h_w /(37.4*t*math.sqrt(235/f_y)*math.sqrt(k_tau)) #formula 5.6
        lambda_w_bar = min(lambda_w_bar_1, lambda_w_bar_2)

        assert lambda_w_bar > 0, "Strange value for lambda_w_bar"
        #assume a deformable support stiffener
        #no resistance due to plastic hinges in flanges
        chi_w = 0
        if lambda_w_bar < 0.83/eta:
            chi_w = eta
        else:
            chi_w = 0.83/lambda_w_bar

        assert chi_w <= eta, "value for chi_w too high"
        #calculate resistance
        V_Rd = chi_w*f_y*h_w*t/(math.sqrt(3)*gamma_M1)

    eta_3 = V_Ed_plate / V_Rd

    string = "\n      eta_3: "+str(eta_3)
    printing.printing(string, terminal = True)

    return eta_3
