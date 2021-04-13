#initialisation

#this statement adds the project path to the path where the python interpreter looks
#for packages to import
#if we start the program from main, this should not be an issue
import sys
#just add the directory where the BA folder is on your computer
sys.path.append('C:/Users/Nino/Google Drive/Studium/FS 2021/Bachelorarbeit/BA')

import initial_cs as ics
from classes import crosssection as cs
from classes import plate_code as plcd

#assign input to variables
b_sup = 4000 #data.input_data["b_sup"]
b_inf = 2000 #data.input_data["b_inf"]
h = 1500 #data.input_data["h"]

#create initial cross section
test_cs = ics.create_initial_cs(b_sup, b_inf, h)
for line in test_cs.lines:
    line.t = 20

code = plcd.plate_code(2,0,0,0,0)
test_cs.get_line_code(code)
print(line.a.z, line.a.y)
