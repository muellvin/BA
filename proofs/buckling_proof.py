#buckling proof
from proofs import local_buckling
from proofs import column_buckling
from proofs import plate_global
from proofs import shear_lag
from proofs import resistance_to_shear
from proofs import global_buckling
from proofs import verification
from proofs import interaction
import defaults


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
        for side in range(1,5,1):
            #5. resistance to shear
            plate_glob = cs.get_stiffened_plate(side)
            eta_3 = resistance_to_shear.resistance_to_shear(total_cs, plate_glob)
            if side == 1 or side == 3:
                interaction.interaction_flange()
            if side == 2 or side == 4:
                interaction.interaction_web()
            
            #7.1 Interaction between shear forces, bending moment and axial force
        return report

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
