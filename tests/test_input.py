#initialisation

#this statement adds the project path to the path where the python interpreter looks
#for packages to import
#if we start the program from main, this should not be an issue
import sys
#just add the directory where the BA folder is on your computer
sys.path.append('C:/Users/Nino/Google Drive/Studium/FS 2021/Bachelorarbeit/BA')

#imports
import input.input
import data
import initial_cs as ics
from classes import crosssection as cs
from classes import line as ln
from proofs import stress_cal as str_cal

#assign input to variables
b_sup = data.input_data["b_sup"]
b_inf = data.input_data["b_inf"]
h = data.input_data["h"]

#create initial cross section
test_cs = ics.create_initial_cs(b_sup, b_inf, h)
for line in test_cs.lines:
    line.t = 20

#get geometry values of cross section
y_center = test_cs.get_center_y_tot()
print("y_center = " + str(y_center))
z_center = test_cs.get_center_z_tot()
print("z_center = " + str(z_center))
A = test_cs.get_area_tot()
print("Area = " + str(A))
I_y = test_cs.get_i_y_tot()
print("I_y = " + str(I_y))
I_z = test_cs.get_i_z_tot()
print("I_z = " + str(I_z))
A_0 = test_cs.get_azero()
print("A_0 = " + str(A_0))

#assign load input to variables
my = data.input_data["M_Ed"]

#testing of stresscal
test_line = 0
for line in test_cs.lines:
    if line.code.pl_position == 1:
        test_line = line
    else:
        pass
sigma_sup_test_cs = str_cal.get_sigma_sup(test_cs, test_line, my)
print("sigma_sup = " + str(sigma_sup_test_cs))
