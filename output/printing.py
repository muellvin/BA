import defaults
from fpdf import FPDF
import cs_collector


def printing(string, terminal = False):
    if terminal == True and defaults.do_print_to_txt == True:
        file = open("output\cs_analysis.txt", "a+")
        file.write(string)
        file.close()
    if terminal == True and defaults.do_print_to_terminal == True:
        print(string, end = "")



def txt_to_pdf(name, location = None):
    # save FPDF() class into
    # a variable pdf
    pdf = PDF()

    # Add a page
    pdf.add_page()

    pdf.image("output/cs_in.png", x = None, y = None, w = 200, h = 0, type = '', link = '')
    # set style and size of font
    # that you want in the pdf
    pdf.set_font("Arial", size = 11)

    # open the text file in read mode
    txt_file = open("output/cs_analysis.txt", "r")

    # insert the texts in pdf
    for line in txt_file:
        if line[0]!= " " and line != "\n":
            pdf.cell(200, 10, txt = line, border = 1, ln = 1, align = 'C')
        else:
            pdf.cell(200, 10, txt = line, border = 0, ln = 1, align = 'L')

    pdf.image("output/cs_out.png", x = None, y = None, w = 200, h = 0, type = '', link = '')

    if location != None:
        pdf.output(location+str(name)+".pdf", "F")
    else:
        # save the pdf with name .pdf
        pdf.output("web_interface/templates/"+str(name)+".pdf", "F")



def print_best_proof():
    i = 1
    for cs in cs_cllector.get_best():
        cs.reset()
        name = "cs_"+str(i)
        geometry_output.print_cs_to_pdf(cs, input = True)

        cs = buckling_proof.buckling_proof(cs)

        ei = round(cs.get_ei() / 1000 / 1000 / 1000)
        interaction_2 = cs.interaction_2
        interaction_3 = cs.interaction_3
        interaction_4 = cs.interaction_4
        cost = optimization_value.cost(cs)
        line1 = "\n\nResults:"
        line2 = "\n   EI: "+str(ei)+"Nm^2"
        line3 = "\n   interaction side 2: "+str(interaction_2)
        line4 = "\n   interaction side 3: "+str(interaction_3)
        line5 = "\n   interaction side 4: "+str(interaction_4)
        line6 = "\n   cost: "+str(cost)+"CHF/m"
        string = line1 + line2 + line3 + line4 + line5 + line6
        printing.printing(string, terminal = True)

        geometry_output.print_cs_to_png(cs, input = False)
        printing.txt_to_pdf(name, location = "best_crosssections/")

def print_best():
        pass



class PDF(FPDF):
    def header(self):
        # Logo
        #self.image('logo_pb.png', 10, 8, 33)
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(30, 10, 'CS Analysis Tool', 0, 0, 'C')
        # Line break
        self.ln(20)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '\{nb}', 0, 0, 'C')
