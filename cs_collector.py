#crosssection generation framework still to be completely implemented
class cs_collection():
    """This is a collection of crossections."""

    #constructor creates four empty crosssection lists
    def __init__(self, initial_cs, current_cs, last_cs, best_cs):
        self.initial_cs = crosssection()
        self.current_cs = crosssection()
        self.last_cs = crosssection()
        self.best_cs = crosssection()

    def create_initial(b_sup, b_inf, h, t_sup, t_inf, t_side):
        pass

    def add_stiffener(line, norm_position, stiffener):
        pass
