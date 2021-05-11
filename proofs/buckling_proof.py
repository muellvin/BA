#buckling proof
from proofs import local_buckling
from proofs import column_buckling
from proofs import shear_lag
from proofs import resistance_to_shear
from proofs import global_buckling
from proofs import interaction
import defaults
import data
from proofs import stress_cal
from output import printing



def buckling_proof(cs):
    if defaults.do_shear_lag_plastically == False:
        #3.2 shear lag elastically
        if defaults.do_shear_lag == True:
            cs = shear_lag.shear_lag(cs)
        #4.4 plate elements without longitudinal stiffeners
        cs = local_buckling.local_buckling(cs)
        #4.5 stiffened plate elements with longitudinal stiffeners
        cs = global_buckling.global_buckling(cs)
        #4.6 verification
        m_rd_eff = cs.get_m_rd_el_eff()
        cs.eta_1 = abs(data.input_data.get("M_Ed")/m_rd_eff)
        for side in range(1,5,1):
            #5. resistance to shear
            plate_glob = cs.get_stiffened_plate(side)
            #7.1 Interaction between shear forces, bending moment and axial force
            if side == 1 or side == 3:
                V_Ed_plate = stress_cal.get_tau_int_flange(cs, side, data.input_data.get("V_Ed"),\
                data.input_data.get("T_Ed"))
                eta_3 = resistance_to_shear.resistance_to_shear(plate_glob, V_Ed_plate)
                if side == 1:
                    pass
                if side == 3:
                    cs.interaction_3 = interaction.interaction_flange(cs, plate_glob, eta_3)
            if side == 2 or side == 4:
                V_Ed_plate = stress_cal.get_tau_int_web(cs, side, data.input_data.get("V_Ed"),\
                data.input_data.get("T_Ed"))
                eta_3 = resistance_to_shear.resistance_to_shear(plate_glob, V_Ed_plate)
                if side == 2:
                    cs.interaction_2 = interaction.interaction_web(cs, plate_glob, eta_3)
                if side == 4:
                    cs.interaction_4 = interaction.interaction_web(cs, plate_glob, eta_3)

        return cs

    else:
        m_rd_eff_before = cs.get_m_rd_el_eff()
        m_rd_eff_after = 1
        while (m_rd_eff_before / m_rd_eff_after - 1) > 0.05:
            m_rd_eff_before = cs.get_m_rd_el_eff()
            #3.2 shear lag elastically
            if defaults.do_shear_lag == True:
                cs = shear_lag.shear_lag(cs)
            #4.4 plate elements without longitudinal stiffeners
            cs = local_buckling.local_buckling(cs)
            #4.5 stiffened plate elements with longitudinal stiffeners
            cs = global_buckling.global_buckling(cs)
            #4.6 verification
            m_rd_eff = cs.get_m_rd_el_eff()
            cs.eta_1 = abs(data.input_data.get("M_Ed")/m_rd_eff)
            for side in range(1,5,1):
                #5. resistance to shear
                plate_glob = cs.get_stiffened_plate(side)
                #7.1 Interaction between shear forces, bending moment and axial force
                if side == 1 or side == 3:
                    V_Ed_plate = stress_cal.get_tau_int_flange(cs, side, data.input_data.get("V_Ed"),\
                    data.input_data.get("T_Ed"))
                    eta_3 = resistance_to_shear.resistance_to_shear(plate_glob, V_Ed_plate)
                    if side == 1:
                        pass
                    if side == 3:
                        cs.interaction_3 = interaction.interaction_flange(cs, plate_glob, eta_3)
                if side == 2 or side == 4:
                    V_Ed_plate = stress_cal.get_tau_int_web(cs, side, data.input_data.get("V_Ed"),\
                    data.input_data.get("T_Ed"))
                    eta_3 = resistance_to_shear.resistance_to_shear(plate_glob, V_Ed_plate)
                    if side == 2:
                        cs.interaction_2 = interaction.interaction_web(cs, plate_glob, eta_3)
                    if side == 4:
                        cs.interaction_4 = interaction.interaction_web(cs, plate_glob, eta_3)
            m_rd_eff_after = cs.get_m_rd_el_eff()

        return cs
