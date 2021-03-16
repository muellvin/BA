#not really a class
#has methods for creating stiffeners of the type crosssection

import math


    #method that will be called by the optimizer
    def add_stiffener(crosssection, stiffeners_proposition):
        #important for the creation of the stiffener is the position and the moment of inertia along the plate where it is placed
        #assumptions: symmetric distribution of stiffeners along z axis
        #pl_position, same as plate_code
        #location: between 0 and 1:
            #for top/ bottom it is the distance to the symmetry axis as a ratio to the max (width/2)
            #for the sides it is the ratio of z value to the height of the cross-section
        #i_along is the moment of inertia along the plate to which it is added
        """code der im file stiffener mit der Methode get_i_along_stiffener, viele ausprobiert und mittels geometrischen beschränkungen entscheidet welche"""
        pass



    #function creating a crosssection, which is the three lines of a stiffener at the place desired
    def create_stiffener_global(pl_position, st_number, center_y, center_z, angle, width_top, width_bottom, height, t):
        y_corr = center_y - math.cos(angle)*width_top
        z_corr = center_z - math.sin(angle)*width_top
        assert width_top >= width_bottom: "width out of bound or wrong way around"
        half_width_diff = width_top - width_bottom
        length_side = math.sqrt(half_width_diff**2 + height**2)
        own_angle = math.atan(half_width_diff / height)

        #create plate 2
        a2 = point.point(y_corr,z_corr)
        b2 = point.point(y_corr + math.sin(own_angle-angle)*length_side, z_corr + math.cos(own_angle-angle)*length_side)
        code2 = plate_code.code(pl_position, 1, 0, st_number, 2)
        line2 = line.line(code2, a2, b2, t)


        #create plate 3
        a3 = b2
        b3 = point.point(a3.y + math.cos(angle)*width_bottom, a3.z + math.sin(angle)*width_bottom)
        code3 = plate_code.code(pl_position, 1, 0, st_number, 3)
        line3 = line.line(code3, a3, b3, t)

        #create plate 4
        a4 = b3
        b4 = point.point(y_corr + math.cos(angle)*width_top, z_corr + math.sin(angle)*width_top)
        code4 = plate_code.code(pl_position, 1, 0, st_number, 4)
        line4 = line.line(code4, a4, b4, t)

        stiffener_global = crosssection.crosssection()
        #add the lines to itself
        stiffener_global.lines.addline(line2)
        stiffener_global.lines.addline(line3)
        stiffener_global.lines.addline(line4)
        return stiffener_global

    #function creating a crosssection, which is the three lines of a stiffener. it is in its own coordinate system -> for calculation of i_along
    def create_stiffener_local(width_top, width_bottom, height, t):
        assert width_top >= width_bottom: "width out of bound or wrong way around"
        half_width_diff = width_top - width_bottom
        length_side = math.sqrt(half_width_diff**2 + height**2)
        own_angle = math.atan(half_width_diff / height)

        #create plate 2
        a2 = point.point(-width_top/2,0)
        b2 = point.point(a2.y + math.sin(own_angle)*length_side, math.cos(own_angle)*length_side)
        code2 = plate_code.code(0, 1, 0, 0, 2)
        line2 = line.line(code2, a2, b2, t)

        #create plate 3
        a3 = b2
        b3 = point.point(a3.y + width_bottom, a3.z)
        code3 = plate_code.code(0, 1, 0, 0, 3)
        line3 = line.line(code3, a3, b3, t)

        #create plate 4
        a4 = b3
        b4 = point.point(width_top/2, 0)
        code4 = plate_code.code(0, 1, 0, 0, 4)
        line4 = line.line(code4, a4, b4, t)

        stiffener_local = crosssection.crosssection()
        #add the lines to itself
        stiffener_local.lines.addline(line2)
        stiffener_local.lines.addline(line3)
        stiffener_local.lines.addline(line4)
        return stiffener_local


    def get_i_along_stiffener(width_top, width_bottom, height, t):
        stiffener_local = create_stiffener_local(width_top, width_bottom, height, t)
        i_along = stiffener_local.get_i_y_tot()
        return i_along


    def substantiate(stiffeners_proposition):
        pass

    #this function should check weather the proposed stiffeners are feasable in the initial crosssection with the track_plate
    #as an argument it takes the initial crosssection and a list of all proposed stiffeners of type crosssection in the global coordinate system
    def check_geometry(crosssection, stiffeners, stiffeners_proposition):

        #reorganize the stiffeners into own lists
        stiffeners1 = []
        stiffeners2 = []
        stiffeners3 = []
        stiffeners4 = []

        """a loop to create stiffeners1 is missing, as they are not included in stiffeners"""

        for stiffener in stiffeners:
            if stiffener[0].code.pl_number == 2:
                stiffeners2.append(stiffener)
            elif stiffener[0].code.pl_number == 3:
                stiffeners3.append(stiffener)
            elif stiffener[0].code.pl_number == 4:
                stiffeners4.append(stiffener)
            else
                print("the lines of the stiffeners that were given to check_geometry do not contain codes")


        #find for each side the most left and the most right one
        min = random.choice(stiffeners1)[0].code.st_number
        max = random.choice(stiffeners1)[0].code.st_number
        top_right = None
        top_left = None
        for stiffener in stiffeners1:
            if stiffener[0].code.st_number <= min:
                top_left = stiffener
                min = stiffener[0].code.st_number
            elif stiffener[0].code.st_number >= max:
                top_right = stiffener
                max =
        min = random.choice(stiffeners2)[0].code.st_number
        max = random.choice(stiffeners2)[0].code.st_number
        right_top = None
        right_bottom = None
        for stiffener in stiffeners2:
            if stiffener[0].code.st_number <= min:
                right_top = stiffener
            elif stiffener[0].code.st_number >= max:
                right_bottom = stiffener
        min = random.choice(stiffeners3)[0].code.st_number
        max = random.choice(stiffeners3)[0].code.st_number
        bottom_left = None
        bottom_right = None
        for stiffener in stiffeners2:
            if stiffener[0].code.st_number <= min:
                bottom_right = stiffener
            elif stiffener[0].code.st_number >= max:
                bottom_left = stiffener
        min = random.choice(stiffeners4)[0].code.st_number
        max = random.choice(stiffeners4)[0].code.st_number
        left_top = None
        left_bottom = None
        for stiffener in stiffeners4:
            if stiffener[0].code.st_number <= min:
                left_bottom = stiffener
            elif stiffener[0].code.st_number >= max:
                left_top = stiffener

        #points from track plate stiffeners
        top_left_4b = top_left.get_line(1,1,4).b
        top_left_4a = top_left.get_line(1,1,4).a
        top_right_2b = top_right.get_line(1,1,2).b
        top_right_2a = top_right.get_line(1,1,2).a

        #points from right side stiffeners
        right_top_4b = right_top.get_line(2,1,4).b
        right_top_4a = right_top.get_line(2,1,4).a
        right_bottom_2b = right_bottom.get_line(2,1,2).b
        right_bottom_2a = right_bottom.get_line(2,1,2).a

        #points from bottom side stiffeners
        bottom_right_4b = bottom_right.get_line(3,1,4).b
        bottom_right_4a = bottom_right.get_line(3,1,4).a
        bottom_left_2b = bottom_left.get_line(3,1,2).b
        bottom_left_2a = bottom_left.get_line(3,1,2).a

        #points from left side stiffeners
        left_bottom_4b = left_bottom.get_line(4,1,4).b
        left_bottom_4a = left_bottom.get_line(4,1,4).a
        left_top_2b = left_top.get_line(4,1,2).b
        left_top_2a = left_top.get_line(4,1,2).a


        #corners of the crosssection
        corner_top_right = None
        corner_top_left = None
        corner_bottom_right = None
        corner_bottom_left = None

        y_top_max = 0
        y_top_min = 0
        z_bottom_max = 0
        y_bottom_max = 0
        y_bottom_min = 0

        for plate in crosssection:
            for point in plate:
                if point.y >= y_top_max and point.z == 0:
                    y_top_max = point.y
                    corner_top_left = point
                elif point.y <= y_top_min and point.z == 0:
                    y_top_min = point.y
                    corner_top_right = point
                elif point.y >= y_bottom_max and point.z >= z_bottom_max:
                    y_bottom_max = point.y
                    z_bottom_max = point.z
                    corner_bottom_left = point
                elif point.y <= y_bottom_min and point.z >= z_bottom_max:
                    y_bottom_min = point.y
                    z_bottom_max = point.z

        """minimal distances need to be defined"""
        mindis_top_corner = 30
        mindis_side_top_corner = 30
        mindis_side_bottom_corner = 30
        mindis_bottom_corner = 30

        #check distances to corners of crosssection
        if corner_top_left.y - top_left_4b.y < mindis_top_corner:
            print("top left stiffener too close to the corner")
        if corner_top_right.y - top_right_2a.y > mindis_top_corner:
            print("top right stiffener too close to the corner")
        if right_top_4b.z < mindis_side_top_corner.z:
            print("right top stiffener too close to the corner")
        if left_top_2a.z < mindis_side_top_corner.z:
            print("left top stiffener too close to the corner")
        if corner_bottom_right.z - right_bottom_2a.z < mindis_side_bottom_corner:
            print("right bottom stiffener too close to the corner")
        if corner_bottom_left.z - left_bottom_4b.z <mindis_side_bottom_corner:
            print("left bottom stiffener too close to the corner")
        if corner_bottom_left.y - bottom_right_4b.y > mindis_bottom_corner:
            print("bottom right stiffener too close to the corner")
        if corner_bottom_right.y - bottom_left_2a.y < mindis_bottom_corner:
            print("bottom left stiffener too close to the corner")

        #check distances between stiffeners

        #check distances in corners between stiffeners
