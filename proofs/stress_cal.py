def get_sigma_sup(cs, line, m_y):
    i_y = cs.get_i_y_tot()
    print(i_y)
    z_center = cs.get_center_z_tot()
    print(z_center)
    if line.a.z <= line.b.z:
        z_sup = line.a.z
    else:
        z_sup = line.b.z
    print(z_sup)
    print(m_y)
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
def get_tau_int(cs, line):
    return abs(get_tau_int_t() + get_tau_int_qy())

#shear stresses positive in counterclockwise direction
def get_tau_int_qy(cs, line, v_ed):
    tau_int = 0
    y_center = line.get_center_y_tot()
    sideplate_slope = (line.a.y - line.b.y)/(line.a.z - line.b.z)
    code = line.code.pl_position
    assert code > 0 and code < 5, "Invalid plate code"
    if code == 1 or code ==3:
        if y_center == 0:
            #assumption should be reconsidered
            tau_int = 0
        elif y_center > 0:
            tau_int = get_v_horizontal_plates(cs, line, v_ed)
        else:
            tau_int = -1*get_v_horizontal_plates(cs, line, v_ed)
    elif code == 2:
        tau_int = - v_ed / 2* math.cos(math.atan(sideplate_slope))
    elif code == 4:
        tau_int = v_ed / 2* math.cos(math.atan(sideplate_slope))

#shear stresses positive in counterclokwise direction
def get_tau_int_t(cs, line, tor):
    azero = cs.get_azero()
    t = line.t
    l = line.get_length_tot()
    tau = tor / (2*azero*t)
    tau_int = tau * l
    return tau_int

def get_v_horizontal_plates(cs, line, v_ed):
    sy_max = math.max(abs(line.a.y), abs(line.b.y))*line.t*abs(line.b.z - cs.get_center_z_tot())
    sy_min = math.min(abs(line.a.y), abs(line.b.y))*line.t*abs(line.b.z - cs.get_center_z_tot())
    v_max = 0.5*math.max(abs(line.a.y), abs(line.b.y))*v_ed*sy_max*cs.get_i_y_tot()
    v_min = 0.5*math.min(abs(line.a.y), abs(line.b.y))*v_ed*sy_min*cs.get_i_y_tot()
    tau_int = abs(v_max - v_min)
    return tau_int
