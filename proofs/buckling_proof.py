#buckling proof
from proofs import local_buckling
from proofs import column_buckling
from proofs import plate_global
from proofs import shear_lag
from proofs import resistance_to_shear
from proofs import global_buckling
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
        eta_1 = longitudinal_verification.longitudinal_verification(cs)
        #5. resistance to shear
        cs = resistance_to_shear.resistance_to_shear(cs)
        #5.5 verification
        eta_2 = shear_verification.shear_verification(cs)
        #7.1 Interaction between shear forces, bending moment and axial force
        utilisation = interaction.interaction(cs)
        return utilisation
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
