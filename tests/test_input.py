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

#test code
x = data.input_data["b_sup"]
print(x)
y = data.input_data["h"]
print(y)
z = data.constants["E"]
print(z)
