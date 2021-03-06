def get_sigma_sup(cs, line):
    m_y = datenbank.m_y
    i_y = cs.get_i_y()
    if line.a.z <= line.b.z:
        z_sup = line.a.z
    else:
        z_sup = line.b.z
    sigma_sup = m_y / i_y * z_sup
    return sigma_sup

def get_sigma_inf(cs, line):
    m_y = datenbank.m_y
    i_y = cs.get_i_y()
    if line.a.z >= line.b.z:
        z_inf = line.a.z
    else:
        z_inf = line.b.z
    sigma_inf = m_y / i_y * z_inf
    return sigma_inf

def get_sigma_sup_red(cs, line):
    m_y = datenbank.m_y
    i_y = cs.get_i_y()
    if line.p1.z <= line.p2.z:
        z_sup = line.p1.z
    else:
        z_sup = line.p2.z
    sigma_sup_red = m_y / i_y * z_sup
    return sigma_sup_red

def get_sigma_inf_red(cs, line):
    m_y = datenbank.m_y
    i_y = cs.get_i_y()
    if line.p1.z >= line.p2.z:
        z_inf = line.p1.z
    else:
        z_inf = line.p2.z
    sigma_inf_red = m_y / i_y * z_inf
    return sigma_inf_red

def get_tau_int_t(cs, line):
