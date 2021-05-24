import matplotlib.pyplot as plt, mpld3
import numpy as np
from classes import line as ln
from classes import point as pt
from classes import crosssection as cs
from classes import plate_code as plcd


#function that prints a gross cross section to html
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

#function that prints the effective cross section to html
def print_cs_red(crosssection):

    fig = plt.figure()
    fig, ax = plt.subplots()
    ax.axis('scaled')
    ax.set_xlim([-3000, 3000])
    ax.set_ylim([-3000, 1000])

    for i in range(len(crosssection.lines)):
        line = crosssection.lines[i]
        y = []
        z = []

        y.append(-line.a.y)
        y.append(-line.p1.y)
        z.append(-line.a.z)
        z.append(-line.p1.z)
        y_list = np.array(y)
        z_list = np.array(z)
        ax.plot(y_list, z_list, 'k')



    for i in range(len(crosssection.lines)):
        line = crosssection.lines[i]
        y = []
        z = []
        y.append(-line.p2.y)
        y.append(-line.b.y)
        z.append(-line.p2.z)
        z.append(-line.b.z)
        y_list = np.array(y)
        z_list = np.array(z)
        ax.plot(y_list, z_list, 'r')

    return mpld3.fig_to_html(fig)
