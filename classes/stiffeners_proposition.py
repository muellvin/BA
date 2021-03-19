
class stiffeners_proposition():

    __init__(self):
        self.stiffeners = []


    def add_proposed_stiffener(self, pl_position, st_number, location, i_along):
        proposed_stiffener = new proposed_stiffener(pl_position, st_number, location, i_along)

    def get_proposed_stiffener(self, pl_position, st_number):
        for prop_stiffener in self.stiffeners:
            if prop_stiffener.pl_position == pl_position and prop_stiffener.st_number == st_number:
                return prop_stiffener
        return None
