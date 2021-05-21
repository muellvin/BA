import math
from data_and_defaults import data
from data_and_defaults import defaults
from user_interface/output import printing


#EC 1993 1-5 3.3 shear lag at ULS
#3.3 (3): A_eff can be calculated from A_c_eff (width from plate buckling 4.4 and 4.5)
#and the values beta and kappa from table 3.1

#in the book design of plated structures: equation 2.8

def shear_lag(cs):

    #the top flange is pl_position 1
    #the bottom flange is pl_position 3
    cs = reduction_shear_lag(cs, 1)
    cs = reduction_shear_lag(cs, 3)

    return cs



def reduction_shear_lag(cs, flange):
    string = "\n   Shear lag reduction for flange "+str(flange)
    printing.printing(string, terminal = True)

    if flange == 1:
        b_0 = cs.b_sup / 2 #3.1 (2)
    elif flange == 3:
        b_0 = cs.b_inf / 2

    #check if necessary
    if b_0 < data.input_data.get("L_e")/50:
        string = "\n      Shear Lag is neglectable"
        printing.printing(string, terminal = True)
        return cs

    string = "\n      Shear Lag is not neglectable"
    printing.printing(string, terminal = True)

    A_c_eff = 0
    for line in cs.lines:
        if line.code.pl_position == flange:
            #if the side is under tension, A_c_eff is the gross cross-sectional area as said in last remark in the EC after eq 3.5
            A_c_eff += line.get_area_red()
    A_sl = 0
    for line in cs.lines:
        if line.code.pl_position == flange and line.code.pl_type == 1:
            A_sl += line.get_area_tot()

    t_f = t = cs.get_line(pl_position = flange, pl_type = 0).t
    alpha_0_star = math.sqrt(A_c_eff / (b_0 * t_f))
    alpha_0 = math.sqrt(1 + A_sl / (b_0*t))



    if defaults.do_shear_lag_plastically == True:
        kappa = alpha_0_star * b_0 / data.input_data.get("L_e")

        beta_ult = beta_from_kappa(kappa)
        string = "\n      alpha_0_star: "+str(round(10*alpha_0_star)/10)
        string += "\n      Beta_ult: "+str(beta_ult)
        printing.printing(string, terminal = True)
        #follow EC 3.3; plastically
        #recommended calculation from book design of plated structures (2.8):
            #also in EC 1993 1-5 3.3 eq 3.5
            #A_eff = beta**kappa * A_c_eff
        #here doing 3.3: A_eff = Ac_eff * beta_ult
        reduction_factor_shear_lag = beta_ult**kappa
    else:
        string = "\n      alpha_0: "+str(round(10*alpha_0)/10)
        kappa = alpha_0 * b_0 / data.input_data.get("L_e")

        beta = beta_from_kappa(kappa)

        string += "\n      Beta: "+str(beta)
        printing.printing(string, terminal = True)
        #follow EC 3.2; elastically; conservative, no iterations needed
        reduction_factor_shear_lag = beta


    #the book recommends to apply this reduction to the thickness of the flange plates
    for line in cs.lines:
        if line.code.pl_position == flange:
            line.t_stress = line.t * reduction_factor_shear_lag

    return cs








#table 3.1
def beta_from_kappa(kappa):
    #calculation of beta
    #beta_0: end support
    #beta_1: sagging bending
    #beta_2: hogging bending (and also cantilever at support and at the end)
    beta = 0
    if kappa <= 0.02:
        beta = 1.0
    elif 0.02 < kappa <= 0.7:
        if data.input_data.get("bending type") == "sagging bending":
            beta_1 = 1 / (1 + 6.4 * kappa**2)
            beta = beta_1
        elif data.input_data.get("bending type") == "hogging bending":
            beta = beta_2 = 1 / (1 + 6.0 * (kappa - 1 / (2500 * kappa) + 1.6 * kappa**2))
        else:
            print("bending type is not defined")
    elif 0.7 < kappa:
        if data.input_data.get("bending type") == "sagging bending":
            beta = beta_1 = 1 / (5.9 * kappa)
        elif data.input_data.get("bending type") == "hogging bending":
            beta = beta_2 = 1 / (8.6 * kappa)
        else:
            print("bending type is not defined")

    if data.input_data.get("cs position") == "end support":
        beta = beta_0 = (0.55 + 0.025 / kappa) * beta_1
        if beta_0 >= beta_1:
            beta = beta_0 = beta_1
    elif data.input_data.get("cs position") == "Cantilever":
        beta = beta_2
    #if no cs position is given, it is a sagging or bending moment inbetween the ends of the bridge
    #thus no else clause

    return beta
