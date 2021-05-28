import sys
import os
from fpdf import FPDF
from data_and_defaults import defaults
from output import geometry_output
from cs_optimization_tool import optimization_value
from cs_optimization_tool import cs_collector
from proofs_and_stress_calculation import buckling_proof

do_print_to_pdf = True
do_print_to_txt = True
do_print_to_terminal = True

#sys.path.append('C:/Users/Vinzenz Müller/Dropbox/ETH/6. Semester/BA')
#sys.path.append('C:/Users/Nino/Google Drive/Studium/FS 2021/Bachelorarbeit/BA')

"""
CONVENTION:
txt files in user_interface/output
png and single proofs from print_best_proof in user_interface/output/best_crosssections
cs_analysis_tool.pdf and all.pdf in user_interface/static
"""


def printing(string, terminal = False):
    if terminal == True and do_print_to_txt == True:
        file = open("user_interface\output\cs_analysis.txt", "a+")
        file.write(string)
        file.close()
    if terminal == True and do_print_to_terminal == True:
        print(string, end = "")



def txt_to_pdf(cs, name, location = None):
    # save FPDF() class into
    # a variable pdf
    pdf = PDF()

    # Add a page
    pdf.add_page()

    geometry_output.print_cs_to_png(cs, name, input = True, location = "user_interface/output/best_crosssections/")
    geometry_output.print_cs_to_png(cs, name, input = False, location = "user_interface/output/best_crosssections/")



    pdf.image("user_interface/output/best_crosssections/"+name+"_in.png", x = None, y = None, w = 200, h = 0, type = '', link = '')
    # set style and size of font
    # that you want in the pdf
    pdf.set_font("Arial", size = 10)
    pdf.set_fill_color(255, 0, 10)

    # open the text file in read mode
    txt_file = open("user_interface/output/cs_analysis.txt", "r")

    # insert the texts in pdf
    for line in txt_file:
        number_of_dots = 0
        for char in line:
            if char == ".":
                number_of_dots += 1

        #reading the lines and deciding on how to format them
        if line[0]!= " " and line != "\n":
            pdf.set_font("Arial", size = 12)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(180, 10, txt = line, border = 1, ln = 1, fill = True, align = 'C')
        elif number_of_dots == 0 and "Side" in line:
            pdf.cell(180, 10, txt = line, border = 1, ln = 1, fill = False, align = 'L')
        else:
            pdf.cell(200, 10, txt = line, border = 0, ln = 1, align = 'L')

    pdf.image("user_interface/output/best_crosssections/"+name+"_out.png", x = None, y = None, w = 200, h = 0, type = '', link = '')

    if location != None:
        pdf.output(location+str(name)+".pdf", "F")
    else:
        # save the pdf with name .pdf
        pdf.output("user_interface/static/"+str(name)+".pdf", "F")



def print_best_proof():
    #a function that prints a proof pdf per cs in best_crosssections
    #uses the txt_to_pdf function
    file = open("user_interface/output/cs_analysis.txt", "w+")
    file.close()
    do_print_to_txt = True
    i = 1
    for cs in cs_collector.get_best():
        cs.reset()
        name = "cs_"+str(i)


        cs = buckling_proof.buckling_proof(cs)

        ei = round(cs.get_ei() / 1000 / 1000 / 1000)
        cost = optimization_value.cost(cs)
        line1 = "\n\nResults:"
        line2 = "\n   EI: "+str(ei)+"kNm^2"
        line3 = "\n   interaction side 1: "+str(cs.interaction_1)
        line4 = "\n   interaction side 2: "+str(cs.interaction_2)
        line5 = "\n   interaction side 3: "+str(cs.interaction_3)
        line6 = "\n   interaction side 4: "+str(cs.interaction_4)
        line7 = "\n   eta_1: "+str(cs.eta_1)
        line8 = "\n   eta_3 side 1: "+str(cs.eta_3_side_1)
        line9 = "\n   eta_3 side 2: "+str(cs.eta_3_side_2)
        line10 = "\n   eta_3 side 3: "+str(cs.eta_3_side_3)
        line11 = "\n   eta_3 side 4: "+str(cs.eta_3_side_4)
        line12 = "\n   cost: "+str(cost)+"CHF/m"
        string = line1 + line2 + line3 + line4 + line5 + line6 + line7 + line8 + line9 + line10 + line11 + line12
        printing(string, terminal = True)

        geometry_output.print_cs_to_png(cs, name, input = False, location = "user_interface/output/best_crosssections/")
        geometry_output.print_cs_to_png(cs, name, input = True, location = "user_interface/output/best_crosssections/")
        txt_to_pdf(cs, name, location = "user_interface/output/best_crosssections/")






def print_best():

    file = open("user_interface/output/all.txt", "w+")
    file.close()
    i = 1
    file_name = "all"
    for cs in cs_collector.get_best():
        name = "cs_"+str(i)

        geometry_output.print_cs_to_png(cs, name, input = False, location = "user_interface/output/best_crosssections/")


        line1 = "\n"+name
        line2 = cs.print_cs_as_list()

        ei = round(cs.get_ei() / 1000 / 1000 / 1000)
        cost = optimization_value.cost(cs)
        line3 = "\n\nResults:"
        line4 = "\n   EI: "+str(ei)+"kNm^2"
        line5 = "\n   interaction side 1: "+str(cs.interaction_1)
        line6 = "\n   interaction side 2: "+str(cs.interaction_2)
        line7 = "\n   interaction side 3: "+str(cs.interaction_3)
        line8 = "\n   interaction side 4: "+str(cs.interaction_4)
        line9 = "\n   eta_1: "+str(cs.eta_1)
        line10 = "\n   eta_3 side 1: "+str(cs.eta_3_side_1)
        line11 = "\n   eta_3 side 2: "+str(cs.eta_3_side_2)
        line12 = "\n   eta_3 side 3: "+str(cs.eta_3_side_3)
        line13 = "\n   eta_3 side 4: "+str(cs.eta_3_side_4)
        line14 = "\n   cost: "+str(cost)+"CHF/m"
        string = line1 + line2 + line3 + line4 + line5 + line6 + line7 + line8 + line9 + line10 + line11 + line12 + line13 + line14

        file = open("user_interface/output/all.txt", "a+")
        file.write(string)
        file.close()
        i += 1

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 10)
    pdf.set_fill_color(255, 0, 10)
    txt_file = open("user_interface/output/all.txt", "r")
    # insert the texts in pdf
    i = 1
    for line in txt_file:
        number_of_dots = 0
        name = "cs_"+str(i)
        for char in line:
            if char == ".":
                number_of_dots += 1

        #reading the lines and deciding on how to format them
        if line[0]!= " " and line != "\n":
            pdf.set_font("Arial", size = 12)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(180, 10, txt = line, border = 1, ln = 1, fill = True, align = 'C')
        elif number_of_dots == 0 and "Side" in line:
            pdf.cell(180, 10, txt = line, border = 1, ln = 1, fill = False, align = 'L')
        else:
            pdf.cell(200, 10, txt = line, border = 0, ln = 1, align = 'L')
        if "cs_" in line:
            pdf.image("user_interface/output/best_crosssections/"+name+"_out.png", x = None, y = None, w = 200, h = 0, type = '', link = '')
            i += 1

    pdf.output("user_interface/static/all.pdf", "F")











class PDF(FPDF):
    def header(self):
        # Logo
        #self.image('logo_pb.png', 10, 8, 33)
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(30, 10, 'Title of the program', 0, 0, 'C')
        self.cell(50)
        self.set_font('Arial', 'B', 10)
        self.cell(30, 10, 'N. Hasler, V. Müller', 0, 0, 'R')
        # Line break
        self.ln(20)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')
