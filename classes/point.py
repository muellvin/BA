#classes

import math

class point():
#origin: symmetry axis and track plate
#usual civil engineering coordinates: z down, y out of paper (to the left)
    def __init__(self, y, z):
        self.y = float(y)
        self.z = float(z)

    def __str__(self):
        return "(" + str(int(self.y)) + ", " + str(int(self.z)) + ")"
