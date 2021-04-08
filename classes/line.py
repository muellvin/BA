from classes import point
import math

class line():
#a and b are of starting end ending points of the line
#p1 and p2 are the borders of "active" crosssection regarding effective width
#p1 is closer to A and p2 is closer to B
#t is the thickness of the plate
#p1 and p2 are optional
    def __init__(self, code, a, b, t, p1 = None, p2 = None):
        self.code = code
        self.a = a
        self.b = b
        self.p1 = p1 if p1 is not None else point.point(a.y + 1/2*(b.y - a.y), a.z + 1/2*(b.z-a.z))
        self.p2 = p2 if p1 is not None else point.point(a.y + 1/2*(b.y - a.y), a.z + 1/2*(b.z-a.z))
        self.t = float(t)
        self.beta = 1
        self.rohc1 = 1
        self.rohc2 = 1
        #normal stress with tension being positive at point a and point b for the effective crosssection
        self.sigma_a_red = 0
        self.sigma_b_red = 0
        #ratio of sigma at a and b, smaller/larger with tension being negative
        self.psi = 1
        #local plate buckling reduction factor
        self.rho_loc = 1
        #global plate buckling reduction factor from interaction plate and column
        self.rho_c = 1

#p1 should be closer to a and p2 closer to b
    def sanitycheck(self):
        disap1 = math.sqrt((self.a.y - self.p1.y)**2 + (self.a.z - self.p1.z)**2)
        disbp2 = math.sqrt((self.b.y - self.p2.y)**2 + (self.b.z - self.p2.z)**2)
        if disap1 <= self.get_length_tot()/2 and disbp2 <= self.get_length_tot()/2:
            return true
        else:
            return false


#methods to calculate line propreties for non-reduced
    def get_center_y_tot(self):
        return self.cal_center_y(self.a.y, self.a.z, self.b.y, self.b.z, self.t)
    def get_center_z_tot(self):
        return self.cal_center_z(self.a.y, self.a.z, self.b.y, self.b.z, self.t)
    def get_length_tot(self):
        return self.cal_length(self.a.y, self.a.z, self.b.y, self.b.z, self.t)
    def get_area_tot(self):
        return self.cal_area(self.a.y, self.a.z, self.b.y, self.b.z, self.t)
    def get_i_along_tot(self):
        return self.cal_i_along(self.a.y, self.a.z, self.b.y, self.b.z, self.t)
    def get_i_perpen_tot(self):
        return self.cal_i_perpen(self.a.y, self.a.z, self.b.y, self.b.z, self.t)
    def get_i_y_tot(self):
        return self.cal_i_y(self.a.y, self.a.z, self.b.y, self.b.z, self.t)
    def get_i_z_tot(self):
        return self.cal_i_z(self.a.y, self.a.z, self.b.y, self.b.z, self.t)
    def get_i_rot_tot(self, angle):
        return self.cal_i_rot(self.a.y, self.a.z, self.b.y, self.b.z, self.t, angle)


#methods to calculate line propreties for reduced
    def get_center_y_red(self):
        return self.cal_center_y_red()
    def get_center_z_red(self):
        return self.cal_center_z_red()
    def get_length_red(self):
        return self.cal_length_red()
    def get_area_red(self):
        return self.cal_area_red()
    def get_area_red1(self):
        return self.cal_area_red1()
    def get_area_red2(self):
        return self.cal_area_red2()
    def get_i_along_red(self):
        return self.cal_i_along_red()
    def get_i_along_red1(self):
        return self.cal_i_along_red1()
    def get_i_along_red2(self):
        return self.cal_i_along_red2()    
    def get_i_perpen_red(self):
        return self.cal_i_perpen_red()
    def get_i_y_red(self):
        return self.cal_i_y_red()
    def get_i_z_red(self):
        return self.cal_i_z_red()
    def get_i_rot_red(self, angle):
        return self.cal_i_rot_red(angle)


#GENERAL
    def cal_angle_y(self):
        zdis = abs(self.b.z - self.a.z)
        ydis = abs(self.b.y - self.a.y)
        if ydis > 0:
            angle = math.atan(zdis / ydis) #smaller angle between y axis and line, thus should be between 0 and pi/2
        else:
            angle = math.pi/2
        return angle
    def cal_angle_z(self):
        complangle = math.pi/2 - self.cal_angle_y()
        return complangle


#NON-REDUCED (and also used for reduced, that's why with coordinates as arguments)
    def cal_center_y(self, ay, az, by, bz, t):
        return 1/2 * (ay + by)
    def cal_center_z(self, ay, az, by, bz, t):
        return 1/2 * (az + bz)
    def cal_length(self, ay, az, by, bz, t):
        return math.sqrt((ay - by)**2 + (az - bz)**2)
    def cal_area(self, ay, az, by, bz, t):
        return self.cal_length(ay, az, by, bz, t) * self.t
    def cal_i_along(self, ay, az, by, bz, t):
        return self.t**3 * self.cal_length(ay, az, by, bz, t) / 12
    def cal_i_perpen(self, ay, az, by, bz, t):
        return self.cal_length(ay, az, by, bz, t)**3 * self.t / 12
    def cal_i_y(self, ay, az, by, bz, t):
        angle = self.cal_angle_y()
        return math.cos(angle)**2 * self.cal_i_along(ay, az, by, bz, t) + math.sin(angle)**2 * self.cal_i_perpen(ay, az, by, bz, t)
    def cal_i_z(self, ay, az, by, bz, t):
        complangle = self.cal_angle_z()
        return math.cos(complangle)**2 * self.cal_i_along(ay, az, by, bz, t) + math.sin(complangle)**2 * self.cal_i_perpen(ay, az, by, bz, t)
    def cal_i_rot(self, ay, az, by, bz, t, angle):
        return math.cos(angle)**2 * self.cal_i_along(ay, az, by, bz, t) + math.sin(angle)**2 * self.cal_i_perpen(ay, az, by, bz, t)


#FOR REDUCED
    def cal_center_y_red(self):
        length_red1 = self.cal_length(self.a.y, self.a.z, self.p1.y, self.p1.z, self.t)
        length_red2 = self.cal_length(self.b.y, self.b.z, self.p2.y, self.p2.z, self.t)
        weight_1 = length_red1/(length_red1+length_red2)
        weight_2 = length_red2 /(length_red1+length_red2)
        center_y_red1 = self.cal_center_y(self.a.y, self.a.z, self.p1.y, self.p1.z, self.t)
        center_y_red2 = self.cal_center_y(self.b.y, self.b.z, self.p2.y, self.p2.z, self.t)
        center = center_y_red1 * weight_1 + center_y_red2 * weight_2
        return center
    def cal_center_z_red(self):
        length_red1 = self.cal_length(self.a.y, self.a.z, self.p1.y, self.p1.z, self.t)
        length_red2 = self.cal_length(self.b.y, self.b.z, self.p2.y, self.p2.z, self.t)
        weight1 = length_red1 /(length_red1+length_red2)
        weight2 = length_red2 /(length_red1+length_red2)
        center_z_red1 = self.cal_center_z(self.a.y, self.a.z, self.p1.y, self.p1.z, self.t)
        center_z_red2 = self.cal_center_z(self.b.y, self.b.z, self.p2.y, self.p2.z, self.t)
        center = center_z_red1 * weight1 + center_z_red2 * weight2
        return center
    def cal_length_red(self):
        return self.cal_length(self.a.y, self.a.z, self.p1.y, self.p1.z, self.t) + self.cal_length(self.p2.y, self.p2.z, self.b.y, self.b.z, self.t)
    def cal_area_red(self):
        return self.cal_area(self.a.y, self.a.z, self.p1.y, self.p1.z, self.t) + self.cal_area(self.p2.y, self.p2.z, self.b.y, self.b.z, self.t)
    def cal_area_red1(self):
        return self.cal_area(self.a.y, self.a.z, self.p1.y, self.p1.z, self.t)
    def cal_area_red2(self):
        return self.cal_area(self.p2.y, self.p2.z, self.b.y, self.b.z, self.t)
    def cal_i_along_red(self):
        return self.cal_i_along(self.a.y, self.a.z, self.p1.y, self.p1.z, self.t) + self.cal_i_along(self.b.y, self.b.z, self.p2.y, self.p2.z, self.t)
    def cal_i_along_red1(self):
        return self.cal_i_along(self.a.y, self.a.z, self.p1.y, self.p1.z, self.t)
    def cal_i_along_red2(self):
        return self.cal_i_along(self.b.y, self.b.z, self.p2.y, self.p2.z, self.t)
    def cal_i_perpen_red(self):
        i_perpen_red1 = self.cal_i_perpen(self.a.y, self.a.z, self.p1.y, self.p1.z, self.t)
        i_perpen_red2 = self.cal_i_perpen(self.b.y, self.b.z, self.p2.y, self.p2.z, self.t)
        dis1 = math.sqrt((abs(self.cal_center_y_red()) - abs(self.cal_center_y(self.a.y, self.a.z, self.p1.y, self.p1.z, self.t)))**2 + (abs(self.cal_center_z_red())-abs(self.cal_center_z(self.a.y, self.a.z, self.p1.y, self.p1.z, self.t)))**2)
        dis2 = math.sqrt((abs(self.cal_center_y_red()) - abs(self.cal_center_y(self.b.y, self.b.z, self.p2.y, self.p2.z, self.t)))**2 + (abs(self.cal_center_z_red())-abs(self.cal_center_z(self.b.y, self.b.z, self.p2.y, self.p2.z, self.t)))**2)
        steiner1 = self.cal_area(self.a.y, self.a.z, self.p1.y, self.p1.z, self.t) * dis1**2
        steiner2 = self.cal_area(self.b.y, self.b.z, self.p2.y, self.p2.z, self.t) * dis2**2
        i_perpen_red1_withsteiner = i_perpen_red1 + steiner1
        i_perpen_red2_withsteiner = i_perpen_red2 + steiner2
        return i_perpen_red1_withsteiner + i_perpen_red2_withsteiner
    def cal_i_y_red(self):
        angle = self.cal_angle_y()
        return math.cos(angle)**2 * self.cal_i_along_red() + math.sin(angle)**2 * self.cal_i_perpen_red()
    def cal_i_z_red(self):
        complangle = self.cal_angle_z()
        return math.cos(complangle)**2 * self.get_i_along_red() + math.sin(complangle)**2 * self.cal_i_perpen_red()
    def cal_i_rot_red(self, angle):
        return math.cos(angle)**2 * self.cal_i_along_red() + math.sin(angle)**2 * self.cal_i_perpen_red()
