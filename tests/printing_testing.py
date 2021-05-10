import sys
sys.path.append('C:/Users/Vinzenz Müller/Dropbox/ETH/6. Semester/BA')
import os
import defaults
import data


def print_():
    if defaults.do_print_to_txt == True:
        file = open("output\cs_analysis.txt", "a+")
        file.write(string)
        file.close()
    if defaults.do_print_to_terminal == True:
        print(string, end = "")

file = open("output\cs_analysis.txt", "a+")
file.write("\nCONSTANTS")
for key, value in data.constants.items():
    string = "\n"+ str(key) +": " +str(value)
    file.write(string)
file.close()
