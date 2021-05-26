import math
import copy
import sys
sys.path.insert(0, './proofs_and_stress_calculation')
from proofs_and_stress_calculation import stress_cal
from ebplate_batch_mode import ebplate
from classes import line
from classes import crosssection
from classes import point
from data_and_defaults import data
from data_and_defaults import defaults
sys.path.insert(0, './user_interface')
from output import printing

def global_plate_buckling(total_cs, plate_glob):
    string = "\n      4.5.2 Plate type behaviour"
    printing.printing(string, terminal = True)


    stiffened_plate = copy.deepcopy(plate_glob)

    #identify the border plates a and b and numbers of end stiffeners
    plate_a = None
    plate_b = None
    min_tpl = -1
    max_tpl = -1
    max_stn = 0
    min_stn = 1000

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

    ### Get Stresses ###
    sigma_a = stress_cal.get_sigma_a_red(total_cs, plate_a, data.input_data.get("M_Ed"))
    sigma_b = stress_cal.get_sigma_b_red(total_cs, plate_b, data.input_data.get("M_Ed"))
    if abs(sigma_a) <= 0.1:
        sigma_a = sigma_a/abs(sigma_a)*0.1
    if abs(sigma_b) <= 0.1:
        sigma_b = sigma_b/abs(sigma_b)*0.1
    if abs(sigma_a) > 1000:
        sigma_a = sigma_a/abs(sigma_a)*1000
    if abs(sigma_b) > 1000:
        sigma_b = sigma_b/abs(sigma_b)*1000

    psi = min(sigma_a, sigma_b) / max(sigma_a, sigma_b)

    if sigma_a <= 0 and sigma_b <= 0:
        rho_glob = 1
        sigma_cr_p = 10**10
    ### Get Plate Geometry ###
    else:
        h = 0
        for plate in stiffened_plate.lines:
            if plate.code.pl_type == 0:
                h += plate.get_length_tot()
        t = plate_a.t
        b = data.input_data.get("a")

        #find borders of compression zone
        comp = None
        if sigma_a > 0 and sigma_b >0:
            comp = (0, h)
        elif sigma_a > 0 and sigma_b <= 0:
            h_red = h * sigma_a / (sigma_a - sigma_b)
            comp = (0, h_red)
        elif sigma_b > 0 and sigma_a <= 0:
            h_red = h * -sigma_a / (sigma_b - sigma_a)
            comp = (h_red, h)
        else:
            assert True, "This should never happen!"

        #coordinate transformation (a+b)/2 is the new origin and baseplate is horizontal
        #set new origin
        move_z = 0.5*(plate_a.a.z + plate_b.b.z)
        move_y = 0.5*(plate_a.a.y + plate_b.b.y)

        for plate in stiffened_plate.lines:
            plate.a.y -= move_y
            plate.a.z -= move_z
            plate.b.y -= move_y
            plate.b.z -= move_z
            plate.p1.y -= move_y
            plate.p1.z -= move_z
            plate.p2.y -= move_y
            plate.p2.z -= move_z

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
            p1y = plate.p1.y
            p1z = plate.p1.z
            p2y = plate.p2.y
            p2z = plate.p2.z
            plate.a.y = math.cos(angle)*ay - math.sin(angle)*az
            plate.a.z = math.sin(angle)*ay + math.cos(angle)*az
            plate.b.y = math.cos(angle)*by - math.sin(angle)*bz
            plate.b.z = math.sin(angle)*by + math.cos(angle)*bz
            plate.p1.y = math.cos(angle)*p1y - math.sin(angle)*p1z
            plate.p1.z = math.sin(angle)*p1y + math.cos(angle)*p1z
            plate.p2.y = math.cos(angle)*p2y - math.sin(angle)*p2z
            plate.p2.z = math.sin(angle)*p2y + math.cos(angle)*p2z

        #claculate A of stiffened plate
        A_tot = h*t

        #create a list of all stiffeners
        stiffener_list = []
        plate_num_list = []
        corresp_tpl = -2
        for st_number in range(min_stn, max_stn+1, 1):
            stiffener_list.insert(st_number - min_stn, crosssection.crosssection(0,0,0))
            #find three plates of stiffener
            for plate in stiffened_plate.lines:
                if plate.code.st_number == st_number:
                    stiffener_list[st_number - min_stn].addline(plate)
                    #find middle part of the trapezoid
                    if plate.code.tpl_number != 0:
                        corresp_tpl = plate.code.tpl_number
                        plate_num_list.insert(st_number - min_stn, corresp_tpl)
                    else:
                        corresp_tpl = -2
            #find adjacent parts of the trapezoid
            for plate in stiffened_plate.lines:
                if plate.code.tpl_number == corresp_tpl -1 or plate.code.tpl_number == corresp_tpl +1:
                    stiffener_list[st_number - min_stn].addline(plate)

        ###calculate adimensional parameters for each stiffener###
        stiffeners_ebp = []
        compression_stiffener = False
        for i in range(len(stiffener_list)):
            #extract the useful plates
            stiffener = stiffener_list[i]
            corresp_tpl = plate_num_list[i]
            center_plate = None
            top_plate = None
            top_plate_tpl = 0
            bottom_plate = None
            for plate in stiffened_plate.lines:
                if plate.code.tpl_number == corresp_tpl and plate.code.pl_type == 0:
                    center_plate = plate
                if plate.code.tpl_number == corresp_tpl+1:
                    bottom_plate = plate
                    bottom_plate_tpl = plate.code.tpl_number
                elif plate.code.tpl_number == corresp_tpl-1:
                    top_plate = plate
                    top_plate_tpl = plate.code.tpl_number
            #find distance to point a
            delta_z = center_plate.get_center_z_tot() - plate_a.a.z
            delta_y = center_plate.get_center_y_tot() - plate_a.a.y
            distance = math.sqrt(delta_z **2 + delta_y **2)

            #calculate theta
            b_sup_st = stiffener.get_line(st_pl_position = 1).get_length_tot()
            b_inf_st = stiffener.get_line(st_pl_position = 3).get_length_tot()
            t_st = stiffener.get_line(st_pl_position = 3).t
            diag = stiffener.get_line(st_pl_position = 2).get_length_tot()
            diff = (b_sup_st-b_inf_st)/2
            h_st = math.sqrt(diag**2 - diff**2)
            A_0 = 0.5*(b_sup_st + b_inf_st)*h_st
            integral = b_sup_st / t + (2*diag + b_inf_st) / t_st
            J_T = 4* A_0**2 / integral
            J_T_ref = 1/3 * h * t**3
            theta = J_T / J_T_ref


            #calculate delta
            unit_vec_to_a = (top_plate.a.y - top_plate.b.y) / top_plate.get_length_tot()
            unit_vec_to_b = (bottom_plate.b.y - bottom_plate.a.y) / bottom_plate.get_length_tot()
            #find additional parts of top plate
            top_original = total_cs.get_line(tpl_number = top_plate_tpl)
            sigma_a_top = stress_cal.get_sigma_a(total_cs, top_original, data.input_data.get("M_Ed"))
            sigma_b_top = stress_cal.get_sigma_b(total_cs, top_original, data.input_data.get("M_Ed"))
            psi_top =  min(sigma_a_top, sigma_b_top) / max(sigma_a_top, sigma_b_top)
            length_top = 0
            if sigma_b_top > 0:
                if sigma_a_top > 0:
                    if sigma_a_top < sigma_b_top:
                        #high stress side
                        length_top = top_plate.get_length_tot()*2/(5-psi_top)
                    else:
                        #low stress side
                        length_top = top_plate.get_length_tot()*(3-psi_top)/(5-psi_top)
                else:
                    #point a in tension zone
                    b_comp = top_plate.get_length_tot()/(1-psi_top)
                    length_top = 0.4*b_comp
            else:
                #tension zone
                pass

            #find additional parts of bottom plate
            bottom_original = total_cs.get_line(tpl_number = bottom_plate_tpl)
            sigma_a_bottom = stress_cal.get_sigma_a(total_cs, bottom_original, data.input_data.get("M_Ed"))
            sigma_b_bottom = stress_cal.get_sigma_b(total_cs, bottom_original, data.input_data.get("M_Ed"))
            psi_bottom = min(sigma_a_bottom, sigma_b_bottom) / max(sigma_a_bottom, sigma_b_bottom)
            length_bottom = 0
            if sigma_a_bottom > 0:
                if sigma_b_bottom > 0:
                    if sigma_b_bottom < sigma_a_bottom:
                        #high stress side
                        length_bottom = bottom_plate.get_length_tot()*2/(5-psi_bottom)
                    else:
                        #low stress side
                        length_bottom = bottom_plate.get_length_tot()*(3-psi_bottom)/(5-psi_bottom)
                else:
                    #point a in tension zone
                    b_comp = bottom_plate.get_length_tot()/(1-psi_bottom)
                    length_bottom = 0.4*b_comp

            else:
                #tension zone
                pass

            #add additional parts of plate to stiffener
            new_top_point = point.point(top_plate.b.y + unit_vec_to_a * length_top, top_plate.b.z)
            new_top_plate = line.line(top_plate.code, new_top_point, top_plate.b, top_plate.t)
            new_bottom_point = point.point(bottom_plate.a.y + unit_vec_to_b * length_bottom, bottom_plate.a.z)
            new_bottom_plate = line.line(bottom_plate.code, bottom_plate.a, new_bottom_point, top_plate.t)
            stiffener.lines.append(new_top_plate)
            stiffener.lines.append(new_bottom_plate)

            delta = stiffener.get_area_tot()/A_tot


            #calculate gamma
            length_gamma = defaults.effective_width_parameter*center_plate.t
            if length_gamma > 0.5*center_plate.get_length_tot():
                new_top_plate.a = point.point(new_top_plate.b.y + unit_vec_to_a*length_gamma, new_top_plate.b.z)
                new_bottom_plate.b = point.point(new_bottom_plate.a.y + unit_vec_to_b*length_gamma, new_bottom_plate.a.z)
            else:
                stiffener.lines.remove(center_plate)
                new_top_plate.a = point.point(new_top_plate.b.y + unit_vec_to_a*length_gamma, new_top_plate.b.z)
                new_top_plate.b = point.point(new_top_plate.b.y + unit_vec_to_b*length_gamma, new_top_plate.b.z)
                new_bottom_plate.b = point.point(new_bottom_plate.a.y + unit_vec_to_b*length_gamma, new_bottom_plate.a.z)
                new_bottom_plate.a = point.point(new_bottom_plate.a.y + unit_vec_to_a*length_gamma, new_bottom_plate.a.z)
            gamma = stiffener.get_i_y_tot() * 12 * (1-0.3**2)/(h*t**3)

        ### USE EBPlate ###
            #assure that there is at least on stiffener in compression zone
            if distance > comp[0] and distance < comp[1]:
                compression_stiffener = True

            if gamma > 1000:
                gamma = 1000
            if theta > 1000:
                theta = 1000
            if delta > 1000:
                delta = 1000
            assert gamma <= 1000 and gamma >= 0, "gamma too high or low"
            assert theta <= 1000 and theta >= 0, "theta too high or low"
            assert delta <= 1000 and delta >= 0, "theta too high or low"
            stiffeners_ebp.insert(i,(distance, gamma, theta, delta))

        assert t>= 3, "\nError: Plate too thin."
        if 100>b:
            b = 100
        if 100>h:
            h = 100
        #finding critical buckling load
        phi_cr_p = 0
        if compression_stiffener == True and abs(sigma_a) >= 0.1 and abs(sigma_a)<= 1000 and abs(sigma_b) >= 0.1 and abs(sigma_b)<= 1000 and 3<=t and 100<=b and 100<=h:
            phi_cr_p = ebplate.ebplate(b,h,t,sigma_a, sigma_b, stiffeners_ebp)

        elif compression_stiffener == False:
            string = "\nno compression stiffener"
            printing.printing(string)
            return 1, 0
        else:
            assert True, "Error: Calculation of phi_cr_p not possible."
        sigma_max = max(sigma_a, sigma_b)
        sigma_cr_p = sigma_max * phi_cr_p
        string = "\n         sigma_cr = " + str(sigma_cr_p)
        printing.printing(string, terminal = True)

        ### Calculation according to EC3, 1-5, 4.5.2 ###
        #calculating plate slenderness
        beta_a_c = get_beta_ac(plate_glob)
        lambda_p_glob_bar = math.sqrt(beta_a_c * data.constants.get("f_y") / sigma_cr_p)
        string = "\n         Lambda: " + str(lambda_p_glob_bar)
        printing.printing(string, terminal = True)

        #calculate rho_glob for plate buckling
        #assumption: cross section parts always supported on both sides
        rho_glob = 0
        #held on both sides
        if lambda_p_glob_bar <= 0.673:
            rho_glob = 1.0
        elif lambda_p_glob_bar > 0.673 and (3 + psi) >= 0:
            rho_glob = (lambda_p_glob_bar - 0.055 * (3 + psi)) / lambda_p_glob_bar**2
            if rho_glob > 1.0:
                rho_glob = 1.0
        else:
            string = "\n         plate slenderness or stress ratio out of range"
            printing.printing(string, terminal = True)
            pass

        string = "\n         Rho_Global: " + str(rho_glob)
        printing.printing(string, terminal = True)


    return rho_glob, sigma_cr_p

#function that returns beta_ac as requested by EC 3, 1-5, 4.5.2
def get_beta_ac(plate_glob):
    beta_plate = copy.deepcopy(plate_glob)
    side = beta_plate.lines[0].code.pl_position
    plate_a = beta_plate.get_plate_a(side)
    plate_b = beta_plate.get_plate_b(side)
    a_c = 0
    a_c_eff_loc = 0
    for plate in beta_plate.lines:
        if plate != plate_a and plate != plate_b:
            a_c += plate.get_area_tot(stress = True)
            a_c_eff_loc += plate.get_area_red(stress = True)
        else:
            a_c += 0.5*plate.get_area_tot(stress = True)
            a_c_eff_loc += 0.5*plate.get_area_red(stress = True)
    beta_a_c = a_c_eff_loc / a_c
    print(beta_a_c)
    return beta_a_c
