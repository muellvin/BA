
class stiffeners_proposition():

    def __init__(self):
        self.stiffeners = []


    def add(self, proposed_stiffener):
        self.stiffeners.append(proposed_stiffener)
        return

    def get_proposed_stiffener(self, pl_position, st_number):
        for prop_stiffener in self.stiffeners:
            if prop_stiffener.pl_position == pl_position and prop_stiffener.st_number == st_number:
                return prop_stiffener
        return None
