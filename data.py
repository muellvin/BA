#list of constants
#if f_y is set to a value > 460 MPa also change eta in defaults.py
constants = {"E": 210000, "nu": 0.3, "f_y": 235, "G": 81000, "gamma_M1": 1.05}

#list of input
input_data = {}

stiffener_data = []

required_input_data = ["b_sup", "b_inf", "h", "M_Ed", "Q_Ed", "T_Ed", "a", "L_e", "bending type", "cs position"]
#a is the length of a local buckling field, ie distance between stiffeners in longitudinal direction
#L_e is the effective length of a continuous beam
#bending type should either be "sagging bending" or "hogging bending"
#cs position should either be "Cantilever", "end support" or "field"

def check_input_data_complete():
    complete = True
    missing = []
    for input in required_input_data:
        if input_data.get(input) == None:
            complete = False
            missing.append(input)
    for input in missing:
        print(input)
    assert complete == True, "The input_data dictionary is incomplete!"
