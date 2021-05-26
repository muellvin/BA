#file with functions to calculate stresses
import math
import sys
sys.path.insert(0, './user_interface')
from output import printing

"""Calculate normal stresses for gross cross sections"""

def get_sigma_a(cs, line, m_y):
    stress = True
    i_y = cs.get_i_y_tot(stress)
    z_center = cs.get_center_z_tot(stress)
    z = line.a.z
    sigma_a = (-1)* m_y * (z-z_center) / i_y
    return sigma_a

def get_sigma_b(cs, line, m_y):
    stress = True
    i_y = cs.get_i_y_tot(stress)
    z_center = cs.get_center_z_tot(stress)
    z = line.b.z
    sigma_b = (-1)*m_y * (z-z_center) / i_y
    return sigma_b

"""Calculate normal Stresses For Effective Cross Sections"""

def get_sigma_a_red(cs, line, m_y):
    stress = True
    i_y = cs.get_i_y_red(stress)
    z_center = cs.get_center_z_red(stress)
    z = line.a.z
    sigma_a_red = (-1)*m_y * (z-z_center) / i_y
    return sigma_a_red

def get_sigma_b_red(cs, line, m_y):
    stress = True
    i_y = cs.get_i_y_red(stress)
    z_center = cs.get_center_z_red(stress)
    z = line.b.z
    sigma_b_red = (-1)*m_y * (z-z_center) / i_y
    return sigma_b_red

def get_sigma_p1_red(cs, line, m_y):
    stress = True
    i_y = cs.get_i_y_red(stress)
    z_center = cs.get_center_z_red(stress)
    z = line.p1.z
    sigma_a_red = (-1)*m_y * (z-z_center) / i_y
    return sigma_a_red

def get_sigma_p2_red(cs, line, m_y):
    stress = True
    i_y = cs.get_i_y_red(stress)
    z_center = cs.get_center_z_red(stress)
    z = line.p2.z
    sigma_b_red = (-1)*m_y * (z-z_center) / i_y
    return sigma_b_red


def get_sigma_sup(cs, line, m_y):
    stress = True
    i_y = cs.get_i_y_tot(stress)
    z_center = cs.get_center_z_tot(stress)
    if line.a.z <= line.b.z:
        z_sup = line.a.z
    else:
        z_sup = line.b.z
    sigma_sup = (-1)*m_y * (z_sup-z_center) / i_y
    return sigma_sup

def get_sigma_inf(cs, line, m_y):
    stress = True
    i_y = cs.get_i_y_tot(stress)
    z_center = cs.get_center_z_tot(stress)
    if line.a.z >= line.b.z:
        z_inf = line.a.z
    else:
        z_inf = line.b.z
    sigma_inf = (-1)*m_y / i_y * (z_inf-z_center)
    return sigma_inf

def get_sigma_sup_red(cs, line, m_y):
    stress = True
    i_y = cs.get_i_y_red(stress)
    z_center = cs.get_center_z_red(stress)
    if line.p1.z <= line.p2.z:
        z_sup = line.p1.z
    else:
        z_sup = line.p2.z
    sigma_sup_red = (-1)*m_y / i_y * (z_sup-z_center)
    return sigma_sup_red

def get_sigma_inf_red(cs, line, m_y):
    stress = True
    i_y = cs.get_i_y_red(stress)
    z_center = cs.get_center_z_red(stress)
    if line.p1.z >= line.p2.z:
        z_inf = line.p1.z
    else:
        z_inf = line.p2.z
    sigma_inf_red = (-1)*m_y / i_y * (z_inf-z_center)
    return sigma_inf_red


"""Calculate Shear Stresses due to Applied Shear Forces and Torsional Moments """

#returns the absolute value of the resulting shear force in a plate of the crosssection
def get_tau_int_web(cs, side, v_ed, t_ed):
    return abs(get_tau_int_t(cs, side, t_ed) + get_tau_int_qy(cs, side, v_ed))

#shear stresses positive in clockwise direction
def get_tau_int_qy(cs, side, v_ed):
    if side == 1 or side == 3:
        return 0
    elif side == 2 or side == 4:
        line = cs.get_line(pl_type = 0, pl_position = 2)
        sideplate_slope = (line.a.y - line.b.y)/(line.a.z - line.b.z)
        if side == 2:
            tau_int = v_ed / (2* math.cos(math.atan(sideplate_slope)))
        if side == 4:
            tau_int = (-1)*v_ed / (2* math.cos(math.atan(sideplate_slope)))
    return tau_int

#shear stresses positive in clokwise direction
def get_tau_int_t(cs, side, t_ed):
    stress = False
    azero = cs.get_azero(stress)
    length = 0
    for plate in cs.lines:
        if plate.code.pl_type == 0 and plate.code.pl_position == side:
            length += plate.get_length_tot(stress)
    tau = - t_ed / (2*azero)
    assert length != 0, "wrong cs dimensions"
    tau_int = tau * length
    return tau_int

#for S_y and I_y stress = False, come from moment equilibrium
def get_tau_int_flange(cs, side, v_ed, t_ed):
    stress = False
    area = 0
    t = cs.get_line(pl_position = side, pl_type = 0).t
    for plate in cs.lines:
        if plate.code.pl_type == 0 and plate.code.pl_position == side:
            area += plate.get_length_tot()*plate.t
    tau_int_t_flange = get_tau_int_t(cs, side, t_ed)
    #calculate exact shear stresses due to shear force
    if side == 1:
        b = cs.b_sup
    elif side == 3:
        b = cs.b_inf
    else:
        assert True, "This should never happen!"
    S_y_corner = 0.5*b*t*abs(cs.get_center_z_tot(stress)-cs.get_line(pl_position = side, pl_type = 0).a.z)
    tau_q_max_abs = abs(0.5*v_ed * S_y_corner /(t * cs.get_i_y_tot(stress)))
    tau_int_qy_flange = tau_q_max_abs * area * 0.5
    tau_int_flange = max(abs(tau_int_t_flange+tau_int_qy_flange), abs(tau_int_t_flange-tau_int_qy_flange))

    string = "\ntau_int_t_flange: "+str(math.floor(tau_int_t_flange*100)/100)
    string +="\ntau_int_qy_flange: "+str(math.floor(tau_int_qy_flange*100)/100)
    string +="\ntau_int_flange: "+str(math.floor(tau_int_flange*100)/100)
    printing.printing(string, terminal = True)
    return tau_int_flange

def get_tau_int_subpanel(cs, panel, v_ed, t_ed):
    stress = False
    #check if plate is flange plate
    assert panel.code.pl_position == 1 or panel.code.pl_position == 3, "ERROR!!"
    #calculate tau_mean from q
    center_of_panel = panel.get_center_y_tot(stress)
    if center_of_panel == 0:
        #plate where tau changes sign
        x = panel.get_length_tot(stress)/4
    else:
        x = abs(center_of_panel)
    S_y_panel = x*panel.t*abs(cs.get_center_z_tot(stress)-panel.a.z)
    tau_q_panel_abs = abs(v_ed * S_y_panel /(panel.t * cs.get_i_y_tot(stress)))
    tau_int_qy_panel = panel.get_area_tot(stress)*tau_q_panel_abs

    #calculate tau_mean from t
    side = panel.code.pl_position
    tau_int_t_flange = get_tau_int_t(cs, side, t_ed)
    tau_int_t_panel = 0
    if panel.code.pl_position == 1:
        tau_int_t_panel = panel.get_length_tot(stress)/cs.b_sup*tau_int_t_flange
    else:
        tau_int_t_panel = panel.get_length_tot(stress)/cs.b_inf*tau_int_t_flange
    tau_int_panel = max(abs(tau_int_t_panel+tau_int_qy_panel), abs(tau_int_t_panel-tau_int_qy_panel))
    return tau_int_panel
