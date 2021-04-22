import data
from classes import resistance_to_shear

def interaction_web(total_cs, web_plate, eta_3):
    m_f_rd = total_cs.get_m_f_rd_eff()
    if eta_3 <= 0.5 and m_ed < m_f_rd:
        #no interaction needed
        #what is a reasonable return value, -1?
        utilisation = -1
        return utilisation
    else:
        #interaction required
        m_pl_rd = total_cs.get_m_rd_pl_eff()
        eta_1 = m_ed / m_pl_rd
        utilisation = eta_1 + (1-m_f_rd/m_pl_rd)*(2*eta_3-1)^2
        return utilisation

def interaction_flange(total_cs, flange_plate):
    #choose correct shear stresses for calculation
    if eta_3 <= 0.5:
        #no interaction needed
        #what is a resonable return value, -1?
        utilisation = -1
    else:
        eta_1 = data.input_data.get("M_Ed") / toal_cs.get_m_rd_el_eff()
        utilisation = eta_1 + (2*eta_3-1)**2
    #prove shear resistance for each subpanel
    for plate in flange_plate.lines:
        if plate.code.tpl_number != 0:
            v_ed_panel = get_tau_int_subpanel(total_cs, plate, data.input_data.get("Q_Ed"),\
            data.input_data.get("T_Ed"))
            eta_3 = resistance_to_shear.resistance_to_shear(plate, v_ed_panel)
            if eta_3 < 1:
                print("pass subpanel")
            elif eta_3 > 1:
                print("fail subpanel")
            else:
                assert True, "This is not possible"
