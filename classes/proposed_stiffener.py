
class proposed_stiffener():

    def __init__(self, pl_position, st_number, location, i_along, b_sup = None, b_inf = None, h = None, t = None):
        self.pl_position = pl_position
        self.st_number = st_number
        self.location = location
        self.i_along = i_along
        self.b_sup = b_sup if b_sup is not None else 0
        self.b_inf = b_inf if b_inf is not None else 0
        self.h = h if h is not None else 0
        self.t = t if t is not None else 0
        self.b_sup_corr = False
        self.b_inf_corr = False
        self.h_corr = False
        self.b_sup_corr_val = 0
        self.b_inf_corr_val = 0
        self.h_corr_val = 0
