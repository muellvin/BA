#initialisation

#this statement adds the project path to the path where the python interpreter looks
#for packages to import
#it is also possible to add this to the environment variable PYTHONPATH in the windows settings
#as far as I understand this needs to be done individually for each user, because the documents variable
#saved on differen paths...
#this could be a big issue for distribution...
#However it makes our inputs work :-)
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
