import unittest
from classes import line
from classes import point
from classes import plate_code

class TestLine(unittest.TestCase):

    def test_center(self):
        a = point.point(2000, 0)
        b = point.point(-1000, 1000)
        code = plate_code.plate_code(1,0,0,0,0)
        t = 5
        horizontal = line.line(code, a, b, t)
        y = horizontal.get_center_y_tot()
        z = horizontal.get_center_z_tot()
        self.assertEqual(y, 500)
        self.assertEqual(z, 500)

    def test_length(self):
        a = point.point(2000, 0)
        b = point.point(-2000, 3000)
        code = plate_code.plate_code(1,0,0,0,0)
        t = 5
        plate = line.line(code, a, b, t)
        length = plate.get_length_tot()
        self.assertEqual(length, 5000)

    def test_area(self):
        a = point.point(2000, 0)
        b = point.point(-2000, 3000)
        code = plate_code.plate_code(1,0,0,0,0)
        t = 5
        plate = line.line(code, a, b, t)
        area = plate.get_area_tot()
        self.assertEqual(area, 25000)

if __name__ == '__main__':
    unittest.main()
