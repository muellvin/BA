#imports
import math

def get_sigma_a(cs, line, m_y):
    i_y = cs.get_i_y_tot()
    z_center = cs.get_center_z_tot()
    z = line.a.z
    sigma_a = - m_y * (z-z_center) / i_y
    return sigma_a

def get_sigma_b(cs, line, m_y):
    i_y = cs.get_i_y_tot()
    z_center = cs.get_center_z_tot()
    z = line.b.z
    sigma_b = -m_y * (z-z_center) / i_y
    return sigma_b

def get_sigma_a_red(cs, line, m_y):
    i_y = cs.get_i_y_red()
    z_center = cs.get_center_z_red()
    z = line.a.z
    sigma_a_red = -m_y * (z-z_center) / i_y
    return sigma_a_red

def get_sigma_b_red(cs, line, m_y):
    i_y = cs.get_i_y_red()
    z_center = cs.get_center_z_red()
    z = line.b.z
    sigma_b_red = -m_y * (z-z_center) / i_y
    return sigma_b_red


def get_sigma_sup(cs, line, m_y):
    i_y = cs.get_i_y_tot()
    z_center = cs.get_center_z_tot()
    if line.a.z <= line.b.z:
        z_sup = line.a.z
    else:
        z_sup = line.b.z
    sigma_sup = -m_y * (z_sup-z_center) / i_y
    return sigma_sup

def get_sigma_inf(cs, line, m_y):
    i_y = cs.get_i_y_tot()
    z_center = cs.get_center_z_tot()
    if line.a.z >= line.b.z:
        z_inf = line.a.z
    else:
        z_inf = line.b.z
    sigma_inf = -m_y / i_y * (z_inf-z_center)
    return sigma_inf

def get_sigma_sup_red(cs, line, m_y):
    i_y = cs.get_i_y_red()
    z_center = cs.get_center_z_red()
    if line.p1.z <= line.p2.z:
        z_sup = line.p1.z
    else:
        z_sup = line.p2.z
    sigma_sup_red = -m_y / i_y * (z_sup-z_center)
    return sigma_sup_red

def get_sigma_inf_red(cs, line, m_y):
    i_y = cs.get_i_y_red()
    z_center = cs.get_center_z_red()
    if line.p1.z >= line.p2.z:
        z_inf = line.p1.z
    else:
        z_inf = line.p2.z
    sigma_inf_red = -m_y / i_y * (z_inf-z_center)
    return sigma_inf_red

#returns the absolute value of the resulting shear force in a plate of the crosssection
def get_tau_int(cs, side, v_ed, t_ed):
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
            tau_int = - v_ed / (2* math.cos(math.atan(sideplate_slope)))
    return tau_int

#shear stresses positive in counterclokwise direction
def get_tau_int_t(cs, side, t_ed):
    azero = cs.get_azero()
    length = 0
    for plate in cs.lines:
        if plate.code.pl_type == 0 and plate.code.pl_position == side:
            length += plate.get_length_tot()
    tau = - t_ed / (2*azero)
    assert length != 0, "wrong cs dimensions"
    tau_int = tau * length
    return tau_int
