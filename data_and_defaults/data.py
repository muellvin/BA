from data_and_defaults import defaults

#list of constants
#if f_y is set to a value > 460 MPa also change eta in defaults.py
constants = {"E": 210000, "nu": 0.3, "f_y": 235, "G": 81000, "gamma_M1": 1.05}

#list of input
input_data = {}

#list of stiffener input data
stiffener_data = None

#list where all cross sections that passed are stored
cs_collection = []

#print function
def constants_tostring():
    string = "\nCONSTANTS"
    for key, value in constants.items():
        next_line = "\n    "+ str(key) +": " +str(value)
        string += next_line
    return string

#print function 
def input_data_tostring():
    string = "\nINPUT DATA"
    for key, value in input_data.items():
        next_line = "\n    "+ str(key) +": " +str(value)
        string += next_line
    return string
