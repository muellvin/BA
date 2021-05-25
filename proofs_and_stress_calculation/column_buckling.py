import sys
import math
import copy
from classes import crosssection
from classes import point
from classes import line
from data_and_defaults import data
from data_and_defaults import defaults
sys.path.insert(0, './user_interface')
from output import printing





#EC 1993 1-5 (7)  stiffeners as a member have to be investigated as they can be of different form
#
#according to the EC 1993 1-5 (1) the equivalent member can no longer be seen as supported on the sides
#
#according to A.2 (3) -> Illustration A.1
#the contributing widths are the ones defined by local buckling

#does not write attributes thus does not need cs
def column_buckling(plate_glob, side, height_zero_pressure, height_max_pressure):
    string = "\n      4.5.3 Column type buckling behaviour"
    printing.printing(string, terminal = True)


    #add the lines to the right list
    stiffener_lines = []
    tpl_lines_list = []
    stiffeners_list = []
    #points of max pressure and zero pressure; needed for extrapolation
    point_max = None
    sigma_max = 0
    for plate in plate_glob.lines:
        if plate.code.tpl_number == 0:
            stiffener_lines.append(plate)
        elif plate.code.pl_type == 0:
            tpl_lines_list.append(plate)
        #for extrapolation b_c and the positions will be required
        if plate.sigma_a_red >= sigma_max:
            point_max = copy.deepcopy(plate.a)
            sigma_max = plate.sigma_a_red
        elif plate.sigma_b_red >= sigma_max:
            point_max = copy.deepcopy(plate.b)
            sigma_max = plate.sigma_b_red




    #case 1: stiffened plate
    if stiffener_lines != []:
        st_number_min = stiffener_lines[0].code.st_number
        st_number_max = stiffener_lines[0].code.st_number
        for plate in stiffener_lines:
            if plate.code.st_number < st_number_min:
                st_number_min = plate.code.st_number
            elif plate.code.st_number > st_number_max:
                st_number_max = plate.code.st_number
        number_of_stiffeners = int(len(stiffener_lines)/3)

        for i in range(number_of_stiffeners):
            stiffeners_list.append(crosssection.crosssection(0, 0, 0))
            for plate in stiffener_lines:
                if plate.code.st_number == i+st_number_min:
                    stiffeners_list[i].lines.append(plate)

        #sort the lists
        tpl_lines_list = sorted(tpl_lines_list, key = lambda plate: plate.code.tpl_number)
        stiffeners_list = sorted(stiffeners_list, key = lambda stiffener: stiffener.lines[0].code.st_number)

        #create sets
        tpl_st_lines_set = {}
        tpl_betw_lines_set = {}

        j = 1
        for plate in tpl_lines_list:
            #is the tpl_number even, (or odd, see correction)
            #meaning included in a stiffener
            if j%2 == 0:
                st_number = st_number_min + int(j/2) - 1
                tpl_st_lines_set.update({st_number: plate})
            else:
                st_number_before = st_number_min + int(j/2) - 1
                tpl_betw_lines_set.update({st_number_before: plate})
            j += 1

        stiffeners_set = {}
        stiffeners_set_length = 0
        for stiffener in stiffeners_list:
            st_number = stiffener.lines[0].code.st_number
            stiffeners_set.update({st_number: stiffener})
            stiffeners_set_length += 1


        columns = {}
        i = st_number_min
        #a set of all columns (stiffener + carrying widths) is created -> see column_class
        #they carry the number of the stiffener and they have the stiffener number as a key
        while i < st_number_max+1:
            stiffener_i = copy.deepcopy(stiffeners_set.get(i))
            plate_before = copy.deepcopy(tpl_betw_lines_set.get(i-1))
            plate_between = copy.deepcopy(tpl_st_lines_set.get(i))
            plate_after = copy.deepcopy(tpl_betw_lines_set.get(i))
            code_before = plate_before.code
            code_between = plate_between.code
            code_after = plate_after.code
            plate_between_A_tot = plate_between.get_area_tot()
            plate_between_A_red = plate_between.get_area_red()
            plate_between_I_tot = plate_between.get_i_along_tot()

            #plate_before
            plate_before_gross_len = figure_Aone(plate_before, False, True)
            factor = plate_before_gross_len/plate_before.get_length_tot()
            point_a_y = plate_before.b.y + factor*(plate_before.a.y - plate_before.b.y)
            point_a_z = plate_before.b.z + factor*(plate_before.a.z - plate_before.b.z)
            border_before_gross = point.point(point_a_y, point_a_z)
            plate_before_gross = line.line(code_before, border_before_gross, plate_before.b, plate_before.t)
            plate_before_gross_I = plate_before_gross.get_i_along_tot()
            plate_before_gross_A = plate_before_gross.get_area_tot()
            sigma_border_before_gross = plate_before.sigma_b_red + factor*(plate_before.sigma_a_red - plate_before.sigma_b_red)
            plate_before_gross.sigma_a_red = sigma_border_before_gross
            plate_before_gross.sigma_b_red = plate_before.sigma_b_red

            plate_before_eff_len = figure_Aone(plate_before, False, False)
            factor = plate_before_eff_len/plate_before.get_length_tot()
            point_a_y = plate_before.b.y + factor*(plate_before.a.y - plate_before.b.y)
            point_a_z = plate_before.b.z + factor*(plate_before.a.z - plate_before.b.z)
            border_before_eff = point.point(point_a_y, point_a_z)
            plate_before_eff = line.line(code_before, border_before_eff, plate_before.b, plate_before.t)
            plate_before_eff_I = plate_before_eff.get_i_along_tot()
            plate_before_eff_A = plate_before_eff.get_area_tot()
            sigma_border_before_eff = plate_before.sigma_b_red + factor*(plate_before.sigma_a_red - plate_before.sigma_b_red)
            plate_before_eff.sigma_a_red = sigma_border_before_eff
            plate_before_eff.sigma_b_red = plate_before.sigma_b_red

            #plate_after
            plate_after_gross_len = figure_Aone(plate_after,True, True)
            factor = plate_after_gross_len/plate_after.get_length_tot()
            point_b_y = plate_after.a.y + factor*(plate_after.b.y - plate_after.a.y)
            point_b_z = plate_after.a.z + factor*(plate_after.b.z - plate_after.a.z)
            border_after_gross = point.point(point_b_y, point_b_z)
            plate_after_gross = line.line(code_after, plate_after.a, border_after_gross, plate_after.t)
            plate_after_gross_I = plate_after_gross.get_i_along_tot()
            plate_after_gross_A = plate_after_gross.get_area_tot()
            sigma_border_after_gross = plate_after.sigma_b_red + factor*(plate_after.sigma_a_red - plate_after.sigma_b_red)
            plate_after_gross.sigma_a_red = plate_after.sigma_a_red
            plate_after_gross.sigma_b_red = sigma_border_after_gross

            plate_after_eff_len = figure_Aone(plate_after, True, False)
            factor = plate_after_eff_len/plate_after.get_length_tot()
            point_b_y = plate_after.a.y + factor*(plate_after.b.y - plate_after.a.y)
            point_b_z = plate_after.a.z + factor*(plate_after.b.z - plate_after.a.z)
            border_after_eff = point.point(point_b_y, point_b_z)
            plate_after_eff = line.line(code_after, plate_after.a, border_after_eff, plate_after.t)
            plate_after_eff_I = plate_after_eff.get_i_along_tot()
            plate_after_eff_A = plate_after_eff.get_area_tot()
            sigma_border_after_eff = plate_after.sigma_b_red + factor*(plate_after.sigma_a_red - plate_after.sigma_b_red)
            plate_after_eff.sigma_a_red = plate_after.sigma_a_red
            plate_after_eff.sigma_b_red = sigma_border_after_eff


            #EC 1993 1-5 4.5.3 (3)
            A_sl = stiffener_i.get_area_tot() + plate_before_gross_A + plate_after_gross_A + plate_between_A_tot
            A_sl_eff = stiffener_i.get_area_red() + plate_before_eff_A + plate_after_eff_A + plate_between_A_red
            I_sl = stiffener_i.get_i_along_tot(plate_between) + plate_before_gross_I + plate_after_gross_I + plate_between_I_tot
            sigma_cr_sl = (math.pi**2 * data.constants.get("E") * I_sl) / (A_sl * data.input_data.get("a")**2)


            ######calculation of sigma_cr_c################
            #span of column
            b = dis_points(border_before_gross, border_after_gross)
            #stress ratio across the whole cross-section of the column
            stress_ratio = min(sigma_border_before_gross, sigma_border_after_gross) / max(sigma_border_before_gross, sigma_border_after_gross)

            column_as_cs = copy.deepcopy(stiffener_i)
            column_as_cs.addline(plate_before_gross)
            column_as_cs.addline(plate_after_gross)
            column_as_cs.addline(plate_between)


            #calculating stiffener center
            tpl_st_center = point.point(tpl_st_lines_set.get(i).get_center_y_tot(), tpl_st_lines_set.get(i).get_center_z_tot())
            height_stiffener_center = tpl_st_center.z

            #calculating b_c and sigma_cr_c
            all_tension = False
            if sigma_border_before_gross<0 and sigma_border_after_gross<0:
                #all tension
                b_c = 0
                sigma_cr_c = 10**8
                all_tension = True
            elif abs(sigma_border_before_gross - sigma_border_after_gross) < 0.5:
                #same pressure; bottom stiffener; no extrapolation required
                b_c = b
                sigma_cr_c = sigma_cr_sl
                all_tension = False
            #different pressure; side stiffener; extrapolation required
            else:
                b_sl_1 = height_stiffener_center -height_zero_pressure
                b_c = height_max_pressure-height_zero_pressure
                factor = b_c/b_sl_1
                if factor > 0:
                    #stiffener in compression zone --> extrapolation
                    sigma_cr_c = sigma_cr_sl * factor
                else:
                    #stiffener in tension zone --> no proof required
                    b_c = 0
                    sigma_cr_c = 10**8
                    all_tension = True



            #excentricities
            st_center = point.point(stiffener_i.get_center_y_tot(), stiffener_i.get_center_z_tot())

            sl_cs = crosssection.crosssection(0,0,0)
            for plate in stiffener_i.lines:
                sl_cs.addline(plate)
            sl_cs.addline(plate_before_gross)
            sl_cs.addline(plate_after_gross)
            sl_cs.addline(plate_between)

            #center of the whole column
            sl_center = point.point(sl_cs.get_center_y_tot(), sl_cs.get_center_z_tot())

            e2 = dis_plate_point(tpl_st_lines_set.get(i), sl_center)
            e1 = dis_plate_point(tpl_st_lines_set.get(i), st_center) - e2



            column = column_class(i, A_sl, A_sl_eff, I_sl, sigma_cr_c, e1, e2, all_tension, column_as_cs)

            columns.update({i: column})


            printing.printing(str(column))

            i += 1
        #all columns created



        Chi_c = 10**8
        sigma_cr_c = 1



        #searches for the single column buckling mechanism with the smallest Chi_c
        #this one will be the defining column mechanism
        #as not all our stiffeners will be the same, we can not conclude that it is one at a border (highest pressure)
        for key in columns:
            Chi_c_column = column_buckling_Chi_c(columns.get(key))
            if Chi_c_column < Chi_c:
                Chi_c = Chi_c_column
                sigma_cr_c = column.sigma_cr_c


    #case 2: unstiffened plate
    else:
        t_plate = tpl_lines_list[0].t
        sigma_cr_c = math.pi**2 * data.constants.get("E") * t_plate**2 / \
        (12 * (1-data.constants.get("nu")**2)*data.input_data.get("a")**2)
        lambda_c_bar = math.sqrt(data.constants.get("f_y") / sigma_cr_c)
        alpha = 0.21
        Phi_c = 0.5*(1+alpha*(lambda_c_bar - 0.2) + lambda_c_bar**2)

        Chi_c = 1 / (Phi_c + math.sqrt(Phi_c**2 - lambda_c_bar**2))
        if Chi_c > 1:
            Chi_c = 1

        line1 = "\n         Unstiffened Plate"
        line2 = "\n            sigma_cr_c: "+str(sigma_cr_c)
        line3 = "\n            lambda_c_bar ="+str(lambda_c_bar)
        line4 = "\n            Phi_c: "+str(Phi_c)
        line5 = "\n            Chi_c: "+str(Chi_c)
        string = line1 + line2 + line3 + line4 + line5
        printing.printing(string, terminal = True)

    line1 = "\n         Critical buckling values"
    line2 = "\n            Chi_c: "+str(Chi_c)
    line3 = "\n            sigma_cr_c: "+str(sigma_cr_c)
    string = line1 + line2 + line3
    printing.printing(string, terminal = True)

    return Chi_c, sigma_cr_c







def column_buckling_Chi_c(column):

    if column.all_tension == True:
        beta_A_c = column.A_sl_eff / column.A_sl
        lambda_c_bar = 0
        Phi_c = 0
        Chi_c = 1
        line1 = str(column)
        line2 = "\n         Buckling Values "+str(column.st_number)
        line3 = "\n            beta_A_c =" +str(beta_A_c)
        line4 = "\n            lambda_c_bar =" +str(lambda_c_bar)
        line5 = "\n            Phi_c ="+ str(Phi_c)
        line6 = "\n            Chi_c ="+ str(Chi_c)
        string = line1 + line2 + line3 + line4 + line5 + line6
        printing.printing(string, terminal = True)
        return 1
    else:
        beta_A_c = column.A_sl_eff / column.A_sl
        lambda_c_bar = math.sqrt(beta_A_c * data.constants.get("f_y") / column.sigma_cr_c)

        i = math.sqrt(column.I_sl/column.A_sl)
        e = max(column.e1, column.e2)
        alpha = 0.34 #curve b for closed stiffeners
        alpha_e = alpha + 0.09/(e/i)

        Phi_c = 0.5*(1+alpha_e*(lambda_c_bar - 0.2) + lambda_c_bar**2)
        Chi_c = 1 / (Phi_c + math.sqrt(Phi_c**2 - lambda_c_bar**2))
        if Chi_c > 1:
            Chi_c = 1

        line1 = str(column)
        line2 = "\n         Buckling Values "+str(column.st_number)
        line3 = "\n            beta_A_c =" +str(beta_A_c)
        line4 = "\n            lambda_c_bar =" +str(lambda_c_bar)
        line5 = "\n            Phi_c ="+ str(Phi_c)
        line6 = "\n            Chi_c ="+ str(Chi_c)
        string = line1 + line2 + line3 + line4 + line5 + line6
        printing.printing(string, terminal = True)

        return Chi_c

#this functions calculates the area of the adjacent plates that can be counted to the column
#both for gross (A_sl1) and effective (A_sl1_eff)
def figure_Aone(plate, a, gross):
    assert plate.rho_c_a == 1, "Error reduction rho_c_a should not be included at column-like buckling"
    assert plate.rho_c_b == 1, "Error reduction rho_c_b should not be included at column-like buckling"

    #is the width superior (on side of higher stress of plate) or inferior (on side of lower stress of plate)
    if a:
        if plate.sigma_a_red > plate.sigma_b_red:
            sup = True
        else:
            sup = False #inf is the case
    else:
        if plate.sigma_b_red > plate.sigma_a_red:
            sup = True
        else:
            sup = False #inf is the case

    #all pressure no tension
    if plate.psi >= 0:
        if gross:
            b = plate.get_length_tot()
        else:
            b = plate.get_length_red()

        if sup:
            factor = 2 / (5-plate.psi)
        else:
            factor = (3-plate.psi) / (5-plate.psi)

        return factor*b

    #some tension
    elif plate.psi < 0:
        if gross:
            b_c = 1 / (1-plate.psi) * plate.get_length_tot()
        else:
            b_c = plate.get_length_red() - (-plate.psi/(1-plate.psi))*plate.get_length_tot()

        if sup:
            factor = 0.4
        else:
            factor = 0

        return factor*b_c



#function to calculate the distance between two points
def dis_points(a, b):
    return math.sqrt((a.y - b.y)**2 + (a.z - b.z)**2)

#function to calculate the distance between a plate and a point using the dot product
def dis_plate_point(plate, point):
    plate_vector_y = 1/plate.get_length_tot() * (plate.b.y - plate.a.y)
    plate_vector_z = 1/plate.get_length_tot() * (plate.b.z - plate.a.z)
    norm_vector_y = - plate_vector_z
    norm_vector_z = plate_vector_y

    point_vector_y = point.y - plate.a.y
    point_vector_z = point.z - plate.a.z

    #dot product
    dis = point_vector_y * norm_vector_y + point_vector_z * norm_vector_z

    return abs(dis)



class column_class():
    #constructor
    def __init__(self,st_number, A_sl, A_sl_eff, I_sl, sigma_cr_c, e1, e2, all_tension, column_as_cs):
        self.st_number = st_number
        self.A_sl = A_sl
        self.A_sl_eff = A_sl_eff
        self.I_sl = I_sl
        self.sigma_cr_c = sigma_cr_c
        self.e1 = e1
        self.e2 = e2
        self.all_tension = all_tension
        self.column_as_cs = column_as_cs

    #method to get string output when print()
    def __str__(self):
        line1 = "\n         Column number "+str(self.st_number)
        line2 = "\n            A_sl="+str(int(100*self.A_sl)/100)+", A_sl_eff="+str(int(100*self.A_sl_eff)/100)+", I_sl="+str(int(100*self.I_sl)/100)
        line3 = "\n            sigma_cr_c="+str(int(100*self.sigma_cr_c)/100)
        line4 = "\n            e1="+str(int(100*self.e1)/100)+", e2="+str(int(100*self.e2)/100)
        line5 = "\n            All tension ="+str(self.all_tension)
        #rest = str(self.column_as_cs)

        string = line1 + line2 + line3 + line4 + line5 #+ rest
        return string
