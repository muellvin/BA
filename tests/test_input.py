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

#test code
b_sup = float(data.input_data["b_sup"])
b_inf = float(data.input_data["b_inf"])
h = float(data.input_data["h"])

#create initial cross section
test_cs = ics.create_initial_cs(b_sup, b_inf, h)

#get geometry values of cross section
y_center = test_cs.get_center_y_tot()
print("y_center = " + str(y_center))
z_center = test_cs.get_center_z_tot()
print("z_center =" + str(z_center))
A = test_cs.get_area_tot()
print("Area =" + str(A))
