#classes

import math

class point():
#origin: symmetry axis and track plate
#usual civil engineering coordinates: z down, y out of paper (to the left)
    def __init__(self, y, z):
        self.y = y
        self.z = z

    def __str__(self):
        return "Point at (" + self.y + ", " + self.z + ")"


class line():
#code for identification: position, type, number, pos in profile
#a and b are of starting end ending points of the line
#p1 and p2 are the borders of "active" crosssection regarding effective width
#p1 is closer to A and p2 is closer to B
#t is the thickness of the plate
#p1 and p2 are optional
    def __init__(self, code, a, b, t, p1 = None, p2 = None):
        self.code = code
        self.a = a
        self.b = b
        self.p1 = p1 if p1 is not None else point(a.y + (a.y-b.y), a.z + (a.z-b.z))
        self.p2 = p2 if p1 is not None else point(a.y + (a.y-b.y), a.z + (a.z-b.z))
        self.t = t

#p1 should be closer to a and p2 closer to b
    def sanitycheck(self):
        disap1 = math.sqrt((self.a.y - self.p1.y)^2 + (self.a.z - self.p1.z)^2)
        disbp2 = math.sqrt((self.b.y - self.p2.y)^2 + (self.b.z - self.p2.z)^2)
        if disap1 <= self.get_length_tot()/2 and disbp2 <= self.get_length_tot()/2:
            return true
        else:
            return false

#methods to calculate line propreties for non-reduced
    def get_length_tot(self):
        return self.cal_length(self.a.y, self.a.z, self.b.y, self.b.z, self.t)
    def get_area_tot(self):
        return self.cal_area(self.a.y, self.a.z, self.b.y, self.b.z, self.t)
    def get_ialong_tot(self):
        return self.cal_ialong(self.a.y, self.a.z, self.b.y, self.b.z, self.t)
    def get_iperpen_tot(self):
        return self.cal_perpen(self.a.y, self.a.z, self.b.y, self.b.z, self.t)
    def get_iy_tot(self):
        return self.cal_iy(self.a.y, self.a.z, self.b.y, self.b.z, self.t)
    def get_iz_tot(self):
        return self.cal_iz(self.a.y, self.a.z, self.b.y, self.b.z, self.t)

#methods to calculate line propreties for reduced
    def get_length_red1(self):
        return self.cal_length(self.a.y, self.a.z, self.p1.y, self.p1.z, self.t)
    def get_length_red2(self):
        return self.cal_length(self.b.y, self.b.z, self.p2.y, self.p2.z, self.t)
    def get_area_red1(self):
        return self.cal_area(self.a.y, self.a.z, self.p1.y, self.p1.z, self.t)
    def get_area_red2(self):
        return self.cal_area(self.b.y, self.b.z, self.p2.y, self.p2.z, self.t)
    def get_ialong_red(self):
        return self.cal_ialong(self.a.y, self.a.z, self.p1.y, self.p1.z, self.t) + self.cal_ialong(self.b.y, self.b.z, self.p2.y, self.p2.z, self.t)
    def get_iperpen_red(self):
        iperpen_red1 = self.cal_perpen(self.a.y, self.a.z, self.p1.y, self.p1.z, self.t)
        iperpen_red2 = self.cal_perpen(self.b.y, self.b.z, self.p2.y, self.p2.z, self.t)
        iperpen_red1_withsteiner = self.cal_iperpen(self.a.y, self.a.z, self.p1.y, self.p1.z, self.t) + self.cal_area(self.a.y, self.a.z, self.p1.y, self.p1.z, self.t) * (self.cal_center_along(self.a.y, self.a.z, self.b.y, self.b.z, self.t) - self.cal_center_along(self.a.y, self.a.z, self.p1.y, self.p1.z, self.t))^2
        iperpen_red2_withsteiner = self.cal_iperpen(self.b.y, self.b.z, self.p2.y, self.p2.z, self.t) + self.cal_area(self.b.y, self.b.z, self.p2.y, self.p2.z, self.t) * (self.cal_center_along(self.a.y, self.a.z, self.b.y, self.b.z, self.t) - self.cal_center_along(self.b.y, self.b.z, self.p2.y, self.p2.z, self.t))^2
        return iperpen_red1_withsteiner + iperpen_red2_withsteiner
    #the iy and iz functions do not work with the general ones, as the
    def get_iy_red(self):
        bz = self.b.z
        az = self.a.z
        by = self.b.y
        ay = self.a.y
        zdis = abs(bz - az)
        ydis = abs(by - ay)
        angle = math.atan(zdis / ydis) #smaller angle between y axis and line, thus should be between 0 and pi
        assert angle >= 0, "getiy and getiz function are faulty"
        assert angle <= math.pi, "getiy and getiz function are faulty"
        return math.cos(angle)^2 * self.get_i_along_red() + math.sin(angle)^2 * self.get_iperpen_red()
    def get_iz_red(self):
        bz = self.b.z
        az = self.a.z
        by = self.b.y
        ay = self.a.y
        zdis = abs(bz - az)
        ydis = abs(by - ay)
        angle = math.atan(zdis / ydis) #smaller angle between y axis and line, thus should be between 0 and pi
        assert angle >= 0, "getiy and getiz function are faulty"
        assert angle <= math.pi, "getiy and getiz function are faulty"
        complangle = math.pi - angle
        return math.cos(complangle)^2 * self.get_ialong_red() + math.sin(complangle)^2 * self.cal_iperpen_red()

#general calculation methods so that they can be used for both reduced and non-reduced
    def cal_centeryz(self, ay, az, by, bz, t):
        yc = 1/2 * (ay + by)
        zc = 1/2 * (az + bz)
        return yc, zc
    def cal_center_along(self, ay, az, by, bz, t):
        return 1/2 * self.cal_length(ay, az, by, bz, t)
    def cal_length(self, ay, az, by, bz, t):
        return math.sqrt((ay - by)^2 + (az - bz)^2)
    def cal_area(self, ay, az, by, bz, t):
        return self.cal_length(ay, az, by, bz) * t
    def cal_ialong(self, ay, az, by, bz, t):
        return t^3 * self.cal_length(ay, az, by, bz, t) / 12
    def cal_iperpen(self, ay, az, by, bz, t):
        return self.cal_length(ay, az, by, bz, t)^3 * t / 12
#moments of inertia along y and z are created with a tensor rotation of i_along and i_perpen
#it uses the fact that the line is symmetric in two axis and it does not matter weather we rotate in positive or negative angle direction
#thus it calculates with absolute length and minimal angle
    def cal_iy(self, ay, az, by, bz, t):
        zdis = abs(bz - az)
        ydis = abs(by - ay)
        angle = math.atan(zdis / ydis) #smaller angle between y axis and line, thus should be between 0 and pi
        assert angle >= 0, "getiy and getiz function are faulty"
        assert angle <= math.pi, "getiy and getiz function are faulty"
        return math.cos(angle)^2 * self.cal_ialong(ay, az, by, bz, t) + math.sin(angle)^2 * self.cal_iperpen(ay, az, by, bz, t)
    def cal_iz(self, ay, az, by, bz, t):
        zdis = abs(bz - az)
        ydis = abs(by - ay)
        angle = math.atan(zdis / ydis) #smaller angle between y axis and line, thus should be between 0 and pi
        assert angle >= 0, "getiy and getiz function are faulty"
        assert angle <= math.pi, "getiy and getiz function are faulty"
        complangle = math.pi - angle
        return math.cos(complangle)^2 * self.cal_ialong(ay, az, by, bz, t) + math.sin(complangle)^2 * self.cal_iperpen(ay, az, by, bz, t)



class cs():
#a crosssection is defined as a list of lines
    def __init__(self):
        self.lines = []

    def addline(self, line):
        self.lines.append(line)
