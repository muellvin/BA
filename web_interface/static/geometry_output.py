import matplotlib.pyplot as plt, mpld3
import numpy as np
from classes import line as ln
from classes import point as pt
from classes import crosssection as cs
from classes import plate_code as plcd

def create_initial_cs(b_sup, b_inf, h, t_side, t_deck, t_bottom):
    #create four corner points
    a1 = pt.point(0.5*b_sup, 0)
    a2 = pt.point(0.5*b_sup, 0)
    b1 = pt.point(-0.5*b_sup, 0)
    b2 = pt.point(-0.5*b_sup, 0)
    c1 = pt.point(-0.5*b_inf, h)
    c2 = pt.point(-0.5*b_inf, h)
    d1 = pt.point(0.5*b_inf, h)
    d2 = pt.point(0.5*b_inf, h)

    #create four lines
    code_1 = plcd.plate_code(1,0,1,0,0)
    line_1 = ln.line(code_1, a1, b2, t_deck)
    code_2 = plcd.plate_code(2,0,2,0,0)
    line_2 = ln.line(code_2, b1, c2, t_side)
    code_3 = plcd.plate_code(3,0,3,0,0)
    line_3 = ln.line(code_3, c1, d2, t_bottom)
    code_4 = plcd.plate_code(4,0,4,0,0)
    line_4 = ln.line(code_4, d1, a2, t_side)

    #add lines to crosssection
    x_section = cs.crosssection(b_sup, b_inf, h)
    x_section.addline(line_1)
    x_section.addline(line_2)
    x_section.addline(line_3)
    x_section.addline(line_4)

    return x_section

def print_cs(crosssection):
    fig = plt.figure()
    fig, ax = plt.subplots()
    ax.axis('scaled')
    ax.set_xlim([-3000, 3000])
    ax.set_ylim([-3000, 1000])
    for i in range(len(crosssection.lines)):
        y = []
        z = []
        line = crosssection.lines[i]
        y.append(-line.a.y)
        y.append(-line.b.y)
        z.append(-line.a.z)
        z.append(-line.b.z)
        y_list = np.array(y)
        z_list = np.array(z)
        if line.code.tpl_number != 0:
            ax.plot(y_list, z_list, 'k')
        else:
            ax.plot(y_list, z_list, 'r')
        #plt.axis('scaled')
        #plt.savefig(r'static\xs.png')
    #mpld3.save_html(fig, r'templates\figure.html')
    return mpld3.fig_to_html(fig)
