import geometry_classes

class crosssection():
#a crosssection is defined as a list of lines
    def __init__(self):
        self.lines = []

    def addline(self, line):
        self.lines.append(line)
# methods to calculate properties of total crossection
    def get_area_tot(self):
        a=0
        for i in self.lines:
            a = a + i.get_area_tot()
        return a

    def get_z_center_tot(self):
        weighted_a = 0
        for i in self.lines:
            weighted_a = weighted_a + i.get_area_tot()*i.get_z_center_tot()
        return weighted_a/self.get_area_tot()

    def get_y_center_tot(self):
        weighted_a = 0
        for i in self.lines:
            weighted_a = weighted_a + i.get_area_tot()*i.get_y_center_tot()
        return weighted_a/self.get_area_tot()

#area moment of inertia functions have not been tested yet, because functionality in line for this purpose is missing up to present.
    def get_iy_tot(self):
        z_s = self.get_z_center_tot()
        iy_tot = 0
        for i in self.lines:
            iy_tot = iy_tot + i.get_iy_tot() + (z_s-i.get_z_center_tot())**2 * i.get_area_tot()
        return iy_tot

    def get_iz_tot(self):
        y_s = self.get_y_center_tot()
        iz_tot = 0
        for i in self.lines:
            iz_tot = iz_tot + i.get_iz_tot() + (y_s-i.get_y_center_tot())**2 * i.get_area_tot()
        return iz_tot
#methods to calculate properties of reduced crossection
#still tbd
