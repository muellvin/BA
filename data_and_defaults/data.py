from data_and_defaults import defaults

sys_paths = {"vinz": 'C:/Users/Vinzenz Müller/Dropbox/ETH/6. Semester/BA', "nino": 'C:/Users/Nino/Google Drive/Studium/FS 2021/Bachelorarbeit/BA'}

#list of constants
#if f_y is set to a value > 460 MPa also change eta in defaults.py
constants = {"E": 210000, "nu": 0.3, "f_y": 235, "G": 81000, "gamma_M1": 1.05}

#list of input
input_data = {}

stiffener_data = None

cs_collection = []

def constants_tostring():
    string = "\nCONSTANTS"
    for key, value in constants.items():
        next_line = "\n    "+ str(key) +": " +str(value)
        string += next_line
    return string


def input_data_tostring():
    string = "\nINPUT DATA"
    for key, value in input_data.items():
        next_line = "\n    "+ str(key) +": " +str(value)
        string += next_line
    return string
