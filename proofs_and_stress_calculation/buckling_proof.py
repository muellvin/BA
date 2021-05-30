import sys
import math
from proofs_and_stress_calculation import local_buckling
from proofs_and_stress_calculation import column_buckling
from proofs_and_stress_calculation import shear_lag
from proofs_and_stress_calculation import resistance_to_shear
from proofs_and_stress_calculation import global_buckling
from proofs_and_stress_calculation import interaction
from proofs_and_stress_calculation import stress_cal
from data_and_defaults import defaults
from data_and_defaults import data
sys.path.insert(0, './user_interface')
from output import printing




def buckling_proof(cs):
    string = "\n\nBuckling Proof according to EC 1993 Part 1-5"
    printing.printing(string)

    #3.3 Shear lag at the ultimate limit state
    string = "\n\n3.3 Shear lag at the ultimate limit state"
    printing.printing(string)
    if defaults.do_shear_lag == True:
        cs = shear_lag.shear_lag(cs)


    if data.input_data.get("M_Ed") == 0:
        string = "\n\n4.6 Verification"
        printing.printing(string)
        cs.eta_1 = 0
        string = "\n         eta_1 = " + str(0)
        printing.printing(string)
    else:
        #4.4 plate elements without longitudinal stiffeners
        string = "\n\n4.4 Plate elements without longitudinal stiffeners"
        printing.printing(string)
        cs = local_buckling.local_buckling(cs)

        #4.5 stiffened plate elements with longitudinal stiffeners
        string = "\n\n4.5 Stiffened plate elements with longitudinal stiffeners"
        printing.printing(string)
        cs = global_buckling.global_buckling(cs)

        #4.6 verification
        m_rd_eff = cs.get_m_rd_el_eff()
        cs.eta_1 = abs(data.input_data.get("M_Ed")/m_rd_eff)
        string = "\n\n4.6 Verification"
        string += "\n      eta_1: "+str(math.floor(1000*abs(data.input_data.get("M_Ed")/m_rd_eff))/1000)
        printing.printing(string)


    for side in range(1,5,1):
        line1 = "\n\nResistance to shear and interaction shear force and bending moment for side "+str(side)
        string = line1
        printing.printing(string)

        plate_glob = cs.get_stiffened_plate(side)
        if side == 1 or side == 3:

            #5. resistance to shear
            V_Ed_plate = stress_cal.get_tau_int_flange(cs, side, data.input_data.get("V_Ed"),\
            data.input_data.get("T_Ed"))
            eta_3 = resistance_to_shear.resistance_to_shear(plate_glob, V_Ed_plate)

            if side == 1:
                cs.eta_3_side_1 = eta_3
                #7.1 Interaction between shear forces, bending moment and axial force
                cs.interaction_1 = interaction.interaction_flange(cs, plate_glob, eta_3)

            if side == 3:
                cs.eta_3_side_3 = eta_3
                #7.1 Interaction between shear forces, bending moment and axial force
                cs.interaction_3 = interaction.interaction_flange(cs, plate_glob, eta_3)


        if side == 2 or side == 4:

            #5. resistance to shear
            V_Ed_plate = stress_cal.get_tau_int_web(cs, side, data.input_data.get("V_Ed"),\
            data.input_data.get("T_Ed"))
            eta_3 = resistance_to_shear.resistance_to_shear(plate_glob, V_Ed_plate)

            if side == 2:
                cs.eta_3_side_2 = eta_3
                #7.1 Interaction between shear forces, bending moment and axial force
                cs.interaction_2 = interaction.interaction_web(cs, plate_glob, eta_3)
            if side == 4:
                cs.eta_3_side_4 = eta_3
                #7.1 Interaction between shear forces, bending moment and axial force
                cs.interaction_4 = interaction.interaction_web(cs, plate_glob, eta_3)


    return cs
