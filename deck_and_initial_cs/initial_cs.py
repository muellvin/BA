from classes import line
from classes import point
from classes import crosssection
from classes import plate_code

def create_initial_cs(b_sup, b_inf, h, t_side, t_deck, t_bottom):
    #create four corner points
    a1 = point.point(0.5*b_sup, 0)
    a2 = point.point(0.5*b_sup, 0)
    b1 = point.point(-0.5*b_sup, 0)
    b2 = point.point(-0.5*b_sup, 0)
    c1 = point.point(-0.5*b_inf, h)
    c2 = point.point(-0.5*b_inf, h)
    d1 = point.point(0.5*b_inf, h)
    d2 = point.point(0.5*b_inf, h)

    #create four lines
    code_1 = plate_code.plate_code(1,0,1,0,0)
    line_1 = line.line(code_1, a1, b2, t_deck)
    code_2 = plate_code.plate_code(2,0,2,0,0)
    line_2 = line.line(code_2, b1, c2, t_side)
    code_3 = plate_code.plate_code(3,0,3,0,0)
    line_3 = line.line(code_3, c1, d2, t_bottom)
    code_4 = plate_code.plate_code(4,0,4,0,0)
    line_4 = line.line(code_4, d1, a2, t_side)

    #add lines to crosssection
    x_section = crosssection.crosssection(b_sup, b_inf, h)
    x_section.addline(line_1)
    x_section.addline(line_2)
    x_section.addline(line_3)
    x_section.addline(line_4)

    return x_section

#nino: track-plate
#initialer cs erstellen; fahrbahnplatte mit normierten dicken
