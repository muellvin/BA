from proofs_and_stress_calculation import local_buckling
from proofs_and_stress_calculation import column_buckling
from proofs_and_stress_calculation import shear_lag
from proofs_and_stress_calculation import resistance_to_shear
from proofs_and_stress_calculation import global_buckling
from proofs_and_stress_calculation import interaction
from proofs_and_stress_calculation import stress_cal
from data_and_defaults import defaults
from data_and_defaults import data
from user_interface/output import printing




def buckling_proof(cs):
    string = "\n\nBuckling Proof according to EC 1993 Part 1-5"
    printing.printing(string, terminal = True)

    if defaults.do_shear_lag_plastically == False:

        #3.2 shear lag elastically
        string = "\n\n3.2 Effective width for elastic shear lag"
        printing.printing(string, terminal = True)
        if defaults.do_shear_lag == True:
            cs = shear_lag.shear_lag(cs)

        #4.4 plate elements without longitudinal stiffeners
        string = "\n\n4.4 Plate elements without longitudinal stiffeners"
        printing.printing(string, terminal = True)
        cs = local_buckling.local_buckling(cs)

        #4.5 stiffened plate elements with longitudinal stiffeners
        string = "\n\n4.5 Stiffened plate elements with longitudinal stiffeners"
        printing.printing(string, terminal = True)
        cs = global_buckling.global_buckling(cs)

        #4.6 verification
        string = "\n\n4.6 Verification"
        m_rd_eff = cs.get_m_rd_el_eff()
        cs.eta_1 = abs(data.input_data.get("M_Ed")/m_rd_eff)

        for side in range(1,5,1):
            line1 = "\n\nResistance to shear and interaction shear force and bending moment for side "+str(side)
            string = line1
            printing.printing(string, terminal = True)

            plate_glob = cs.get_stiffened_plate(side)
            if side == 1 or side == 3:

                #5. resistance to shear
                V_Ed_plate = stress_cal.get_tau_int_flange(cs, side, data.input_data.get("V_Ed"),\
                data.input_data.get("T_Ed"))
                eta_3 = resistance_to_shear.resistance_to_shear(plate_glob, V_Ed_plate)

                if side == 1:
                    #7.1 Interaction between shear forces, bending moment and axial force
                    line1 = "\n   7.1 Interaction between shear force, bending moment and axial force"
                    line2 = "\n      Deck plate is ignored, as it is dimensioned with EC 3-2"
                    string = line1 + line2
                    printing.printing(string, terminal = True)
                    pass

                if side == 3:
                    #7.1 Interaction between shear forces, bending moment and axial force
                    cs.interaction_3 = interaction.interaction_flange(cs, plate_glob, eta_3)


            if side == 2 or side == 4:

                #5. resistance to shear
                V_Ed_plate = stress_cal.get_tau_int_web(cs, side, data.input_data.get("V_Ed"),\
                data.input_data.get("T_Ed"))
                eta_3 = resistance_to_shear.resistance_to_shear(plate_glob, V_Ed_plate)

                if side == 2:
                    #7.1 Interaction between shear forces, bending moment and axial force
                    cs.interaction_2 = interaction.interaction_web(cs, plate_glob, eta_3)
                if side == 4:
                    #7.1 Interaction between shear forces, bending moment and axial force
                    cs.interaction_4 = interaction.interaction_web(cs, plate_glob, eta_3)


        return cs

    else:
        string = "\n\nShear Lag calculated plastically; iteratively"
        printing.printing(string, terminal = True)
        m_rd_eff_before = cs.get_m_rd_el_eff()
        m_rd_eff_after = 1
        iteration = 1
        convergence = (m_rd_eff_before / m_rd_eff_after - 1)

        while convergence > 0.05:
            line1 = "\nConvergence of M_Rd_eff: "+str(convergence)
            line2 = "\nIteration number "+str(iteration)
            string = line1 + line2
            printing.printing(string, terminal = True)
            iteration += 1
            m_rd_eff_before = cs.get_m_rd_el_eff()
            #reset the rho_c to 1: it is multiplied into the get_sigma_red functions
            #at this point the reduction should not happen yet
            for plate in cs.lines:
                plate.rho_c = 1

            #3.3 shear lag plastically
            string = "\n\n3.3 Shear lag at ultimate limit state"
            printing.printing(string, terminal = True)
            if defaults.do_shear_lag == True:
                for plate in cs.lines:
                    rho_c_a = 1
                    rho_c_b = 1
                cs = shear_lag.shear_lag(cs)

            #4.4 plate elements without longitudinal stiffeners
            string = "\n\n4.4 Plate elements without longitudinal stiffeners"
            printing.printing(string, terminal = True)
            cs = local_buckling.local_buckling(cs)

            #4.5 stiffened plate elements with longitudinal stiffeners
            string = "\n\n4.5 Stiffened plate elements with longitudinal stiffeners"
            printing.printing(string, terminal = True)
            cs = global_buckling.global_buckling(cs)

            #4.6 verification
            string = "\n\n4.6 Verification"
            m_rd_eff = cs.get_m_rd_el_eff()
            cs.eta_1 = abs(data.input_data.get("M_Ed")/m_rd_eff)

            for side in range(1,5,1):
                line1 = "\n\nResistance to shear and interaction shear force and bending moment for side "+str(side)
                string = line1
                printing.printing(string, terminal = True)

                plate_glob = cs.get_stiffened_plate(side)
                if side == 1 or side == 3:

                    #5. resistance to shear
                    V_Ed_plate = stress_cal.get_tau_int_flange(cs, side, data.input_data.get("V_Ed"),\
                    data.input_data.get("T_Ed"))
                    eta_3 = resistance_to_shear.resistance_to_shear(plate_glob, V_Ed_plate)

                    if side == 1:
                        #7.1 Interaction between shear forces, bending moment and axial force
                        line1 = "\n   7.1 Interaction between shear force, bending moment and axial force"
                        line2 = "\n      Deck plate is ignored, as it is dimensioned with EC 3-2"
                        string = line1 + line2
                        printing.printing(string, terminal = True)
                        pass

                    if side == 3:
                        #7.1 Interaction between shear forces, bending moment and axial force
                        cs.interaction_3 = interaction.interaction_flange(cs, plate_glob, eta_3)


                if side == 2 or side == 4:

                    #5. resistance to shear
                    V_Ed_plate = stress_cal.get_tau_int_web(cs, side, data.input_data.get("V_Ed"),\
                    data.input_data.get("T_Ed"))
                    eta_3 = resistance_to_shear.resistance_to_shear(plate_glob, V_Ed_plate)

                    if side == 2:
                        #7.1 Interaction between shear forces, bending moment and axial force
                        cs.interaction_2 = interaction.interaction_web(cs, plate_glob, eta_3)
                    if side == 4:
                        #7.1 Interaction between shear forces, bending moment and axial force
                        cs.interaction_4 = interaction.interaction_web(cs, plate_glob, eta_3)


            m_rd_eff_after = cs.get_m_rd_el_eff()
            convergence = (m_rd_eff_before / m_rd_eff_after - 1)

        return cs
