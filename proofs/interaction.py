import data
from proofs import resistance_to_shear
from proofs import stress_cal
from classes import crosssection
from classes import line
from classes import point
from classes import plate_code
from output import geometry_output
from output import printing
import data
import copy

def interaction_web(total_cs, web_plate, eta_3):
    line1 = "\n   7.1 Interaction between shear force, bending moment and axial force"
    line2 = "\n   Web -> (7.1) without iterating"
    string = line1 + line2
    printing.printing(string, terminal = True)

    m_ed = data.input_data.get("M_Ed")
    m_f_rd = total_cs.get_m_f_rd_eff()
    if eta_3 <= 0.5 and m_ed < m_f_rd:
        #no interaction needed
        #what is a reasonable return value, -1?
        utilisation = -1
        line1 = "\n      eta_3 <= 0.5; no interaction needed"
        line2 = "\n      utilisation: -1"
        string = line1 + line2
        printing.printing(string, terminal = True)

        return utilisation
    else:
        line1 = "\n      eta_3 > 0.5; interaction needed"
        #interaction required
        plastic_cs = copy.deepcopy(total_cs)
        m_pl_rd = get_m_rd_pl_eff(plastic_cs)
        eta_1 = m_ed / m_pl_rd
        utilisation = eta_1 + (1-m_f_rd/m_pl_rd)*(2*eta_3-1)**2
        line2 = "\n      utilisation: "+str(utilisation)
        printing.printing(string, terminal = True)
        return utilisation






def interaction_flange(total_cs, flange_plate, eta_3):
    line1 = "\n   7.1 Interaction between shear force, bending moment and axial force"
    line2 = "\n   Flange -> (7.1), comment (5)"
    string = line1 + line2
    printing.printing(string, terminal = True)


    #choose correct shear stresses for calculation
    if eta_3 <= 0.5:
        line1 = "\n      eta_3 <= 0.5; no interaction needed"
        #no interaction needed
        #what is a resonable return value, -1?
        utilisation = -1
        line2 = "\n      utilisation: -1"
        string = line1 + line2
    else:
        line1 = "\n      eta_3 > 0.5; interaction needed"
        eta_1 = abs(data.input_data.get("M_Ed") / total_cs.get_m_rd_el_eff())
        line2 = "\n      eta_1: "+str(eta_1)
        utilisation = eta_1 + (2*eta_3-1)**2
        line3 = "\n      utilisation: "+str(utilisation)
        string = line1 + line2 + line3
    printing.printing(string, terminal = True)

    #prove shear resistance for each subpanel
    string = "\n   Proofing Resistance to shear for each subpanel"
    printing.printing(string, terminal = True)
    for plate in flange_plate.lines:
        if plate.code.tpl_number != 0:
            v_ed_panel = stress_cal.get_tau_int_subpanel(total_cs, plate, data.input_data.get("V_Ed"),\
            data.input_data.get("T_Ed"))
            panel_cs = crosssection.crosssection(0,0,0)
            panel_cs.addline(plate)
            eta_3_panel = resistance_to_shear.resistance_to_shear(panel_cs, v_ed_panel)
            if eta_3_panel < 1:
                string = "\n      eta_3_panel < 1: pass subpanel"
                printing.printing(string, terminal = True)

            elif eta_3_panel > 1:
                string = "\n      eta_3_panel > 1: subpanel not passed"
                string += "\n      utilisation: 10"
                printing.printing(string, terminal = True)
                utilisation = 10
            else:
                assert True, "This is not possible"
    return utilisation

def get_m_rd_pl_eff(total_cs):
    #returns the value required in EC 1-5, section 7.1 interaction
    #attention: this value is very specific for this section
    #remove side stiffeners
    cs = crosssection.crosssection(total_cs.b_sup, total_cs.b_inf, total_cs.h)
    for plate in total_cs.lines:
        if (plate.code.pl_position == 2 or plate.code.pl_position == 4) and plate.code.pl_type == 1:
            pass
        else:
            cs.addline(plate)
    total_area = cs.get_area_red()
    convergence = 0.05* total_area
    continue_iteration = True
    area_top = 10**12
    area_btm = 0
    start = True
    z_min = 0
    z = cs.h / 2
    z_max = cs.h
    code = plate_code.plate_code(-1,-1,-1,-1,-1)
    counter = 0

    while abs(area_top - area_btm)>convergence and continue_iteration == True:
        counter += 1
        start = False
        top_part = crosssection.crosssection(0,0,0)
        bottom_part = crosssection.crosssection(0,0,0)
        for plate in cs.lines:
            #plate is entirely below assumed plastic zero line
            if plate.a.z >= z and plate.b.z >= z:
                bottom_part.addline(plate)
            #plate is entirely above plastic zero line
            elif plate.a.z <= z and plate.b.z <= z:
                top_part.addline(plate)
            #plate crosses plastic zero line, a on top
            elif plate.a.z <= z and plate.b.z >= z:
                #case 1: pzl crosses a-p1
                if plate.a.z < z and plate.p1.z > z:
                    share = (z-plate.a.z)/(plate.p1.z - plate.a.z)
                    y = plate.a.y + share * (plate.p1.y - plate.a.y)
                    point_middle = point.point(y,z)
                    line_a = line.line(code, plate.a, point_middle, plate.t)
                    top_part.addline(line_a)
                    line_b1 = line.line(code, point_middle, plate.p1, plate.t)
                    bottom_part.addline(line_b1)
                    line_b2 = line.line(code, plate.p2, plate.b, plate.t)
                    bottom_part.addline(line_b2)
                #case 2: pzl crosses p2-b
                elif plate.p2.z < z and plate.b.z > z:
                    share = (z-plate.p2.z)/(plate.b.z - plate.p2.z)
                    y = plate.p2.y + share * (plate.b.y - plate.p2.y)
                    point_middle = point.point(y,z)
                    line_a1 = line.line(code, plate.a, plate.p1, plate.t)
                    top_part.addline(line_a1)
                    line_a2 = line.line(code, plate.p2, point_middle, plate.t)
                    top_part.addline(line_a2)
                    line_b = line.line(code, point_middle, plate.b, plate.t)
                    bottom_part.addline(line_b)
                #case 3 pzl crosses p1-p2
                else:
                    line_a = line.line(code, plate.a, plate.p1, plate.t)
                    top_part.addline(line_a)
                    line_b = line.line(code, plate.p1, plate.b, plate.t)
                    bottom_part.addline(line_b)
            elif plate.a.z >= z and plate.b.z <= z:
                #case 1: pzl crosses b-p2
                if plate.b.z < z and plate.p2.z > z:
                    share = (z-plate.b.z)/(plate.p2.z - plate.b.z)
                    y = plate.b.y + share * (plate.p2.y - plate.b.y)
                    point_middle = point.point(y,z)
                    line_b = line.line(code, plate.b, point_middle, plate.t)
                    top_part.addline(line_b)
                    line_a1 = line.line(code, point_middle, plate.p2, plate.t)
                    bottom_part.addline(line_a1)
                    line_a2 = line.line(code, plate.p1, plate.a, plate.t)
                    bottom_part.addline(line_a2)
                #case 2: pzl crosses p1-a
                elif plate.p1.z < z and plate.a.z > z:
                    share = (z-plate.p1.z)/(plate.a.z - plate.p1.z)
                    y = plate.p1.y + share * (plate.a.y - plate.p1.y)
                    point_middle = point.point(y,z)
                    line_b1 = line.line(code, plate.b, plate.p2, plate.t)
                    top_part.addline(line_b1)
                    line_b2 = line.line(code, plate.p1, point_middle, plate.t)
                    top_part.addline(line_b2)
                    line_a = line.line(code, point_middle, plate.a, plate.t)
                    bottom_part.addline(line_a)
                #case 3 pzl crosses p1-p2
                else:
                    line_b = line.line(code, plate.b, plate.p2, plate.t)
                    top_part.addline(line_b)
                    line_a = line.line(code, plate.p2, plate.a, plate.t)
                    bottom_part.addline(line_a)
        area_top = top_part.get_area_red()
        area_btm = bottom_part.get_area_red()
        if area_top > area_btm:
            z_max = z
            z = 0.5*(z+z_min)
        else:
            z_min = z
            z = 0.5*(z+z_max)
        counter +=1
        if counter > 10:
            continue_iteration = False
    z_s_top = abs(z-top_part.get_center_z_red())
    z_s_btm = abs(z-bottom_part.get_center_z_red())
    m_pl_rd_eff = (z_s_top * area_top + z_s_btm * area_btm)*data.constants.get("f_y")
    return m_pl_rd_eff
