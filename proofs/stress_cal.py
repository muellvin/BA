#imports
import math

def get_sigma_a(cs, line, m_y):
    i_y = cs.get_i_y_tot()
    z_center = cs.get_center_z_tot()
    z = line.a.z
    sigma_a = m_y * (z-z_center) / i_y
    return sigma_a

def get_sigma_b(cs, line, m_y):
    i_y = cs.get_i_y_tot()
    z_center = cs.get_center_z_tot()
    z = line.b.z
    sigma_b = m_y * (z-z_center) / i_y
    return sigma_b

def get_sigma_a_red(cs, line, m_y):
    i_y = cs.get_i_y_red()
    z_center = cs.get_center_z_red()
    z = line.a.z
    sigma_a_red = m_y * (z-z_center) / i_y
    return sigma_a_red

def get_sigma_b_red(cs, line, m_y):
    i_y = cs.get_i_y_red()
    z_center = cs.get_center_z_red()
    z = line.b.z
    sigma_b_red = m_y * (z-z_center) / i_y
    return sigma_b_red


def get_sigma_sup(cs, line, m_y):
    i_y = cs.get_i_y_tot()
    z_center = cs.get_center_z_tot()
    if line.a.z <= line.b.z:
        z_sup = line.a.z
    else:
        z_sup = line.b.z
    sigma_sup = m_y * (z_sup-z_center) / i_y
    return sigma_sup

def get_sigma_inf(cs, line, m_y):
    i_y = cs.get_i_y_tot()
    z_center = cs.get_center_z_tot()
    if line.a.z >= line.b.z:
        z_inf = line.a.z
    else:
        z_inf = line.b.z
    sigma_inf = m_y / i_y * (z_inf-z_center)
    return sigma_inf

def get_sigma_sup_red(cs, line, m_y):
    i_y = cs.get_i_y_red()
    z_center = cs.get_center_z_red()
    if line.p1.z <= line.p2.z:
        z_sup = line.p1.z
    else:
        z_sup = line.p2.z
    sigma_sup_red = m_y / i_y * (z_sup-z_center)
    return sigma_sup_red

def get_sigma_inf_red(cs, line, m_y):
    i_y = cs.get_i_y_red()
    z_center = cs.get_center_z_red()
    if line.p1.z >= line.p2.z:
        z_inf = line.p1.z
    else:
        z_inf = line.p2.z
    sigma_inf_red = m_y / i_y * (z_inf-z_center)
    return sigma_inf_red

#returns the absolute value of the resulting shear force in a plate of the crosssection
def get_tau_int(cs, line, v_ed, t_ed):
    return abs(get_tau_int_t(cs, line, t_ed) + get_tau_int_qy(cs, line, v_ed))

#shear stresses positive in counterclockwise direction
def get_tau_int_qy(cs, line, v_ed):
    y_center = line.get_center_y_tot()
    if code.pl_position == 1 or code.pl_position ==3:
        if y_center == 0:
            #assumption should be reconsidered
            tau_int = 0
        elif y_center > 0:
            tau_int = get_v_horizontal_plates(cs, line, v_ed)
        else:
            tau_int = -1*get_v_horizontal_plates(cs, line, v_ed)
    elif code.pl_position == 2:
        sideplate_slope = (line.a.y - line.b.y)/(line.a.z - line.b.z)
        tau_int = - v_ed / (2* math.cos(math.atan(sideplate_slope)))
    elif code.pl_position == 4:
        sideplate_slope = (line.a.y - line.b.y)/(line.a.z - line.b.z)
        tau_int = v_ed / (2* math.cos(math.atan(sideplate_slope)))
    print("Tau_Q = " + str(tau_int))
    return tau_int

#shear stresses positive in counterclokwise direction
def get_tau_int_t(cs, line, tor):
    azero = cs.get_azero()
    l = line.get_length_tot()
    tau = tor / (2*azero)
    tau_int = tau * l
    print ("Tau_T = " + str(tau_int))
    return tau_int

def get_v_horizontal_plates(cs, line, v_ed):
    sy_max = math.max(abs(line.a.y), abs(line.b.y))*line.t*abs(line.b.z - cs.get_center_z_tot())
    sy_min = math.min(abs(line.a.y), abs(line.b.y))*line.t*abs(line.b.z - cs.get_center_z_tot())
    v_max = 0.5*math.max(abs(line.a.y), abs(line.b.y))*v_ed*sy_max*cs.get_i_y_tot()
    v_min = 0.5*math.min(abs(line.a.y), abs(line.b.y))*v_ed*sy_min*cs.get_i_y_tot()
    tau_int = abs(v_max - v_min)
    return tau_int
