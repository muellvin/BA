def interaction_web():
    m_f_rd = 10**20
    if eta_3 <= 0.5 and m_ed < m_f_rd:
        #no interaction needed
        #what is a reasonable return value
        utilisation = 0
        return utilisation
    else:
        #interaction required
        m_pl_rd = 10**20
        eta_1 = m_ed / m_pl_rd
        utilisation = eta_1 + (1-m_f_rd/m_pl_rd)*(2*eta_3-1)^2
        return utilisation

def interaction_flange():
    #choose correct shear stresses for calculation 
    if eta_3 <= 0.5:
        #no interaction needed
        #what is a resonable return value
        utilisation = 0
    else:
        eta_1 = m_ed / m_rd_el_eff
        utilisation = eta_1 + (2*eta_3-1)^2

    #prove shear resistance for each subpanel
    #tbd
