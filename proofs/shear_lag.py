import math
import data


#EC 1993 1-5 3.3 shear lag at ULS
#3.3 (3): A_eff can be calculated from A_c_eff (width from plate buckling 4.4 and 4.5)
#and the values beta and kappa from table 3.1
#for ULS the value alpha_0 is replaced by alpha_0*

#in the book design of plated structures: equation 2.8

def shear_lag(cs):
    #the top flange is pl_position 1
    #the bottom flange is pl_position 3
    reduction_shear_lag(1)
    reduction_shear_lag(3)


def reduction_shear_lag(cs, flange):

    #calculation of alpha_0*
    A_c_eff = 0
    for line in cs.lines:
        if line.code.pl_position == flange:
            A_c_eff += line.get_area_red()

    if flange == 1:
        b_0 = cs.b_sup / 2 #3.1 (2)
    elif flange == 3:
        b_0 = cs.b_inf / 2

    t_f = cs.get_pl_line(flange).t

    alpha_0_star = math.sqrt(A_c_eff / (b_0 * t_f))

    kappa = alpha_0_star * b_0 / data.input_data.get("L_e")

    beta = beta_from_kappa(kappa)

    #recommended calculation from book design of plated structures (2.8)
    #also in EC 1993 1-5 3.3 eq 3.5
    A_eff = beta**kappa * A_c_eff
    reduction_factor_shear_lag = beta**kappa

    #the book recommends to apply this reduction to the thickness of the flange plates
    for line in cs.lines:
        if line.code.pl_position == flange:
            line.t = line.t * reduction_factor_shear_lag




#table 3.1
def beta_from_kappa(kappa):
    #calculation of beta
    #beta_0: end support
    #beta_1: sagging bending
    #beta_2: hogging bending (and also cantilever at support and at the end)
    if kappa <= 0.02:
        beta = 1.0
    elif 0.02 < kappa <= 0.7:
        if data.input_data.get("bending type") == "sagging bending":
            beta = beta_1 = 1 / (1 + 6.4 * kappa**2)
        elif data.input_data.get("bending type") == "hogging bending":
            beta = beta_2 = 1 / (1 + 6.0 * (kappa - 1 / (2500 * kappa) + 1.6 * kappa**2)
        else:
            print("bending type is not defined")
            pass
    elif 0.7 < kappa:
        if data.input_data.get("bending type") == "sagging bending":
            beta = beta_1 = 1 / (5.9 * kappa)
        elif data.input_data.get("bending type") == "hogging bending":
            beta = beta_2 = 1 / (8.6 * kappa)
    if data.input_data.get("cs position") == "end support":
        beta = beta_0 = (0.55 + 0.025 / kappa) * beta_1
        if beta_0 >= beta_1:
            beta = beta_0 = beta_1
    elif data.input_data.get("cs position") == "cantilever":
        beta = beta_2
    #if no cs position is given, it is a sagging or bending moment inbetween the ends of the bridge
    #thus no else clause
