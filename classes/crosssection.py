import math
import copy
import sys
sys.path.insert(0, './user_interface')
from output import printing
from data_and_defaults import data
from classes import line
from classes import plate_code
from classes import point

#crosssection class
class crosssection():

    """Constructor and Printing Methods"""

    #constructor
    def __init__(self, b_sup, b_inf, h, eta_1 = -2, eta_3_side_1 = -2, eta_3_side_2 = -2, eta_3_side_3 = -2, eta_3_side_4 = -2, interaction_1 = -2, interaction_2 = -2, interaction_3 = -2, interaction_4 = -2):
        #container for all plates
        self.lines = []
        #container for geometric values
        self.b_sup = b_sup
        self.b_inf = b_inf
        self.h = h
        #container for proof results
        self.eta_1 = eta_1
        self.eta_3_side_1 = eta_3_side_1
        self.eta_3_side_2 = eta_3_side_2
        self.eta_3_side_3 = eta_3_side_3
        self.eta_3_side_4 = eta_3_side_4
        self.interaction_1 = interaction_1
        self.interaction_2 = interaction_2
        self.interaction_3 = interaction_3
        self.interaction_4 = interaction_4
        #container for optimization values
        self.cost = 0
        self.ei = 0
        self.ratio = 0
        #container for optimization output
        self.st_props = None

    #for control
    def print_centers(self):
        line1 = "\ncenter z gross "+str(self.get_center_z_tot())
        line2 = "\ncenter z reduced "+str(self.get_center_z_red())
        return line1 + line2

    #method that prints the cross section (simple)
    def __str__(self):
        string = "\n cross-section with b_sup=" + str(self.b_sup) + ", b_inf=" + str(self.b_inf) + ", h=" + str(self.h) + "\n"
        for line in self.lines:
            string += str(line)
        return string

    #method that priints the cross section (more sophisticated)
    def print_cs_as_list(self):
        string = "\n\n      b_sup: "+str(self.b_sup)+"   b_inf: "+str(self.b_inf)+"   h: "+str(self.h)
        t_deck = self.get_line(pl_position =1, pl_type = 0).t
        t_sides = self.get_line(pl_position = 2, pl_type = 0).t
        t_bottom = self.get_line(pl_position = 3, pl_type = 0).t
        string += "\n      t_deck: "+str(t_deck)+"   t_sides: "+str(t_sides)+"   t_bottom: "+str(t_bottom)+"\n"
        if self.st_props != None:
            self.st_props.stiffeners = sorted(self.st_props.stiffeners, key = lambda st: st.st_number)
            for st in self.st_props.stiffeners:
                line1 = "\n Stiffener Number "+str(round(10*st.st_number)/10)+" on side "+str(round(10*st.pl_position)/10)+" with location: "+str(round(10*st.location)/10)
                line2 = "\n      b_sup: "+str(round(10*st.b_sup)/10)+"   b_inf: "+str(round(10*st.b_inf)/10)+"   h: "+str(round(10*st.h)/10)+"   t: "+str(round(10*st.t)/10)
                string += line1 + line2
        return string


    """Buckling Proof Verification Method"""

    #method that returns if the cross section passes the buckling proof
    def proven(self):
        proven = self.eta_1 < 1 and self.interaction_1 < 1 and self.interaction_2 < 1 and self.interaction_3 < 1 and \
        self.interaction_4 < 1 and self.eta_3_side_1 < 1 and self.eta_3_side_2 < 1 and self.eta_3_side_3 < 1 and self.eta_3_side_4 <1
        return proven


    """Crosssection Manipulation Methods"""

    #method that adds a line to the cross section
    def addline(self, line):
        self.lines.append(line)

    #method that resets all cross sectional values but does not remove any lines
    def reset(self):
        self.eta_1 = -2
        self.interaction_2 = -2
        self.interaction_3 = -2
        self.interaction_4 = -2
        for plate in self.lines:
            plate.t_stress = plate.t
            plate.beta = 1
            plate.rho_c_a = 1
            plate.rho_c_b = 1
            plate.sigma_a_red = 0
            plate.sigma_b_red = 0
            plate.sigma_p1_red = 0
            plate.sigma_p2_red = 0
            plate.psi = 1
            plate.rho_loc = 1
            plate.chi_c = 1
            plate.sigma_cr_c = 0
            plate.rho_p = 1
            plate.sigma_cr_p = 0

    #method that removes the stiffener with the respective stiffener number
    def remove_stiffener(self, st_number):
        to_remove = []

        #going to the plates of this stiffener (all lines have this number)
        for line1 in self.lines():
            if line1.code.st_number is st_number:

                #if the line is a trapezoid line, it has to be removed and the adjecent ones fused
                if line1.code.pl_type == 0: #trapezoid plate of the stiffener
                    left_tr_pl = None
                    right_tr_pl = None
                    for line_tr in self.lines():
                        if line_tr.code.pl_type == 0 and line_tr.code.tpl_number == line1.code.tpl_number - 1:
                            left_tr_pl = line_tr
                        elif line_tr.code.p1_type == 0 and line_tr.code.tpl_number == line1.tpl_number + 1:
                            right_tr_pl = line_tr
                    #creating a new line that spans over the length of all 3
                    new_code = plate_code.plate_code(line1.code.pl_position, 0, line1.code.tpl_number-1, 0, 0)
                    new_tr_pl = line.line(new_code, left_tr_pl.a, right_tr_pl.b, line1.t)
                    new_tr_pl.t_stress = line1.t_stress
                    self.lines.append(new_tr_pl)
                    to_remove.append(rigth_tr_pl)
                    to_remove.append(left_tr_pl)
                    to_remove.append(line1)

                #if the line is a stiffener line (not trapezoid) it can be removed directly
            elif line.code.pl_type == 1:
                    to_remove.append(line)

        #after the trapezoid line is added and all the ones to go are added to to_remove, all in to_removed can be removed
        for pl in to_remove:
            self.lines.remove(pl)


    """Sub-cross-section / Line Getter-Methods"""

    #method that returns one side/stiffened plate of the cross section
    def get_stiffened_plate(self, side):
        plate_glob = crosssection(0,0,0)
        for line in self.lines:
            if line.code.pl_position == side:
                plate_glob.addline(line)
        return plate_glob

    #method that returns edge plate a of a stiffened plate
    def get_plate_a(self, side):
        plate_a = None
        min_tpl = 10000

        for line in self.lines:
            if line.code.pl_type == 0 and line.code.pl_position == side:
                if line.code.tpl_number <= min_tpl:
                    min_tpl = line.code.tpl_number
                    plate_a = line
        return plate_a

    #method that returns edge plate b of a stiffened plate
    def get_plate_b(self, side):
        plate_b = None
        max_tpl = 0

        for line in self.lines:
            if line.code.pl_type == 0 and line.code.pl_position == side:
                if line.code.tpl_number >= max_tpl:
                    max_tpl = line.code.tpl_number
                    plate_b = line
        return plate_b

    #method that returns the line corresponding to the given code
    #if more than one line is found, the first to be found is returned
    #if no line is found, an assertion is thrown
    def get_line(self, pl_position = None, pl_type = None, tpl_number = None, st_number = None, st_pl_position = None):
        found = False
        for line in self.lines:
            match_pl_position = False
            match_pl_type = False
            match_tpl_number = False
            match_st_number = False
            match_st_pl_position = False
            if pl_position == None or pl_position == line.code.pl_position:
                match_pl_position = True
            if pl_type == None or pl_type == line.code.pl_type:
                match_pl_type = True
            if tpl_number == None or tpl_number == line.code.tpl_number:
                match_tpl_number = True
            if st_number == None or st_number == line.code.st_number:
                match_st_number = True
            if st_pl_position == None or st_pl_position == line.code.st_pl_position:
                match_st_pl_position = True
            found = match_pl_position == True and match_pl_type == True and match_tpl_number == True and match_st_number == True and match_st_pl_position == True
            if found == True:
                return line

        assert found == True, "Line could not be found"


    """General Geometry Methods"""

    #method that rotates the entire cross section about a given angle
    def get_cs_rot(self, angle, stress = False):
        #make a copy of the crosssection
        cs = crosssection(0,0,0)
        for plate in self.lines:
            cs.addline(copy.deepcopy(plate))

        for plate in cs.lines:
            ay = plate.a.y
            az = plate.a.z
            p1y = plate.p1.y
            p1z = plate.p1.z
            by = plate.b.y
            bz = plate.b.z
            p2y = plate.p2.y
            p2z = plate.p2.z
            plate.a.y = math.cos(angle)*ay - math.sin(angle)*az
            plate.a.z = math.sin(angle)*ay + math.cos(angle)*az
            plate.p1.y = math.cos(angle)*p1y - math.sin(angle)*p1z
            plate.p1.z = math.sin(angle)*p1y + math.cos(angle)*p1z
            plate.b.y = math.cos(angle)*by - math.sin(angle)*bz
            plate.b.z = math.sin(angle)*by + math.cos(angle)*bz
            plate.p2.y = math.cos(angle)*p2y - math.sin(angle)*p2z
            plate.p2.z = math.sin(angle)*p2y + math.cos(angle)*p2z

        return cs

    #method that returns the coordinates of the position where the stiffener should be placed
    def get_coordinates(self, location, side):
        plate = self.get_line(pl_position = side, pl_type = 0)
        #bottom or top plate
        if plate.a.z == plate.b.z:
            if plate.a.y > 0:
                y = location * plate.a.y
                z = plate.a.z
            else:
                y = location * plate.b.y
                z = plate.a.z
        #side plates
        else:
            if plate.a.z > plate.b.z:
                y = plate.a.y + location * (plate.b.y-plate.a.y)
                z = plate.a.z + location * (plate.b.z-plate.a.z)
            else:
                y = plate.b.y + location * (plate.a.y-plate.b.y)
                z = plate.b.z + location * (plate.a.z-plate.b.z)
        return y,z

    #method that returns the minimal absolute value of the angle between a plate and the y-axis in rad
    def get_angle(self, side):
        plate = self.get_line(pl_position = side)
        return plate.get_angle_y()


    """ Methods to Calculate the Properties of the Gross Crossection """

    #method that returns the z-coordinate of the center of the gross cross section
    def get_center_z_tot(self, stress = False):
        weighted_a = 0
        for i in self.lines:
            weighted_a = weighted_a + i.get_area_tot(stress)*i.get_center_z_tot(stress)
        return weighted_a/self.get_area_tot(stress)
    #method that returns the y coordinate of the center of the gross cross section
    def get_center_y_tot(self, stress = False):
        weighted_a = 0
        for i in self.lines:
            weighted_a = weighted_a + i.get_area_tot(stress)*i.get_center_y_tot(stress)
        return weighted_a/self.get_area_tot(stress)
    #method that returns the area of the gross cross section
    def get_area_tot(self, stress = False):
        a=0
        for i in self.lines:
            a = a + i.get_area_tot(stress)
        return a
    #method that returns I_y of the gross cross section
    def get_i_y_tot(self, stress = False):
        z_s = self.get_center_z_tot(stress)
        iy_tot = 0
        for i in self.lines:
            iy_tot = iy_tot + i.get_i_y_tot(stress) + (z_s-i.get_center_z_tot(stress))**2 * i.get_area_tot(stress)
        return iy_tot
    #method that returns A_zero for torsional loading
    def get_azero(self, stress = False):
        azero = 0
        for l in self.lines:
            if l.code.pl_type == 0: #crosssection plate
                height = abs(abs(l.a.z) - abs(l.b.z))
                width = 1/2 * (abs(l.a.y) + abs(l.b.y))
                a_line = height * width
                azero += a_line
        printing.printing("\nazero: "+str(math.floor(azero*100)/100), terminal = True)
        return azero


    """Methods to Calculate the Properties of the Effective Crossection """

    #method that returns the z-coordinate of the center of the effective cross section
    def get_center_z_red(self, stress = False):
        weighted_a = 0
        for i in self.lines:
            weighted_a = weighted_a + i.get_area_red(stress)*i.get_center_z_red(stress)
        return weighted_a/self.get_area_red(stress)
    #method that returns the z-coordinate of the center of the effective cross section
    def get_center_y_red(self, stress = False):
        weighted_a = 0
        for i in self.lines:
            weighted_a = weighted_a + i.get_area_red(stress)*i.get_center_y_red(stress)
        return weighted_a/self.get_area_red(stress)
    #method that returns the area of the effective cross section
    def get_area_red(self, stress = False):
        a=0
        for i in self.lines:
            a = a + i.get_area_red(stress)
        return a
    #method that returns I_y of the effective cross section
    def get_i_y_red(self, stress = False):
        z_s = self.get_center_z_red(stress)
        iy_tot = 0
        for i in self.lines:
            iy_tot = iy_tot + i.get_i_y_red(stress) + (z_s-i.get_center_z_red(stress))**2 * i.get_area_red(stress)
        return iy_tot
    #method that returns M_Rd_el_eff
    def get_m_rd_el_eff(self):
        stress = True
        max_z_dis = max(self.get_center_z_red(stress) + self.get_line(pl_position = 1, pl_type = 0).t_stress/2 ,  data.input_data.get("h") + self.get_line(pl_position = 3, pl_type = 0).t_stress/2 - self.get_center_z_red(stress))
        m_rd_el_eff = (self.get_i_y_red(stress) / max_z_dis) * (data.constants.get("f_y")/data.constants.get("gamma_M1"))
        return m_rd_el_eff

    #method that returns the cross sectional value EI of the effective
    def get_ei(self):
        ei = self.get_i_y_red()*data.constants.get("E")
        self.ei = ei
        return ei

    #method that returns M_f_Rd_eff according to EC 3, 1-5, 7.1
    def get_m_f_rd_eff(self):
        stress = True
        top_flange = self.get_stiffened_plate(side = 1)
        top_flange_area = top_flange.get_area_red(stress)
        bottom_flange = self.get_stiffened_plate(side = 3)
        bottom_flange_area = bottom_flange.get_area_red(stress)
        if bottom_flange_area < top_flange_area:
            m_f_rd_eff = bottom_flange_area * self.h * data.constants.get("f_y") / data.constants.get("gamma_M1")
        else:
            m_f_rd_eff = bottom_flange_area * self.h * data.constants.get("f_y") / data.constants.get("gamma_M1")
        return m_f_rd_eff

    #method that calculates the moment of inertia of the gross cross section along the line given as an argument
    #when using this method, always make sure line is a principal axis of the cross section
    def get_i_along_tot(self, line, stress = False):
        angle = (-1)* line.get_angle_y_true()
        cs_rot = self.get_cs_rot(angle, stress)
        return cs_rot.get_i_y_tot(stress)

    #method that calculates the moment of inertia of the reduced cross section along the line given as an argument
    #when using this method, always make sure line is a principal axis of the cross section
    def get_i_along_red(self, line, stress = False):
        angle = (-1)*line.get_angle_y_true()
        cs_rot = self.get_cs_rot(angle, stress)
        return cs_rot.get_i_y_red(stress)
