import unittest

from classes import crosssection
from classes import stiffener
from classes import line
from classes import plate_code
from output import geometry_output
import copy
import math

class Testcrosssection(unittest.TestCase):

    def test_i_along_tot(self):
        pl_position = 0
        st_number = 1
        center_y = 0
        center_z = 0
        angle = 0
        b_sup = 10000
        b_inf = 8000
        h = 5000
        t = 20

        #creation of cs horizontally
        cs_y = stiffener.create_stiffener_global(pl_position, st_number, center_y, center_z, angle, b_sup, b_inf, h, t)
        plate_between_code_y = plate_code.plate_code(0,0,1,1,1)
        plate_between_y = line.line(plate_between_code_y, copy.deepcopy(cs_y.get_line(st_pl_position = 4).b), copy.deepcopy(cs_y.get_line(st_pl_position = 2).a), t)
        cs_y.addline(plate_between_y)
        cs_y_i_y= cs_y.get_i_y_tot()
        cs_y_i_y_red = cs_y.get_i_y_red()

        #creation of cs rotated
        angle = math.pi*5/3
        cs_rot = cs_y.get_cs_rot(angle)
        cs_rot_plate_between = cs_rot.get_line(pl_type = 0)
        cs_rot_i_along = cs_rot.get_i_along_tot(cs_rot_plate_between)
        cs_rot_i_along_red = cs_rot.get_i_along_red(cs_rot_plate_between)
        test.assertTrue(cs_rot_i_along/cs_y_i_y - 1 < 0.001)
        test.assertTrue(cs_rot_i_along_red/cs_y_i_y_red - 1 < 0.001)

        angle = math.pi*3.453
        cs_rot = cs_y.get_cs_rot(angle)
        cs_rot_plate_between = cs_rot.get_line(pl_type = 0)
        cs_rot_i_along = cs_rot.get_i_along_tot(cs_rot_plate_between)
        cs_rot_i_along_red = cs_rot.get_i_along_red(cs_rot_plate_between)
        test.assertTrue(cs_rot_i_along/cs_y_i_y - 1 < 0.001)
        test.assertTrue(cs_rot_i_along_red/cs_y_i_y_red - 1 < 0.001)


        angle = math.pi*(-2.34)
        cs_rot = cs_y.get_cs_rot(angle)
        cs_rot_plate_between = cs_rot.get_line(pl_type = 0)
        cs_rot_i_along = cs_rot.get_i_along_tot(cs_rot_plate_between)
        cs_rot_i_along_red = cs_rot.get_i_along_red(cs_rot_plate_between)
        test.assertTrue(cs_rot_i_along/cs_y_i_y - 1 < 0.001)
        test.assertTrue(cs_rot_i_along_red/cs_y_i_y_red - 1 < 0.001)


if __name__ == '__main__':
    unittest.main()
