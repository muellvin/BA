from classes import line
import math

#crosssection calculation
class crosssection():
#a crosssection is defined as a list of lines
    def __init__(self, b_sup, b_inf, h):
        self.lines = []
        self.b_sup = b_sup
        self.b_inf = b_inf
        self.b = h

    def addline(self, line):
        self.lines.append(line)

    def get_line_code(self, code):
        success = 0
        for line in self.lines:
            if line.code == code:
                success = 1
                return line
            else:
                pass
        assert success != 0, "Line could not be found."

    #to get certain line of stiffener
    def get_line(self, pl_position, st_pl_position):
        success = 0
        for i in self.lines:
            if i.code.pl_position == pl_position and i.code.st_pl_position == st_pl_position:
                success = 1
                return i
            else:
                pass
        assert success != 0, "Line could not be found."


    #to get trapezoid plates from initial cs -> to add stiffeners
    def get_pl_line(self, pl_position):
        for i in self.lines:
            if i.code.pl_position == pl_position:
                return i
        else:
            print("You are stupid!")
            return

    def get_angle(self, code):
        line = self.get_line_code(code)
        return line.cal_angle_y()

    #This function returns the coordinates of the position where the stiffener should be placed
    def get_coordinates(self, location, code):
        line = self.get_line_code(code)
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
    #
    def get_stiffener_line(self, pl_position, st_number, st_pl_position):
        for i in self.lines:
            if i.code.pl_position == pl_position and i.code.st_number == st_number \
            and i.code.st_pl_position == st_pl_position:
                return i


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

    def get_azero(self):
        azero = 0
        for l in self.lines:
            if l.code.pl_type == 0: #crosssection plate
                height = abs(abs(l.a.z) - abs(l.b.z))
                width = 1/2 * (abs(l.a.y) + abs(l.b.y))
                a_line = height * width
                azero += a_line
        return azero


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




    #method that renumbers all the lines again correctly
    def renumber(self):
        pass
        #tpl_number, st_number need to be adjusted
