import defaults

sys_paths = {"vinz": 'C:/Users/Vinzenz Müller/Dropbox/ETH/6. Semester/BA', "nino": 'C:/Users/Nino/Google Drive/Studium/FS 2021/Bachelorarbeit/BA'}

#list of constants
#if f_y is set to a value > 460 MPa also change eta in defaults.py
constants = {"E": 210000, "nu": 0.3, "f_y": 235, "G": 81000, "gamma_M1": 1.05}

#list of input
input_data = {}

stiffener_data = None

cs_collection = []

def print_constants():
    if defaults.do_print_to_txt == True:
        file = open("output\cs_analysis.txt", "a+")
        file.write("\nCONSTANTS")
        for key, value in constants.items():
            string = "\n    "+ str(key) +": " +str(value)
            file.write(string)
        file.close()
    if defaults.do_print_to_terminal == True:
        print("CONSTANTS")
        for key, value in constants.items():
            string = "  "+str(key) +": " +str(value)
            print(string)

def print_input_data():
    if defaults.do_print_to_txt == True:
        file = open("output\cs_analysis.txt", "a+")
        file.write("\nINPUT DATA")
        for key, value in input_data.items():
            string = "\n    "+ str(key) +": " +str(value)
            file.write(string)
        file.close()
    if defaults.do_print_to_terminal == True:
        print("INPUT DATA")
        for key, value in input_data.items():
            string = "  "+str(key) +": " +str(value)
            print(string)
