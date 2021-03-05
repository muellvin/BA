#crosssection calculation
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
#functionality of inertial area moments function not tested yet
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
#center functions for reduced crosssections still need to be properly defined
    def get_area_red(self):
        a=0
        for i in self.lines:
            a = a + i.get_area_red()
        return a

    def get_z_center_red(self):
        weighted_a = 0
        for i in self.lines:
            weighted_a = weighted_a + i.get_area_red()*i.get_z_center_red()
        return weighted_a/self.get_area_red()

    def get_y_center_red(self):
        weighted_a = 0
        for i in self.lines:
            weighted_a = weighted_a + i.get_area_red()*i.get_y_center_red()
        return weighted_a/self.get_area_red()

    def get_iy_red(self):
        z_s = self.get_z_center_red()
        iy_tot = 0
        for i in self.lines:
            iy_tot = iy_tot + i.get_iy_red() + (z_s-i.get_z_center_red())**2 * i.get_area_red()
        return iy_tot

    def get_iz_red(self):
        y_s = self.get_y_center_red()
        iz_tot = 0
        for i in self.lines:
            iz_tot = iz_tot + i.get_iz_red() + (y_s-i.get_y_center_red())**2 * i.get_area_red()
        return iz_tot