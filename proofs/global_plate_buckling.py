import math
import defaults
from proofs import stress_cal as stc
import ebplate
from classes import line as ln
from classes import crosssection as cs
from classes import point as pt
from output import geometry_output as go
import random
import data
import copy

def global_plate_buckling(total_cs, plate_glob):
    stiffened_plate = copy.deepcopy(plate_glob)
    #all methods still to be correctly implemented
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
        elif plate.code.st_number <= min_stn and plate.code.st_number != 0:
            min_stn = plate.code.st_number
        elif plate.code.st_number >= max_stn and plate.code.st_number != 0:
            max_stn = plate.code.st_number

    assert plate_a != None and plate_b != None, "For-Loop failed."

    sigma_a = stc.get_sigma_a(total_cs, plate_a, data.input_data.get("M_Ed"))
    sigma_b = stc.get_sigma_b(total_cs, plate_b, data.input_data.get("M_Ed"))
    psi = min(sigma_a, sigma_b) / max(sigma_a, sigma_b)

    if sigma_a <= 0 and sigma_b <= 0:
                rho_glob = 1
                sigma_cr_p = 10**10
    else:
        #get plate geometry
        h = 0
        for plate in stiffened_plate.lines:
            if plate.code.pl_type == 0:
                h += plate.get_length_tot()
                print("length: " + str(plate.get_length_tot()))
        t = plate_a.t
        print("t = " + str(t))
        b = defaults.plate_length

        #coordinate transformation (a+b)/2 is the new origin and baseplate is horizontal
        #set new origin
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

        #claculate A and I of stiffened plate
        A_tot = stiffened_plate.get_area_tot()

        #create a list of all stiffeners
        stiffener_list = []
        plate_num_list = []
        corresp_tpl = -2
        for st_number in range(min_stn, max_stn+1, 1):
            stiffener_list.insert(st_number - min_stn, cs.crosssection(0,0,0))
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
            for plate in stiffened_plate.lines:
                if plate.code.tpl_number == corresp_tpl and plate.code.pl_type == 0:
                    center_plate = plate
                if plate.code.tpl_number == corresp_tpl+1:
                    bottom_plate = plate
                elif plate.code.tpl_number == corresp_tpl-1:
                    top_plate = plate
            #find distance to point a
            delta_z = center_plate.get_center_z_tot() - plate_a.a.z
            delta_y = center_plate.get_center_y_tot() - plate_a.a.y
            distance = math.sqrt(delta_z **2 + delta_y **2)

            #calculate delta
            unit_vec_to_a = (top_plate.a.y - top_plate.b.y) / top_plate.get_length_tot()
            unit_vec_to_b = (bottom_plate.b.y - bottom_plate.a.y) / bottom_plate.get_length_tot()
            #find additional parts of top plate
            sigma_a_top = stc.get_sigma_a(total_cs, top_plate, data.input_data.get("M_Ed"))
            sigma_b_top = stc.get_sigma_b(total_cs, top_plate, data.input_data.get("M_Ed"))
            psi_top =  min(sigma_a_top, sigma_b_top) / max(sigma_a_top, sigma_b_top)
            length_top = 0
            if sigma_a_top > 0 or sigma_b_top > 0:
                #stiffener is at least partly in compression zone
                if sigma_a_top > sigma_b_top:
                    if psi_top > 0:
                        #low stress side
                        length_top = top_plate.get_length_tot()*(3-psi_top)/(5-psi_top)
                    else:
                        #tension zone
                        pass
                else:
                    if psi_top > 0:
                        #high stress side
                        length_top = top_plate.get_length_tot()*2/(5-psi_top)
                    else:
                        b_comp = top_plate.get_length_tot()/(1-psi_top)
                        length_top = 0.4*b_comp
                        pass
            else:
                #stiffener is in tension zone
                pass

            #find additional parts of bottom plate
            sigma_a_bottom = stc.get_sigma_a(total_cs, top_plate, data.input_data.get("M_Ed"))
            sigma_b_bottom = stc.get_sigma_b(total_cs, top_plate, data.input_data.get("M_Ed"))
            psi_bottom = min(sigma_a_bottom, sigma_b_bottom) / max(sigma_a_bottom, sigma_b_bottom)
            length_bottom = 0
            if sigma_a_bottom > 0 or sigma_b_bottom > 0:
                #stiffener is at least partly in compression zone
                if sigma_b_bottom > sigma_a_bottom:
                    if psi_bottom > 0:
                        #low stress side
                        length_bottom = bottom_plate.get_length_tot()*(3-psi_bottom)/(5-psi_bottom)
                    else:
                        #tension zone
                        pass
                else:
                    if psi_bottom > 0:
                        #high stress side
                        length_bottom = bottom_plate.get_length_tot()*2/(5-psi_bottom)
                    else:
                        b_comp = bottom_plate.get_length_tot()/(1-psi_bottom)
                        length_bottom = 0.4*b_comp
                        pass
            else:
                #stiffener is in tension zone
                pass

            #add additional parts of plate to stiffener
            new_top_point = pt.point(top_plate.b.y + unit_vec_to_a * length_top, top_plate.b.z)
            new_top_plate = ln.line(top_plate.code, new_top_point, top_plate.b, top_plate.t)
            new_bottom_point = pt.point(bottom_plate.a.y + unit_vec_to_b * length_bottom, bottom_plate.a.z)
            new_bottom_plate = ln.line(bottom_plate.code, bottom_plate.a, new_bottom_point, top_plate.t)
            stiffener.lines.append(new_top_plate)
            stiffener.lines.append(new_bottom_plate)

            delta = stiffener.get_area_tot()/A_tot


            #calculate gamma
            length_gamma = defaults.effective_width_parameter*center_plate.t
            if length_gamma > 0.5*center_plate.get_length_tot():
                new_top_plate.a = pt.point(new_top_plate.b.y + unit_vec_to_a*length_gamma, new_top_plate.b.z)
                new_bottom_plate.b = pt.point(new_bottom_plate.a.y + unit_vec_to_b*length_gamma, new_bottom_plate.a.z)
            else:
                stiffener.lines.remove(center_plate)
                new_top_plate.a = pt.point(new_top_plate.b.y + unit_vec_to_a*length_gamma, new_top_plate.b.z)
                new_top_plate.b = pt.point(new_top_plate.b.y + unit_vec_to_b*length_gamma, new_top_plate.b.z)
                new_bottom_plate.b = pt.point(new_bottom_plate.a.y + unit_vec_to_b*length_gamma, new_bottom_plate.a.z)
                new_bottom_plate.a = pt.point(new_bottom_plate.a.y + unit_vec_to_a*length_gamma, new_bottom_plate.a.z)

            gamma = stiffener.get_i_y_tot() * 12 * (1-0.3**2)/(h*t**3)

            #calculate theta
            #tbd
            theta = 1.0
            stiffeners_ebp.insert(i,(distance, gamma, theta, delta))

        #finding critical buckling load
        print(len(stiffeners_ebp))
        phi_cr_p = ebplate.ebplate(b,h,t,sigma_a, sigma_b, stiffeners_ebp)
        sigma_max = max(sigma_a, sigma_b)
        sigma_cr_p = sigma_max * phi_cr_p
        print("sigma_cr = " + str(sigma_cr_p))

        #calculating plate slenderness
        "correct beta_a_c still to be implemented"
        beta_a_c = 1
        lambda_p_glob_bar = math.sqrt(beta_a_c * data.constants.get("f_y") / sigma_cr_p)
        print("Lambda: " + str(lambda_p_glob_bar))
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
            print("plate slenderness or stress ratio out of range")
            pass

        print("Rho_Global: " + str(rho_glob))
    return rho_glob, sigma_cr_p
