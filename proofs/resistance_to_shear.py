import defaults
import math
import data

def resistance_to_shear(stiffened_cs):
    #get values of constants
    f_y = data.input_data.get("f_y")
    gamma_M1 = data.input_data.get("gamma_M1")
    eta = defaults.eta

    #proof for all plates
    for line in initial_cs.lines:
        #import important geometry parameters
        h_w = line.get_length_tot
        t = line.t

        #is plate stiffened?
        #this method need to be implemented
        stiffened = True
        #calculate k_tau
        #still needs to be implemented
        k_tau = 5
        #pre_evaluation
        proof_required = True
        if stiffened == False:
            eval = 72 / eta * math.sqrt(235/f_y))
            if h_w/t < eval:
                proof_required = False
        else:
            eval = 31 / eta * math.sqrt(235 *k_tau/f_y)
            if h_w/t < eval:
                proof_required = False

        #Does V_Rd have to be multiplied with eta? --> rather not, but I'm not sure...
        V_Rd = f_y*h_w*t/(math.sqrt(3)*gamma_M1)
        #calculate reduction factor chi_w if required
        if proof_required = True:
            #calculate tau_cr
            sigma_E = 190000*(t/h_w)**2
            tau_cr = k_tau * sigma_E
            #can formula 5.6 be used here as well?
            #and what about formula 5.7? This needs to be considered as well...
            lambda_w_bar_1 = 0.76 * math.sqrt(f_y / tau_cr) # formula 5.3
            lambda_w_bar_2 = h_w /(37.4*t*math.sqrt(235/f_y)*math.sqrt(k_tau)) #formula 5.6
            lambda_w_bar = min(lambda_w_bar_1, lambda_w_bar_2)

            assert lambda_w_bar > 0, "Strange value for lambda_w_bar"
            #assume a deformable support stiffener
            #no resistance due to plastic hinges in flanges
            chi_w = 0
            if lambda_w_bar < 0.83/eta:
                chi_w = eta
            else:
                chi_w = 0.83/lambda_w_bar

            assert chi_w < eta, "value for chi_w too high"
            #calculate resistance
            V_Rd = chi_w*f_y*h_w*t/(math.sqrt(3)*gamma_M1)
