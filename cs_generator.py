from classes import line as ln
from classes import point as pt
from classes import crosssection as cs
from classes import plate_code as plcd

def create_initial_cs(b_sup, b_inf, h, t_sup, t_inf, t_side):
    #create four corner points
    a = pt.point(0.5*b_sup, 0)
    b = pt.point(-0.5*b_sup, 0)
    c = pt.point(-0.5*b_sup, h)
    d = pt.point(0.5*b_inf, h)

    #create four lines
    code_1 = plcd.plate_code(1,0,0,0)
    line_1 = ln.line(code_1, a, b, 1)
    code_2 = plcd.plate_code(2,0,0,0)
    line_2 = ln.line(code_2, b, c, 1)
    code_3 = plcd.plate_code(3,0,0,0)
    line_3 = ln.line(code_3, c, d, 1)
    code_4 = plcd.plate_code(4,0,0,0)
    line_4 = ln.line(code_4, d, a, 1)

    #add lines to crosssection
    x_section = cs.crosssection()
    x_section.addline(line_1)
    x_section.addline(line_2)
    x_section.addline(line_3)
    x_section.addline(line_4)

    return x_section

#crosssection generation framework still to be completely implemented
class cs_collection():
    """This is a collection of crossections."""

    #constructor creates four empty crosssection lists
    def __init__(self, initial_cs, current_cs, last_cs, best_cs):
        self.initial_cs = crosssection()
        self.current_cs = crosssection()
        self.last_cs = crosssection()
        self.best_cs = crosssection()

    def create_initial(b_sup, b_inf, h, t_sup, t_inf, t_side):
        pass

    def add_stiffener(line, norm_position, stiffener):
        pass
