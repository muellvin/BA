from classes import crosssection
from classes import point
from classes import line
from output import geometry_output
import math
import data
import copy
import defaults




#EC 1993 1-5 (7)  stiffeners as a member have to be investigated as they can be of different form
#
#according to the EC 1993 1-5 (1) the equivalent member can no longer be seen as supported on the sides
#
#according to A.2 (3) -> Illustration A.1
#the contributing widths are the ones defined by local buckling

#does not write attributes thus does not need cs
def column_buckling(plate_glob, side):
    if defaults.do_print == True:
        if defaults.do_print_to_txt == True:
            pass
        else:
            print("***************************** column_buckling for side "+str(side)+" **************************************")


    #add the lines to the right list
    stiffener_lines = []
    tpl_lines_list = []
    stiffeners_list = []
    for plate in plate_glob.lines:
        if plate.code.tpl_number == 0:
            stiffener_lines.append(plate)
        elif plate.code.pl_type == 0:
            tpl_lines_list.append(plate)

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
        if defaults.do_print == True:
            if defaults.do_print_to_txt == True:
                pass
            else:
                print("there are "+str(number_of_stiffeners)+" stiffeners on side "+str(side))


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
            #geometry_output.print_cs_red(stiffener)


        print("there are "+str(stiffeners_set_length)+" columns to be created")




        columns = {}
        i = st_number_min
        #a set of all columns (stiffener + carrying widths) is created -> see column_class
        #they carry the number of the stiffener and they have the stiffener number as a key
        while i < st_number_max+1:
            print("     creating column of stiffener "+str(i))
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

            #if the widths were not reduced (p1 is the same as p2) the whole plate is taken into account not only until one of p1 or p2
            if dis_points(plate_before.p1, plate_before.p2) < 0.05:
                print(dis_points(plate_before.p1, plate_before.p2))
                plate_before_A = plate_before.get_area_tot()
                plate_before_I = plate_before.get_i_along_tot()
                sigma_border_before = plate_before.sigma_a_red
                border_before = plate_before.a
                plate_before_eff = line.line(code_before, border_before, plate_before.b, plate_before.t)
            else:
                plate_before_A = plate_before.get_area_red2()
                plate_before_I = plate_before.get_i_along_red2()
                sigma_border_before = plate_before.sigma_a_red
                border_before = plate_before.p2
                plate_before_eff = line.line(code_before, border_before, plate_before.b, plate_before.t)

            if dis_points(plate_after.p1, plate_after.p2) < 0.05:
                plate_after_A = plate_after.get_area_tot()
                plate_after_I = plate_after.get_i_along_tot()
                sigma_border_after = plate_after.sigma_b_red
                border_after = plate_after.b
                plate_after_eff = line.line(code_after, plate_after.a, border_after, plate_after.t)
            else:
                plate_after_A = plate_after.get_area_red1()
                plate_after_I = plate_after.get_i_along_red1()
                sigma_border_after = plate_after.sigma_b_red
                border_after = plate_after.p1
                plate_after_eff = line.line(code_after, plate_after.a, border_after, plate_after.t)


            #EC 1993 1-5 4.5.3 (3)
            A_sl = stiffener_i.get_area_tot() + plate_before_A + plate_after_A + plate_between_A_tot
            A_sl_eff = stiffener_i.get_area_red() + plate_before_A + plate_after_A + plate_between_A_red
            I_sl = stiffener_i.get_i_along_tot(plate_between) + plate_before_I + plate_after_I + plate_between_I_tot
            sigma_cr_sl = (math.pi**2 * data.constants.get("E") * I_sl) / (A_sl * data.input_data.get("a"))


            ######calculation of sigma_cr_c################
            #span of column
            b = dis_points(border_before, border_after)
            #stress ratio across the whole cross-section of the column
            stress_ratio = min(sigma_border_before, sigma_border_after) / max(sigma_border_before, sigma_border_after)

            column_as_cs = stiffener_i
            column_as_cs.addline(plate_before_eff)
            column_as_cs.addline(plate_after_eff)
            column_as_cs.addline(plate_between)
            geometry_output.print_cs_red(column_as_cs)

            #assure the column is under pressure (positive) somewhere
            all_tension = False
            if sigma_border_before > 0 or sigma_border_after > 0:
                if sigma_border_before != sigma_border_after:
                    b_c = b * 1/(1-stress_ratio)
                else:
                    b_c = dis_points(border_before,border_after)
            else:
                b_c = 0
                all_tension = True


            tpl_st_center = point.point(tpl_st_lines_set.get(i).get_center_y_tot(), tpl_st_lines_set.get(i).get_center_z_tot())

            #from which side should be extrapolated
            if sigma_border_before < sigma_border_after:
                b_sl_1 = dis_points(border_before, tpl_st_center)
                sigma_cr_c = sigma_cr_sl * b_c / b_sl_1
            elif sigma_border_before > sigma_border_after:
                b_sl_1 = dis_points(border_after, tpl_st_center)
                sigma_cr_c = sigma_cr_sl * b_c / b_sl_1
            #all the same pressure, no extrapolation necessary
            else:
                b_sl_1 = b_c
                sigma_cr_c = sigma_cr_sl

            #excentricities
            st_center = point.point(stiffener_i.get_center_y_tot(), stiffener_i.get_center_z_tot())

            sl_cs = crosssection.crosssection(0,0,0)
            for plate in stiffener_i.lines:
                sl_cs.addline(plate)
            sl_cs.addline(plate_before_eff)
            sl_cs.addline(plate_after_eff)
            sl_cs.addline(plate_between)

            #center of the whole column
            """center of reduced or total area??????????"""
            sl_center = point.point(sl_cs.get_center_y_tot(), sl_cs.get_center_z_tot())

            e2 = dis_plate_point(tpl_st_lines_set.get(i), sl_center)
            e1 = dis_plate_point(tpl_st_lines_set.get(i), st_center) - e2

            column = column_class(i, A_sl, A_sl_eff, I_sl, sigma_cr_c, e1, e2, all_tension, column_as_cs)
            columns.update({st_number: column})

            i += 1

        Chi_c = 1
        sigma_cr_c = 1

        #searches for the single column buckling mechanism with the smallest Chi_c
        #this one will be the defining column mechanism
        #as not all our stiffeners will be the same, we can not conclude that it is one at a border (highest pressure)
        for column in columns.values():
            if defaults.do_print == True:
                if defaults.do_print_to_txt == True:
                    pass
                else:
                    print(column)
            Chi_c_column = column_buckling_Chi_c(column)
            if Chi_c_column < Chi_c:
                Chi_c = Chi_c_column
                sigma_cr_c = column.sigma_cr_c


    #case 2: unstiffened plate
    else:
        t_plate = tpl_lines_list[0].t
        print(t_plate)
        sigma_cr_c = math.pi**2 * data.constants.get("E") * t_plate**2 / \
        (12 * (1-data.constants.get("nu")**2)*defaults.plate_length**2)
        lambda_c_bar = math.sqrt(data.constants.get("f_y") / sigma_cr_c)
        alpha = 0.21
        Phi_c = 0.5*(1+alpha*(lambda_c_bar - 0.2) + lambda_c_bar**2)
        print("lambda_c_bar =", lambda_c_bar)
        print("Phi_c =", Phi_c)
        Chi_c = 1 / (Phi_c + math.sqrt(Phi_c**2 - lambda_c_bar**2))



    return Chi_c, sigma_cr_c







def column_buckling_Chi_c(column):
    if column.all_tension == True:
        return 1
    else:
        beta_A_c = column.A_sl_eff / column.A_sl
        print("beta_A_c =", beta_A_c)
        lambda_c_bar = math.sqrt(beta_A_c * data.constants.get("f_y") / column.sigma_cr_c)

        i = math.sqrt(column.I_sl/column.A_sl)
        e = max(column.e1, column.e2)
        alpha = 0.34 #curve b for closed stiffeners
        alpha_e = alpha + 0.09/(e/i)

        Phi_c = 0.5*(1+alpha_e*(lambda_c_bar - 0.2) + lambda_c_bar**2)

        print("lambda_c_bar =", lambda_c_bar)
        print("Phi_c =", Phi_c)
        Chi_c = 1 / (Phi_c + math.sqrt(Phi_c**2 - lambda_c_bar**2))

        return Chi_c



def dis_points(a, b):
    return math.sqrt((a.y - b.y)**2 + (a.z - b.z)**2)

def dis_plate_point(plate, point):
    plate_vector_y = 1/plate.get_length_tot() * (plate.b.y - plate.a.y)
    plate_vector_z = 1/plate.get_length_tot() * (plate.b.z - plate.a.z)
    norm_vector_y = - plate_vector_z
    norm_vector_z = plate_vector_y

    point_vector_y = point.y - plate.a.y
    point_vector_z = point.z - plate.a.z

    #dot product
    dis = point_vector_y * norm_vector_y + point_vector_z * norm_vector_z

    return dis



class column_class():
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


    def __str__(self):
        line1 = "''''''''''''''''''''''''''Column number "+str(self.st_number)+"'''''''''''''''''''''''''\n"
        line2 = "A_sl="+str(int(100*self.A_sl)/100)+", A_sl_eff="+str(int(100*self.A_sl_eff)/100)+", I_sl="+str(int(100*self.I_sl)/100)+"\n"
        line3 = "sigma_cr_c="+str(int(100*self.sigma_cr_c)/100)+"\n"
        line4 = "e1="+str(int(100*self.e1)/100)+", e2="+str(int(100*self.e2)/100)+"\n"
        line5 = "All tension ="+str(self.all_tension)+"\n"
        rest = str(self.column_as_cs)

        string = line1 + line2 + line3 + line4 + line5 + rest
        return string
