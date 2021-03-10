#not really a class
#has methods for creating stiffeners of the type crosssection

import math


    """not finished!!! needs correction for center. now center is at point a of plate 2 in stiffener"""
    def create_stiffener_globalcoordinates(center, angle, width_top, width_bottom, height, t):
        assert width_top >= width_bottom: "width out of bound or wrong way around"
        half_width_diff = width_top - width_bottom
        length_side = math.sqrt(half_width_diff**2 + height**2)
        own_angle = math.atan(half_width_diff / height)

        #create plate 2
        a2 = point.point(0,0)
        b2 = point.point(math.sin(own_angle-angle)*length_side, math.cos(own_angle-angle)*length_side)
        line2 = line.line(a2, b2, t)

        #create plate 3
        a3 = b2
        b3 = point.point(a3.y + math.cos(angle)*width_bottom, a3.z + math.sin(angle)*width_bottom)
        line3 = line.line(a3, b3, t)

        #create plate 4
        a4 = b3
        b4 = point.point(math.cos(angle)*width_top, math.sin(angle)*width_top)
        line3 = line.line(a4, b5, t)

        stiffener_global = crosssection.crosssection()
        #add the lines to itself
        stiffener_global.lines.addline(line2)
        stiffener_global.lines.addline(line3)
        stiffener_global.lines.addline(line4)
        return stiffener_global


    def create_stiffener_owncoordinates(width_top, width_bottom, height, t):
        assert width_top >= width_bottom: "width out of bound or wrong way around"
        half_width_diff = width_top - width_bottom
        length_side = math.sqrt(half_width_diff**2 + height**2)
        own_angle = math.atan(half_width_diff / height)

        #create plate 2
        a2 = point.point(-width_top/2,0)
        b2 = point.point(a2.y + math.sin(own_angle)*length_side, math.cos(own_angle)*length_side)
        line2 = line.line(a2, b2, t)

        #create plate 3
        a3 = b2
        b3 = point.point(a3.y + width_bottom, a3.z)
        line3 = line.line(a3, b3, t)

        #create plate 4
        a4 = b3
        b4 = point.point(width_top/2, 0)
        line3 = line.line(a4, b5, t)

        stiffener_local = crosssection.crosssection()
        #add the lines to itself
        stiffener_local.lines.addline(line2)
        stiffener_local.lines.addline(line3)
        stiffener_local.lines.addline(line4)


    def get_i_along_stiffener(width_top, width_bottom, height, t):
        stiffener_local = create_stiffener_local(width_top, width_bottom, height, t)
        i_along = stiffener_local.get_i_y_tot()
        return i_along
