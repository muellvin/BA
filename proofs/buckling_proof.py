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


def buckling_proof(cs):
    if defaults.do_shear_lag_plastically == False:
        #3.2 shear lag elastically
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
            #interaction
            if side == 1 or side == 3:
                V_Ed_plate = stress_cal.get_tau_int_flange(cs, side, data.input_data.get("V_Ed"),\
                data.input_data.get("T_Ed"))
                eta_3 = resistance_to_shear.resistance_to_shear(plate_glob, V_Ed_plate)
                interaction.interaction_flange(cs, plate_glob, eta_3)
            if side == 2 or side == 4:
                V_Ed_plate = stress_cal.get_tau_int_web(cs, side, data.input_data.get("V_Ed"),\
                data.input_data.get("T_Ed"))
                eta_3 = resistance_to_shear.resistance_to_shear(plate_glob, V_Ed_plate)
                interaction.interaction_web(cs, plate_glob, eta_3)

            #7.1 Interaction between shear forces, bending moment and axial force
        return cs

    else:
        convergence = 1
        eta_0 = 1
        while convergence > defaults.convergence_limit_shear_lag:
            #3.2 shear lag elastically
            cs = shear_lag.shear_lag(cs)
            #4.4 plate elements without longitudinal stiffeners
            cs = local_buckling.local_buckling(cs)
            #4.5 stiffened plate elements with longitudinal stiffeners
            cs = global_buckling.global_buckling(cs)
            #4.6 verification
            eta_1 = longitudinal_verification.longitudinal_verification(cs)

            convergence = eta_1 / eta_0 - 1
            eta_0 = eta_1

        #5. resistance to shear
        cs = resistance_to_shear.resistance_to_shear(cs)
        #5.5 verification
        eta_2 = shear_verification.shear_verification(cs)
        #7.1 Interaction between shear forces, bending moment and axial force
        utilisation = interaction.interaction(cs)
        return utilisation
