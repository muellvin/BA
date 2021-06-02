import sys
import os
import math
from fpdf import FPDF
from data_and_defaults import defaults
from output import geometry_output
from cs_optimization_tool import optimization_value
from cs_optimization_tool import cs_collector
from proofs_and_stress_calculation import buckling_proof

do_print_to_pdf = True
do_print_to_txt = True
do_print_to_terminal = True


"""
CONVENTION:
txt files in user_interface/output
png and single proofs from print_best_proof in user_interface/output/best_crosssections
cs_analysis_tool.pdf and all.pdf in user_interface/static
"""






#print to cs_analysis.txt and terminal
def printing(string):
    if do_print_to_txt == True:
        file = open("user_interface\output\cs_analysis.txt", "a+")
        file.write(string)
        file.close()
    if do_print_to_terminal == True:
        print(string, end = "")






#turn the cs_analysis.txt into a pdf
def txt_to_pdf(cs, name, location = None):

    geometry_output.print_cs_to_png(cs, name, input = True, location = "user_interface/output/images/")
    geometry_output.print_cs_to_png(cs, name, input = False, location = "user_interface/output/images/")

    pdf = PDF()
    pdf.add_page()

    # Title
    pdf.set_font('Arial', 'B', 15)
    pdf.cell(45) # Move to the right
    pdf.cell(100, 10, "Cross-Section Analysis Tool", border = 0, ln = 1, align = 'C')

    #cs image
    pdf.image("user_interface/output/images/"+name+"_out.png", x = None, y = None, w = 200, h = 0, type = '', link = '')

    pdf.set_font("Arial", size = 12)
    pdf.set_fill_color(255, 0, 10)

    string = "      EI (with reductions): "+str(math.floor(100*cs.get_ei()/1000/1000/1000)/100)+"kNm^2"
    pdf.cell(190, 10, txt = string, border = 0, ln = 1, fill = False, align = 'L')
    string = "      Center from top (with reductions): "+str(math.floor(100*cs.get_center_z_red(stress = True))/100)+"mm"
    pdf.cell(190, 10, txt = string, border = 0, ln = 1, fill = False, align = 'L')

    string = "      eta_1: "+str(math.floor(100*cs.eta_1)/100)
    pdf.cell(190, 10, txt = string, border = 0, ln = 1, fill = False, align = 'L')

    string = "      deck               eta_3: "+str(math.floor(100*cs.eta_3_side_1)/100) + "   interaction: "+str(math.floor(100*cs.interaction_1)/100)
    pdf.cell(190, 10, txt = string, border = 0, ln = 1, fill = False, align = 'L')
    string = "      right web        eta_3: "+str(math.floor(100*cs.eta_3_side_2)/100) + "   interaction: "+str(math.floor(100*cs.interaction_2)/100)
    pdf.cell(190, 10, txt = string, border = 0, ln = 1, fill = False, align = 'L')
    string = "      bottom plate   eta_3: "+str(math.floor(100*cs.eta_3_side_3)/100) + "   interaction: "+str(math.floor(100*cs.interaction_3)/100)
    pdf.cell(190, 10, txt = string, border = 0, ln = 1, fill = False, align = 'L')
    string = "      left web          eta_3: "+str(math.floor(100*cs.eta_3_side_4)/100) + "   interaction: "+str(math.floor(100*cs.interaction_4)/100)
    pdf.cell(190, 10, txt = string, border = 0, ln = 1, fill = False, align = 'L')
    pdf.add_page()


    #open the cs_analysis.txt file and read each line
    txt_file = open("user_interface/output/cs_analysis.txt", "r")
    for line in txt_file:

        number_of_dots = 0
        for char in line:
            if char == ".":
                number_of_dots += 1

        #reading the lines and deciding on how to format them
        if "Buckling Proof" in line:
            pdf.set_font("Arial", 'B', size = 15)
            pdf.cell(190, 10, txt = line, border = 0, ln = 1, fill = False, align = 'C')
            pdf.set_font("Arial", size = 12)
            pdf.set_fill_color(255, 0, 10)
        elif line[0]!= " " and line != "\n":
            pdf.set_font("Arial", size = 14)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(190, 10, txt = line, border = 1, ln = 1, fill = True, align = 'C')
            pdf.set_font("Arial", size = 12)
            pdf.set_fill_color(255, 0, 10)
        elif number_of_dots == 0 and "Side" in line:
            pdf.cell(190, 10, txt = line, border = 1, ln = 1, fill = False, align = 'L')
        elif "               " in line:
            pdf.cell(200, 10, txt = "                     " + line, border = 0, ln = 1, align = 'L')
        elif "            " in line:
            pdf.cell(200, 10, txt = "               " + line, border = 0, ln = 1, align = 'L')
        elif "         " in line:
            pdf.cell(200, 10, txt = "         " + line, border = 0, ln = 1, align = 'L')
        elif "      " in line:
            pdf.cell(200, 10, txt = "   " + line, border = 0, ln = 1, align = 'L')
        elif "   " in line:
            pdf.cell(200, 10, txt = line, border = 0, ln = 1, align = 'L')
        else:
            pdf.cell(200, 10, txt = line, border = 0, ln = 1, align = 'L')

    #pdf.image("user_interface/output/images/"+name+"_out.png", x = None, y = None, w = 200, h = 0, type = '', link = '')

    if location != None:
        pdf.output(location+str(name)+".pdf", "F")
    else:
        # save the pdf with name .pdf
        pdf.output("user_interface/static/"+str(name)+".pdf", "F")








#a function that prints a proof pdf per cs in best_crosssections
#uses the txt_to_pdf function
def print_best_proof():
    i = 1
    for cs in cs_collector.get_best():
        #clear the txt file
        file = open("user_interface/output/cs_analysis.txt", "w+")
        file.close()

        #reset the cross-section so that the proof can be performed
        cs.reset()
        name = "cs_"+str(i)
        cs = buckling_proof.buckling_proof(cs)
        txt_to_pdf(cs, name, location = "user_interface/output/best_crosssections/")

        i+= 1






#print a list of the best cross sections
def print_best():
    #clear the all.txt file
    file = open("user_interface/output/all.txt", "w+")
    file.close()
    file_name = "all"

    i = 1
    for cs in cs_collector.get_best():
        name = "cs_"+str(i)

        geometry_output.print_cs_to_png(cs, name, input = False, location = "user_interface/output/best_crosssections/")
        ei = round(cs.get_ei() / 1000 / 1000 / 1000)
        cost = optimization_value.cost(cs)

        string = "\n"+name
        string += cs.print_cs_as_list()
        string += "\n\nResults:"
        string += "\n   EI: "+str(ei)+"kNm^2"
        string += "\n   interaction side 1: "+str(cs.interaction_1)
        string += "\n   interaction side 2: "+str(cs.interaction_2)
        string += "\n   interaction side 3: "+str(cs.interaction_3)
        string += "\n   interaction side 4: "+str(cs.interaction_4)
        string += "\n   eta_1: "+str(cs.eta_1)
        string += "\n   eta_3 side 1: "+str(cs.eta_3_side_1)
        string += "\n   eta_3 side 2: "+str(cs.eta_3_side_2)
        string += "\n   eta_3 side 3: "+str(cs.eta_3_side_3)
        string += "\n   eta_3 side 4: "+str(cs.eta_3_side_4)
        string += "\n   cost: "+str(cost)+"CHF/m"


        file = open("user_interface/output/all.txt", "a+")
        file.write(string)
        file.close()
        i += 1

    #now create the pdf from the all.txt file
    pdf = PDF()
    pdf.add_page()
    # Title
    pdf.set_font('Arial', 'B', 15)
    pdf.cell(30) # Move to the right
    pdf.cell(100, 10, "Cross Section Optimization Tool - Results", border = 0, ln = 1, align = 'C')


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
        self.set_font('Arial', 'B', 8)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(30, 10, "CS Analysis and Optimization Program", 0, 0, 'C')
        self.cell(45)
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
