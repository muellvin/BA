class plate_code():
    
    def __init__(self, pl_position, pl_type, tpl_number, st_number, st_pl_position):
        self.pl_position = pl_position
        self.pl_type = pl_type
        self.tpl_number = tpl_number
        self.st_number = st_number
        self.st_pl_position = st_pl_position

    def __eq__(self, other):
        if isinstance(other, plate_code):
            return self.pl_position == other.pl_position and self.pl_type == other.pl_type and self.tpl_number == other.tpl_number and self.st_number == other.st_number and self.st_pl_position == other.st_pl_position
        return False

    def __str__(self):
        return "Plate Code (" + str(self.pl_position) + ", " + str(self.pl_type) \
        + ", " + str(self.tpl_number) + ", "+ str(self.st_number) + ", " \
        + str(self.st_pl_position) + ")"

#pl_position:
    #clockwise, starting with the (top) track plate from 1 to 4
#pl_type:
    #plates of trapezoid: 0, plates of stiffener: 1
#tpl_number: trapezoid plate number
    #the lines of the trapezoid are numbered themselves also starting at top left and going in clockwise direction
    #they do not match to the st_number
    #stiffener have a tpl_number of 0
#st_number:
    #clockwise starting with top left hand corner with number 1 and ending again at top left corner
    #this number is unique for every stiffener
    #the line of the trapezoid included by the stiffener has this number as well
    #the trapezoid lines not included by stiffeners have 0
#st_pl_position:
    #1 is the trapezoid line, 2,3,4 are lines of the stiffener numbered in clockwise direction
    #trapezoid lines not included by the stiffeners have 0
