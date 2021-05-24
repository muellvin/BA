from data_and_defaults import defaults

class stiffeners_proposition():
    #constructor
    def __init__(self):
        self.stiffeners = []

    #method to add another proposed_stiffener
    def add(self, proposed_stiffener):
        self.stiffeners.append(proposed_stiffener)
        return
    #method to get a proposed_stiffener using position and number
    def get_proposed_stiffener(self, pl_position, st_number):
        for prop_stiffener in self.stiffeners:
            if prop_stiffener.pl_position == pl_position and prop_stiffener.st_number == st_number:
                return prop_stiffener
        return None
