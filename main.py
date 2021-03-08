#imports
import input_data as id
import cs_generator as cs_gen
import stress_cal as str_cal

#initialize input container
data = id.input_data()
data.initialize_constants()

#option 1: input from user prompt
data.userprompt()

#option 2: input from standard test cases

#create inital crossection using information from user input
x = cs_gen.create_initial_cs(data.data["b_sup"], data.data["b_inf"], data.data["h"])

#perform example stress calculations (to be deleted afterwards)
sigma_test = str_cal.get_sigma_inf(x, x.lines[0], data.data["M_Ed"])
print(sigma_test)
#perform buckling proof for initial crossection

#check if initial crosssection passes buckling proof
    # if it passes --> output
    # else (should be the case for each reasonable crosssection) --> start optimizer

#return best crossection
