#class containing the orientation code for each plate of the crosssections

class plate_code():
    """This code reveals, where the specified plate of the crosssection is."""

    def __init__(self, pl_position, pl_type, st_number, st_pl_position):
        self.pl_position = pl_position
        self.pl_type = pl_type
        self.st_number = st_number
        self.st_pl_position = st_pl_position

#pl_position: clockwise, starting with the (top) track plate from 1 to 4
#pl_type: plates of initial crossection: 0, plates of stiffener: 1
#st_number: clockwise starting with top left hand corner with number 1
#st_pl_position: similar to pl_position, but with stiffener plates
#main plate is Nr.1, thus if st_pl_position=1, pl_type=0. 
