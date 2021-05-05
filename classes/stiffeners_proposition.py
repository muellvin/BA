import defaults

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

    def print_stiffeners_proposition(self):
        if defaults.do_print_to_txt == True:
            file = open("output\cs_analysis.txt", "a+")
            file.write("\nSTIFFENERS PROPOSITION")
            for stiffener in self.stiffeners:
                stiffener.print_stiffener()
            file.close()
        if defaults.do_print_to_terminal == True:
            pass
