import defaults
from fpdf import FPDF



def printing(string, terminal = False, paragraph = None, pn = 0, sn = 0, cn = 0):
    if terminal == True and defaults.do_print_to_txt == True:
        file = open("output\cs_analysis.txt", "a+")
        file.write(string)
        file.close()
    if terminal == True and defaults.do_print_to_terminal == True:
        print(string, end = "")

    """
        string is the text
        paragraph is a string saying what it is
        pn is the proof number
        sn is the side number
        cn is the column number
    """

    text = paragraph_class(string, paragraph, pn, sn, cn)
    output_text.append(text)


def txt_to_pdf():
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
    # save the pdf with name .pdf
    pdf.output("output/cs_analysis.pdf", "F")



output_text = []
#list of output objects paragraph class

class paragraph_class():
    def __init__(self, string, paragraph = None, pn = 0, sn = 0, cn = 0):
        self.string = string
        self.paragraph = paragraph
        self.pn = pn
        self.sn = sn
        self.cn = cn






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
