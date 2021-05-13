import sys
sys.path.append('C:/Users/Vinzenz Müller/Dropbox/ETH/6. Semester/BA')
import os
import defaults
import data
from output import cs_analysis.txt


from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size = 15)
pdf.cell(200,10,txt = "WHAAAT", ln = 1, align = 'C')
pdf.output("what.pdf")




"""
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
"""
