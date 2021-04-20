from classes import line
import math
import data
import copy

#crosssection calculation
class crosssection():
#a crosssection is defined as a list of lines
    def __init__(self, b_sup, b_inf, h):
        self.lines = []
        self.b_sup = b_sup
        self.b_inf = b_inf
        self.h = h

    def __str__(self):
        string = "\n cross-section with b_sup=" + str(self.b_sup) + ", b_inf=" + str(self.b_inf) + ", h=" + str(self.h) + "\n"
        for line in self.lines:
            string += str(line)
        return string

    def addline(self, line):
        self.lines.append(line)

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



    def get_angle(self, side):
        line = self.get_line(pl_position = side)
        return line.get_angle_y()

    #This function returns the coordinates of the position where the stiffener should be placed
    def get_coordinates(self, location, side):
        line = self.get_line(pl_position = side)
        #bottom or top plate
        if line.a.z == line.b.z:
            if line.a.y > 0:
                y = location * line.a.y
                z = line.a.z
            else:
                y = location * line.b.y
                z = line.a.z
        #side plates
        else:
            if line.a.z > line.b.z:
                y = line.a.y + location * (line.b.y-line.a.y)
                z = line.a.z + location * (line.b.z-line.a.z)
            else:
                y = line.b.y + location * (line.a.y-line.b.y)
                z = line.b.z + location * (line.a.z-line.b.z)
        return y,z





# methods to calculate properties of total crossection
    def get_center_z_tot(self):
        weighted_a = 0
        for i in self.lines:
            weighted_a = weighted_a + i.get_area_tot()*i.get_center_z_tot()
        return weighted_a/self.get_area_tot()
    def get_center_y_tot(self):
        weighted_a = 0
        for i in self.lines:
            weighted_a = weighted_a + i.get_area_tot()*i.get_center_y_tot()
        return weighted_a/self.get_area_tot()
    def get_area_tot(self):
        a=0
        for i in self.lines:
            a = a + i.get_area_tot()
        return a
#functionality of inertial area moments function not tested yet
    def get_i_y_tot(self):
        z_s = self.get_center_z_tot()
        iy_tot = 0
        for i in self.lines:
            iy_tot = iy_tot + i.get_i_y_tot() + (z_s-i.get_center_z_tot())**2 * i.get_area_tot()
        return iy_tot
    def get_i_z_tot(self):
        y_s = self.get_center_y_tot()
        iz_tot = 0
        for i in self.lines:
            iz_tot = iz_tot + i.get_i_z_tot() + (y_s-i.get_center_y_tot())**2 * i.get_area_tot()
        return iz_tot


#methods to calculate properties of reduced crossection
#center functions for reduced crosssections still need to be properly defined
    def get_center_z_red(self):
        weighted_a = 0
        for i in self.lines:
            weighted_a = weighted_a + i.get_area_red()*i.get_center_z_red()
        return weighted_a/self.get_area_red()
    def get_center_y_red(self):
        weighted_a = 0
        for i in self.lines:
            weighted_a = weighted_a + i.get_area_red()*i.get_center_y_red()
        return weighted_a/self.get_area_red()
    def get_area_red(self):
        a=0
        for i in self.lines:
            a = a + i.get_area_red()
        return a
    def get_i_y_red(self):
        z_s = self.get_center_z_red()
        iy_tot = 0
        for i in self.lines:
            iy_tot = iy_tot + i.get_i_y_red() + (z_s-i.get_center_z_red())**2 * i.get_area_red()
        return iy_tot
    def get_i_z_red(self):
        y_s = self.get_center_y_red()
        iz_tot = 0
        for i in self.lines:
            iz_tot = iz_tot + i.get_i_z_red() + (y_s-i.get_center_y_red())**2 * i.get_area_red()
        return iz_tot

    def get_m_rd_el_eff(self):
            max_z_dis = max(self.get_center_z_red() + self.get_line(pl_position = 1, pl_type = 0).t/2 ,  data.input_data.get("h") + self.get_line(pl_position = 3, pl_type = 0).t/2 - self.get_center_z_red())
            m_rd_el_eff = (self.get_i_y_red() / max_z_dis) * (data.constants.get("f_y")/data.constants.get("gamma_M1"))
            return m_rd_el_eff


    def get_azero(self):
        azero = 0
        for l in self.lines:
            if l.code.pl_type == 0: #crosssection plate
                height = abs(abs(l.a.z) - abs(l.b.z))
                width = 1/2 * (abs(l.a.y) + abs(l.b.y))
                a_line = height * width
                azero += a_line
        return azero

    def get_cs_rot(self, angle):
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

    #calculates the moment of inertia along the line given as an argument
    def get_i_along_tot(self, line):
        angle = (-1)* line.get_angle_y_true()
        print(angle/math.pi)
        cs_rot = self.get_cs_rot(angle)
        return cs_rot.get_i_y_tot()


    def get_i_along_red(self, line):
        #make a copy of the crosssection
        cs = crosssection(0,0,0)
        for line in self.lines:
            cs.addline(line)

        angle = line.get_angle_y()

        for plate in cs.lines:
            ay = plate.a.y
            az = plate.a.z
            by = plate.b.y
            bz = plate.b.z
            plate.a.y = math.cos(angle)*ay - math.sin(angle)*az
            plate.a.z = math.sin(angle)*ay + math.cos(angle)*az
            plate.b.y = math.cos(angle)*by - math.sin(angle)*bz
            plate.b.z = math.sin(angle)*by + math.cos(angle)*bz

        return cs.get_i_y_red()


    """ important convention: the point b of a line is always in clockwise direction of point a"""

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
