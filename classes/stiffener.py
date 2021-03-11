#not really a class
#has methods for creating stiffeners of the type crosssection

import math



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


    #this function should check weather the proposed stiffener is feasable in the proposed crosssection with all other proposed stiffeners
    #as an argument it takes the crosssection to which a list of stiffeners need to be added
    #the list of stiffeners includes all the stiffener lines of one side of the bridge cross-section
    def check_geometry(crosssection, stiffeners):
        #4 important distances for each side of stiffener 2 and 4:
            #distance from point a of stiffener plate 2 to end of trapezoid plate               -> dist_2corner
            #distance from point b of stiffener plate 2 to neighbouring trapezoid plate         -> dist_2ntr
            #distance from point b of stiffener plate 2 to stiffener of other trapezoid plate   -> dist_2ntrst
            #distacne from point a of stiffener plate 2 to stiffener of same trapezoid plates   -> dist_2nst

        #check on which side we are (all stiffeners should be on the same side)
        random_stiffener = random.choice(stiffeners)
        random_plate = random.choice(random_stiffener)
        pl_position = random_plate.code.pl_position

        #track_plate
        if pl_position is 1:
            print("invalid list of stiffeners was given to check_geometry. no stiffeners should be added to track_plate")

        #right side
        elif pl_position is 2:

            #find the top and bottom one
            most_up = None
            most_down = None
            st_number_min = random.choice(stiffeners)[0].code.st_number
            st_number_max = random.choice(stiffeners)[0].code.st_number
            for stiffener in stiffeners:
                if stiffener[0].code.st_number <= st_number_min:
                    most_up = stiffener
                elif stiffener[0].code.st_number >= st_number_max:
                    most_down = stiffener

            #calculate the relevant distances
            top_4_b = most_up.get_line(2,1,4).b
            top_4_a = most_up.get_line(2,1,4).a
            bottom_2_a = most_down.get_line(2,1,4).a
            bottom_2_b = most_down.get_line(2,1,4).b


        #bottom side
        elif pl_position is 3:
            pass

        #left side
        elif pl_position is 4:
            pass

        dist_2corner = None
        dist_2ntr = None
        dist_2ntrst = None
        dist_2nst = None

        dist_4corner = None
        dist_4ntr = None
        dist_4ntrst = None
        dist_4nst = None

        pass
