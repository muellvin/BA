#classes

import math

class point():
#origin: symmetry axis and track plate
#usual civil engineering coordinates: z down, y out of paper (to the left)
    def __init__(self, y, z):
        self.y = y
        self.z = z


class line():
#code for identification: position, type, number, pos in profile
#a and b are of starting end ending points of the line
#p1 and p2 are the borders of "active" crosssection regarding effective width
#p1 is closer to A and p2 is closer to B
#t is the thickness of the plate
    def __init__(self, code, a, b, p1, p2, t):
        self.code = code
        self.a = a
        self.b = b
        self.p1 = p1
        self.p2 = p2
        self.t = t
    #non-reduced parameters
        self.lengthtot
        self.areatot
        self.ialongtot
        self.iperpentot
        self.iytot
        self.iztot
    #reduced parameters
        self.lengthred
        self.areared
        self.ialongred
        self.iperpenred
        self.iyred
        self.izred

#p1 should be closer to a and p2 closer to b
    def sanitycheck(self):
        tbd

#methods to calculate line propreties for non-reduced
    def get_length_tot(self):
        return cal_length(self.a.y, self.a.z, self.b.y, self.b.z, self.t)
    def get_area_tot(self):
        return cal_area(self.a.y, self.a.z, self.b.y, self.b.z, self.t)
    def get_ialong_tot(self):
        return cal_ialong(self.a.y, self.a.z, self.b.y, self.b.z, self.t)
    def get_iperpen_tot(self):
        return cal_perpen(self.a.y, self.a.z, self.b.y, self.b.z, self.t)
    def get_iy_tot(self):
        return cal_iy(self.a.y, self.a.z, self.b.y, self.b.z, self.t)
    def get_iz_tot(self):
        return cal_iz(self.a.y, self.a.z, self.b.y, self.b.z, self.t)

#methods to calculate line propreties for reduced
    def get_length_red1(self):
        return cal_length(self.a.y, self.a.z, self.p1.y, self.p1.z, self.t)
    def get_length_red2(self):
        return cal_length(self.b.y, self.b.z, self.p2.y, self.p2.z, self.t)
    def get_area_red1(self):
        return cal_area(self.a.y, self.a.z, self.p1.y, self.p1.z, self.t)
    def get_area_red2(self):
        return cal_area(self.b.y, self.b.z, self.p2.y, self.p2.z, self.t)
    def get_ialong_red(self):
        return cal_ialong(self.a.y, self.a.z, self.b.y, self.b.z, self.t)
    def get_iperpen_red(self):
        iperpen_red1 = cal_perpen(self.a.y, self.a.z, self.p1.y, self.p1.z, self.t)
        iperpen_red2 = cal_perpen(self.b.y, self.b.z, self.p2.y, self.p2.z, self.t)
        iperpen_red1_withsteiner = cal_iperpen(self.a.y, self.a.z, self.p1.y, self.p1.z, self.t) + cal_area(self.a.y, self.a.z, self.p1.y, self.p1.z, self.t) * cal_center_along(self.a.y, self.a.z, self.p1.y, self.p1.z, self.t)^2
        iperpen_red2_withsteiner = cal_iperpen(self.b.y, self.b.z, self.p2.y, self.p2.z, self.t) + cal_area(self.b.y, self.b.z, self.p2.y, self.p2.z, self.t) * cal_center_along(self.b.y, self.b.z, self.p2.y, self.p2.z, self.t)^2
        return iperpen_red1_withsteiner + iperpen_red2_withsteiner
    def get_iy_red(self):
        tbd
    def get_iz_red(self):
        tbd




#general calculation methods so that they can be used for both reduced and non-reduced
    def cal_centeryz(ay, az, by, bz, t):
        yc = 1/2 * (ay + by)
        zc = 1/2 * (az + bz)
        return yc, zc
    def cal_center_along(ay, az, by, bz, t):
        return 1/2 * cal_length(ay, az, by, bz, t)
    def cal_length(ay, az, by, bz, t):
        return math.sqrt((ay - by)^2 + (az - bz)^2)
    def cal_area(ay, az, by, bz, t):
        return cal_length(ay, az, by, bz) * t
    def cal_ialong(ay, az, by, bz, t):
        return t^3 * cal_length(ay, az, by, bz, t) / 12
    def cal_iperpen(ay, az, by, bz, t):
        return cal_length(ay, az, by, bz, t)^3 * t / 12
#moments of inertia along y and z are created with a tensor rotation of ialong
#it uses the fact that the line is symmetric in two axis and it does not matter weather we rotate in positive or negative angle direction
#thus it calculates with absolute length and minimal angle
    def cal_iy(ay, az, by, bz, t):
        zdis = abs(bz - az)
        ydis = abs(by - ay)
        angle = math.atan(zdis / ydis) #smaller angle between y axis and line, thus should be between 0 and pi
        assert angle >= 0, "getiy and getiz function are faulty"
        assert angle <= math.pi, "getiy and getiz function are faulty"
        return math.cos(angle)^2 * cal_ialong(ay, az, by, bz, t) + math.sin(angle)^2 * cal_iperpen(ay, az, by, bz, t)
    def cal_iz(ay, az, by, bz, t):
        zdis = abs(bz - az)
        ydis = abs(by - ay)
        angle = math.atan(zdis / ydis) #smaller angle between y axis and line, thus should be between 0 and pi
        assert angle >= 0, "getiy and getiz function are faulty"
        assert angle <= math.pi, "getiy and getiz function are faulty"
        complangle = math.pi - angle
        return math.cos(complangle)^2 * cal_ialong(ay, az, by, bz, t) + math.sin(complangle)^2 * cal_iperpen(ay, az, by, bz, t)



class cs():
#a crosssection is defined as a list of lines
    def __init__(self):
        self.lines = []

    def addline(self, line):
        self.lines.append(line)
