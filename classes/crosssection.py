from classes import line
import math

#crosssection calculation
class crosssection():
#a crosssection is defined as a list of lines
    def __init__(self):
        self.lines = []

    def addline(self, line):
        self.lines.append(line)


    def get_line(self, pl_position, pl_type, st_pl_position):
        for i in self:
            if i.code.pl_position is pl_position and i.code.pl_type is pl_type and i.code.st_pl_position is st_pl_position:
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
        for l in lines:
            if l.code.pl_type = 0: #crosssection plate
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
                if line1.code.pl_type is 0: #trapezoid plate of the stiffener
                    left_tr_pl = None
                    right_tr_pl = None
                    for line_tr in self.lines():
                        if line_tr.code.pl_type is 0 and line_tr.code.tpl_number is line1.code.tpl_number - 1:
                            left_tr_pl = line_tr
                        elif line_tr.code.p1_type is 0 and line_tr.code.tpl_number is line1.tpl_number + 1:
                            right_tr_pl = line_tr
                    #creating a new line that spans over the length of all 3
                    new_code = plate_code.plate_code(line1.code.pl_position, 0, line1.code.tpl_number-1, 0, 0)
                    new_tr_pl = line.line(new_code, left_tr_pl.a, right_tr_pl.b, line1.t)
                    self.lines.append(new_tr_pl)
                    to_remove.append(rigth_tr_pl)
                    to_remove.append(left_tr_pl)
                    to_remove.append(line1)

                #if the line is a stiffener line (not trapezoid) it can be removed directly
                elif line.code.pl_type is 1:
                    to_remove.append(line)

        #after the trapezoid line is added and all the ones to go are added to to_remove, all in to_removed can be removed
        for pl in to_remove:
            self.lines.remove(pl)


    #method that renumbers all the lines again correctly
    def renumber(self):
        #tpl_number, st_number need to be adjusted



    #method that will be called by the optimizer
    def add_stiffener(self, pl_position, location, i_along):
        #important for the creation of the stiffener is the position and the moment of inertia along the plate where it is placed
        #assumptions: symmetric distribution of stiffeners along z axis
        #pl_position, same as plate_code
        #location: between 0 and 1:
            #for top/ bottom it is the distance to the symmetry axis as a ratio to the max (width/2)
            #for the sides it is the ratio of z value to the height of the cross-section
        #i_along is the moment of inertia along the plate to which it is added
        """code der im file stiffener mit der Methode get_i_along_stiffener, viele ausprobiert und mittels geometrischen beschränkungen entscheidet welche"""
        pass
