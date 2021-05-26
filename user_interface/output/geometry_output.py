#first version of geometry output using matplotlib

#imports
import matplotlib.pyplot as plt
import numpy

#function that prints the gross cross section
def print_cs(crosssection):
    for i in range(len(crosssection.lines)):
        y = []
        z = []
        line = crosssection.lines[i]
        y.append(-line.a.y)
        y.append(-line.b.y)
        z.append(-line.a.z)
        z.append(-line.b.z)
        y_list = numpy.array(y)
        z_list = numpy.array(z)
        if line.code.tpl_number != 0:
            plt.plot(y_list, z_list, 'k')
        else:
            plt.plot(y_list, z_list, 'r')


    plt.axis('scaled')
    plt.show()

#function that prints the effective cross section
def print_cs_red(crosssection):

    for i in range(len(crosssection.lines)):
        line = crosssection.lines[i]
        y = []
        z = []

        y.append(-line.a.y)
        y.append(-line.p1.y)
        z.append(-line.a.z)
        z.append(-line.p1.z)
        y_list = numpy.array(y)
        z_list = numpy.array(z)
        plt.plot(y_list, z_list, 'k')



    for i in range(len(crosssection.lines)):
        line = crosssection.lines[i]
        y = []
        z = []
        y.append(-line.p2.y)
        y.append(-line.b.y)
        z.append(-line.p2.z)
        z.append(-line.b.z)
        y_list = numpy.array(y)
        z_list = numpy.array(z)
        plt.plot(y_list, z_list, 'r')

    plt.axis('scaled')
    plt.show()

#function that prints the effective cross section to png
def print_cs_to_png(crosssection, name, input = True, location = None):


    figure = plt.figure()

    if input:
        for i in range(len(crosssection.lines)):
            line = crosssection.lines[i]
            y = []
            z = []

            y.append(-line.a.y)
            y.append(-line.b.y)
            z.append(-line.a.z)
            z.append(-line.b.z)
            y_list = numpy.array(y)
            z_list = numpy.array(z)
            plt.plot(y_list, z_list, 'k')
    else:

        for i in range(len(crosssection.lines)):
            line = crosssection.lines[i]
            y = []
            z = []

            y.append(-line.a.y)
            y.append(-line.p1.y)
            z.append(-line.a.z)
            z.append(-line.p1.z)
            y_list = numpy.array(y)
            z_list = numpy.array(z)
            plt.plot(y_list, z_list, 'k')

        for i in range(len(crosssection.lines)):
            line = crosssection.lines[i]
            y = []
            z = []
            y.append(-line.p2.y)
            y.append(-line.b.y)
            z.append(-line.p2.z)
            z.append(-line.b.z)
            y_list = numpy.array(y)
            z_list = numpy.array(z)
            plt.plot(y_list, z_list, 'k')

    plt.axis('scaled')
    if location == None:
        if input:
            figure.savefig("user_interface/output/best_crosssections"+name+"_in.png")
        else:
            figure.savefig("user_interface/output/best_crosssections"+name+"_out.png")
    else:
        if input:
            figure.savefig(location+name+"_in.png")
        else:
            figure.savefig(location+name+"_out.png")
