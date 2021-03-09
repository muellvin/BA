#dictionary of input data and constants

class input_data(object):
    """Data container for input data and constants."""

    def __init__(self):
        self.data = {}

    def initialize_constants():
        self.data.update({"E": 210000, "G": 81000, "fy": 235})

    def userprompt():
        print('Value of b_sup? [mm]')
        b_sup = input()
        self.data.update({"b_sup":b_sup})
        print('Value of b_inf? [mm]')
        b_inf = input()
        self.data.update({"b_inf":b_inf})
        print('Value of h? [mm]')
        h = input()
        self.data.update({"h":h})
        print('Value of M_Ed? [kNm]')
        M_Ed= input()
        self.data.update({"M_Ed":M_Ed})
        print('Value of V_Ed? [kN]')
        V_Ed = input()
        self.data.update({"V_Ed":V_Ed})
        print('Value of T_Ed? [kNm]')
        T_Ed = input()
        self.data.update({"T_Ed":T_Ed})

    #set of standard test cases
    #containers still need to be filled with reasonable values
    def standard_test_case(test_number):
        pass
