import math
from classes import point

class line():
#a and b are of starting end ending points of the line
#p1 and p2 are the borders of "active" crosssection regarding effective width
#p1 is closer to A and p2 is closer to B
#t is the thickness of the plate
#p1 and p2 are optional

    #construcor
    def __init__(self, code, a, b, t, p1 = None, p2 = None):
        self.code = code
        self.a = a
        self.b = b
        self.p1 = p1 if p1 is not None else point.point(a.y + 1/2*(b.y - a.y), a.z + 1/2*(b.z-a.z))
        self.p2 = p2 if p2 is not None else point.point(a.y + 1/2*(b.y - a.y), a.z + 1/2*(b.z-a.z))
        self.t = float(t)
        #shear lag is accounted for by reducing the area in stress calculation, this is done by mindering the thickness
        self.t_stress = self.t
        self.beta = 1
        self.rho_c_a = 1
        self.rho_c_b = 1
        #normal stress with tension being negative at point a and point b for the effective crosssection
        self.sigma_a_red = 0
        self.sigma_b_red = 0
        self.sigma_p1_red = 0
        self.sigma_p2_red = 0
        #ratio of sigma at a and b, smaller/larger with tension being negative
        self.psi = 1
        #local plate buckling reduction factor
        self.rho_loc = 1
        #global plate buckling reduction factors
        self.chi_c = 1
        self.sigma_cr_c = 0
        self.rho_p = 1
        self.sigma_cr_p = 0

    #string for print()
    def __str__(self):
        if self.code.pl_type == 0:
            line1 = "   trapezoid plate on side " + str(self.code.pl_position) + "   with the number " + str(self.code.tpl_number) +"\n"
        elif self.code.pl_type == 1:
            line1 = "   stiffener plate on side " + str(self.code.pl_position) + "   of stiffener nr " + str(self.code.st_number) + "    on stiffener plate position " + str(self.code.st_pl_position) + "\n"
        line2 = "           a=" + str(self.a) + "    p1=" + str(self.p1) + "    p2=" + str(self.p2) + "    b=" + str(self.b) + "t=" + str(self.t) + "\n"
        line3 = "           sigma_a_red=" + str(int(100*self.sigma_a_red)/100) + "   sigma_b_red=" + str(int(100*self.sigma_b_red)/100) + "\n"

        string = line1 + line2 + line3
        return string

#p1 should be closer to a and p2 closer to b
    def sanitycheck(self):
        disap1 = math.sqrt((self.a.y - self.p1.y)**2 + (self.a.z - self.p1.z)**2)
        disbp2 = math.sqrt((self.b.y - self.p2.y)**2 + (self.b.z - self.p2.z)**2)
        if disap1 <= self.get_length_tot()/2 and disbp2 <= self.get_length_tot()/2:
            return true
        else:
            return false

#methods to calculate line propreties for non-reduced
    #stress is the boolean defining if the attribute t_stress should be used
    #will be called for cross-sectional stresses and moments, to account for shear lag reductions
    #which are represented by reducing the thickness of flange plates -> t_stress set smaller than
#these getter methods call cal_methods
#the cal methods for non-reduced do not refer to self, thus take the measurements as arguments

    #getter method for center y total area
    def get_center_y_tot(self, stress = False):
        if stress:
            return self.cal_center_y(self.a.y, self.a.z, self.b.y, self.b.z, self.t_stress)
        else:
            return self.cal_center_y(self.a.y, self.a.z, self.b.y, self.b.z, self.t)
    #getter method for center z total area
    def get_center_z_tot(self, stress = False):
        if stress:
            return self.cal_center_z(self.a.y, self.a.z, self.b.y, self.b.z, self.t_stress)
        else:
            return self.cal_center_z(self.a.y, self.a.z, self.b.y, self.b.z, self.t)
    #getter method for total length of plate
    def get_length_tot(self, stress = False):
        if stress:
            return self.cal_length(self.a.y, self.a.z, self.b.y, self.b.z, self.t_stress)
        else:
            return self.cal_length(self.a.y, self.a.z, self.b.y, self.b.z, self.t)
    #getter method for total area of plate (cross-sectional area)
    def get_area_tot(self, stress = False):
        if stress:
            return self.cal_area(self.a.y, self.a.z, self.b.y, self.b.z, self.t_stress)
        else:
            return self.cal_area(self.a.y, self.a.z, self.b.y, self.b.z, self.t)
    #getter method for moment of inertia along the plate (the smaller one of the two)
    def get_i_along_tot(self, stress = False):
        if stress:
            return self.cal_i_along(self.a.y, self.a.z, self.b.y, self.b.z, self.t_stress)
        else:
            return self.cal_i_along(self.a.y, self.a.z, self.b.y, self.b.z, self.t)
    #getter method for the moment of inertia perpendicular to the plate (the bigger one)
    def get_i_perpen_tot(self, stress = False):
        if stress:
            return self.cal_i_perpen(self.a.y, self.a.z, self.b.y, self.b.z, self.t_stress)
        else:
            return self.cal_i_perpen(self.a.y, self.a.z, self.b.y, self.b.z, self.t)
    #getter function for the moment of inertia along the y axis
    def get_i_y_tot(self, stress = False):
        if stress:
            return self.cal_i_y(self.a.y, self.a.z, self.b.y, self.b.z, self.t_stress)
        else:
            return self.cal_i_y(self.a.y, self.a.z, self.b.y, self.b.z, self.t)
    #getter method for the moment of inertia along the z axis
    def get_i_z_tot(self, stress = False):
        if stress:
            return self.cal_i_z(self.a.y, self.a.z, self.b.y, self.b.z, self.t_stress)
        else:
            return self.cal_i_z(self.a.y, self.a.z, self.b.y, self.b.z, self.t)
    #getter method for the moment of inertia along an axis rotated to the y axis with an angle
    def get_i_rot_tot(self, angle, stress = False):
        if stress:
            return self.cal_i_rot(self.a.y, self.a.z, self.b.y, self.b.z, self.t_stress, angle)
        else:
            return self.cal_i_rot(self.a.y, self.a.z, self.b.y, self.b.z, self.t_stress, angle)


#methods to calculate line propreties for reduced
#they follow the same principle as the getter methods for non-reduced
#they cal the cal_methods for non-reduced, they on the other hand refer to the self
    def get_center_y_red(self, stress = False):
        return self.cal_center_y_red(stress)
    def get_center_z_red(self, stress = False):
        return self.cal_center_z_red(stress)
    def get_length_red(self, stress = False):
        return self.cal_length_red(stress)
    def get_area_red(self, stress = False):
        return self.cal_area_red(stress)
    def get_area_red1(self, stress = False):
        return self.cal_area_red1(stress)
    def get_area_red2(self, stress = False):
        return self.cal_area_red2(stress)
    def get_i_along_red(self, stress = False):
        return self.cal_i_along_red(stress)
    def get_i_along_red1(self, stress = False):
        return self.cal_i_along_red1(stress)
    def get_i_along_red2(self, stress = False):
        return self.cal_i_along_red2(stress)
    def get_i_perpen_red(self, stress = False):
        return self.cal_i_perpen_red(stress)
    def get_i_y_red(self, stress = False):
        return self.cal_i_y_red(stress)
    def get_i_z_red(self, stress = False):
        return self.cal_i_z_red(stress)
    def get_i_rot_red(self, angle, stress = False):
        return self.cal_i_rot_red(angle, stress)


#GENERAL (independant of reduced or non-reduced)

    #calculate the smallest angle between the plate and the y axis
    def get_angle_y(self):
        zdis = abs(self.b.z - self.a.z)
        ydis = abs(self.b.y - self.a.y)
        if ydis > 0:
            angle = math.atan(zdis / ydis) #smaller angle between y axis and line, thus should be between 0 and pi/2
        else:
            angle = math.pi/2
        return angle
    #calculate the smallest angle between the plate and the z axis
    def get_angle_z(self):
        complangle = math.pi/2 - self.get_angle_y()
        return complangle

    #does not give the smallest angle but the true angle from the y-axis increasing angle in counter-clockwise direction
    def get_angle_y_true(self):
        dy = self.b.y - self.a.y
        dz = self.b.z - self.a.z

        if dy > 0 and dz == 0:
            angle = 0
        if dy > 0 and dz > 0:
            angle = math.atan(dz/dy)
        if dy == 0 and dz > 0:
            angle = math.pi / 2
        if dy < 0 and dz > 0:
            angle = math.atan(dz/dy)
        if dy < 0 and dz == 0:
            angle = math.pi
        if dy < 0 and dz < 0:
            angle = math.pi + math.atan(dz / dy)
        if dy == 0 and dz < 0:
            angle = 3/2*math.pi
        if dy > 0 and dz < 0:
            angle = 2*math.pi + math.atan(dz / dy)

        #horizontal is not 0 degrees but pi (line from positive y to negative)
        angle -= math.pi
        return angle"""

    #get the stress at the point that is the fraction factor of the total length away from point a
    def get_sigma_red_from_a(self, factor):
        return self.sigma_a_red + factor*(self.sigma_b_red - self.sigma_a_red)
    #get the stress at the point that is the fraction factor of the total length away from point b
    def get_sigma_red_from_b(self, factor):
        return self.sigma_b_red + factor*(self.sigma_a_red - self.sigma_b_red)

#NON-REDUCED (and also used for reduced, that's why with coordinates as arguments)
#these functions only use the given arguments and do not refer to self, so that they can also be used from non-reduced methods
    def cal_center_y(self, ay, az, by, bz, t):
        return 1/2 * (ay + by)
    def cal_center_z(self, ay, az, by, bz, t):
        return 1/2 * (az + bz)
    def cal_length(self, ay, az, by, bz, t):
        return math.sqrt((ay - by)**2 + (az - bz)**2)
    def cal_area(self, ay, az, by, bz, t):
        return self.cal_length(ay, az, by, bz, t) * t
    def cal_i_along(self, ay, az, by, bz, t):
        return t**3 * self.cal_length(ay, az, by, bz, t) / 12
    def cal_i_perpen(self, ay, az, by, bz, t):
        return self.cal_length(ay, az, by, bz, t)**3 * t / 12
    def cal_i_y(self, ay, az, by, bz, t):
        angle = self.get_angle_y()
        return math.cos(angle)**2 * self.cal_i_along(ay, az, by, bz, t) + math.sin(angle)**2 * self.cal_i_perpen(ay, az, by, bz, t)
    def cal_i_z(self, ay, az, by, bz, t):
        complangle = self.get_angle_z()
        return math.cos(complangle)**2 * self.cal_i_along(ay, az, by, bz, t) + math.sin(complangle)**2 * self.cal_i_perpen(ay, az, by, bz, t)
    def cal_i_rot(self, ay, az, by, bz, t, angle):
        return math.cos(angle)**2 * self.cal_i_along(ay, az, by, bz, t) + math.sin(angle)**2 * self.cal_i_perpen(ay, az, by, bz, t)


#FOR REDUCED
    def cal_center_y_red(self, stress = False):
        if stress:
            t_used = self.t_stress
        else:
            t_used = self.t
        length_red1 = self.rho_c_a * self.cal_length(self.a.y, self.a.z, self.p1.y, self.p1.z, t_used)
        length_red2 = self.rho_c_b * self.cal_length(self.b.y, self.b.z, self.p2.y, self.p2.z, t_used)
        if length_red1 == 0 and length_red2 == 0:
            return self.cal_center_y(self.a.y, self.a.z, self.b.y, self.b.z, self.t)
            weight_1 = 0
            weight_2 = 0
        else:
            weight_1 = length_red1/(length_red1+length_red2)
            weight_2 = length_red2 /(length_red1+length_red2)
            center_y_red1 = self.cal_center_y(self.a.y, self.a.z, self.p1.y, self.p1.z, t_used)
            center_y_red2 = self.cal_center_y(self.b.y, self.b.z, self.p2.y, self.p2.z, t_used)
            center = center_y_red1 * weight_1 + center_y_red2 * weight_2
            return center
    def cal_center_z_red(self, stress = False):
        if stress:
            t_used = self.t_stress
        else:
            t_used = self.t
        length_red1 = self.rho_c_a * self.cal_length(self.a.y, self.a.z, self.p1.y, self.p1.z, t_used)
        length_red2 = self.rho_c_b * self.cal_length(self.b.y, self.b.z, self.p2.y, self.p2.z, t_used)
        if length_red1 == 0 and length_red2 == 0:
            return self.cal_center_z(self.a.y, self.a.z, self.b.y, self.b.z, self.t)
            weight_1 = 0
            weight_2 = 0
        else:
            weight_1 = length_red1/(length_red1+length_red2)
            weight_2 = length_red2 /(length_red1+length_red2)
            center_z_red1 = self.cal_center_z(self.a.y, self.a.z, self.p1.y, self.p1.z, t_used)
            center_z_red2 = self.cal_center_z(self.b.y, self.b.z, self.p2.y, self.p2.z, t_used)
            center = center_z_red1 * weight_1 + center_z_red2 * weight_2
            return center
    def cal_length_red(self, stress = False):
        if stress:
            t_used = self.t_stress
        else:
            t_used = self.t
        return self.rho_c_a * self.cal_length(self.a.y, self.a.z, self.p1.y, self.p1.z, t_used) + \
        self.rho_c_b * self.cal_length(self.p2.y, self.p2.z, self.b.y, self.b.z, t_used)
    def cal_area_red(self, stress = False):
        if stress:
            t_used = self.t_stress
        else:
            t_used = self.t
        return self.rho_c_a * self.cal_area(self.a.y, self.a.z, self.p1.y, self.p1.z, t_used) + \
        self.rho_c_b * self.cal_area(self.p2.y, self.p2.z, self.b.y, self.b.z, t_used)
    def cal_area_red1(self, stress = False):
        if stress:
            t_used = self.t_stress
        else:
            t_used = self.t
        return self.rho_c_a * self.cal_area(self.a.y, self.a.z, self.p1.y, self.p1.z, t_used)
    def cal_area_red2(self, stress = False):
        if stress:
            t_used = self.t_stress
        else:
            t_used = self.t
        return self.rho_c_b * self.cal_area(self.p2.y, self.p2.z, self.b.y, self.b.z, t_used)
    def cal_i_along_red(self, stress = False):
        if stress:
            t_used = self.t_stress
        else:
            t_used = self.t
        return self.cal_i_along(self.a.y, self.a.z, self.p1.y, self.p1.z, t_used) + self.cal_i_along(self.b.y, self.b.z, self.p2.y, self.p2.z, t_used)
    def cal_i_along_red1(self, stress = False):
        if stress:
            t_used = self.t_stress
        else:
            t_used = self.t
        return self.rho_c_a**3 * self.cal_i_along(self.a.y, self.a.z, self.p1.y, self.p1.z, t_used)
    def cal_i_along_red2(self, stress = False):
        if stress:
            t_used = self.t_stress
        else:
            t_used = self.t
        return self.rho_c_b**3 * self.cal_i_along(self.b.y, self.b.z, self.p2.y, self.p2.z, t_used)
    def cal_i_perpen_red(self, stress = False):
        if stress:
            t_used = self.t_stress
        else:
            t_used = self.t
        i_perpen_red1 = self.rho_c_a * self.cal_i_perpen(self.a.y, self.a.z, self.p1.y, self.p1.z, t_used)
        i_perpen_red2 = self.rho_c_b * self.cal_i_perpen(self.b.y, self.b.z, self.p2.y, self.p2.z, t_used)
        dis1 = math.sqrt((abs(self.cal_center_y_red()) - abs(self.cal_center_y(self.a.y, self.a.z, self.p1.y, self.p1.z, t_used)))**2 + (abs(self.cal_center_z_red())-abs(self.cal_center_z(self.a.y, self.a.z, self.p1.y, self.p1.z, t_used)))**2)
        dis2 = math.sqrt((abs(self.cal_center_y_red()) - abs(self.cal_center_y(self.b.y, self.b.z, self.p2.y, self.p2.z, t_used)))**2 + (abs(self.cal_center_z_red())-abs(self.cal_center_z(self.b.y, self.b.z, self.p2.y, self.p2.z, t_used)))**2)
        steiner1 = self.rho_c_a * self.cal_area(self.a.y, self.a.z, self.p1.y, self.p1.z, t_used) * dis1**2
        steiner2 = self.rho_c_b * self.cal_area(self.b.y, self.b.z, self.p2.y, self.p2.z, t_used) * dis2**2
        i_perpen_red1_withsteiner = i_perpen_red1 + steiner1
        i_perpen_red2_withsteiner = i_perpen_red2 + steiner2
        return i_perpen_red1_withsteiner + i_perpen_red2_withsteiner
    def cal_i_y_red(self, stress = False):
        angle = self.get_angle_y()
        return math.cos(angle)**2 * self.cal_i_along_red(stress) + math.sin(angle)**2 * self.cal_i_perpen_red(stress)
    def cal_i_z_red(self, stress = False):
        complangle = self.get_angle_z()
        return math.cos(complangle)**2 * self.cal_i_along_red(stress) + math.sin(complangle)**2 * self.cal_i_perpen_red(stress)
    def cal_i_rot_red(self, angle, stress = False):
        return math.cos(angle)**2 * self.cal_i_along_red(stress) + math.sin(angle)**2 * self.cal_i_perpen_red(stress)
