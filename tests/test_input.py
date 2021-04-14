import unittest
from initial_cs import create_initial_cs

class TestInitialCS(unittest.TestCase):

    def test_top_left(self):
        cs = create_initial_cs(4000, 3000, 2000, 10, 10, 10)
        y_top_left = cs.lines[0].a.y
        z_top_left = cs.lines[0].a.z
        self.assertEqual(y_top_left, 2000)
        self.assertEqual(z_top_left, 0)

    def test_top_right(self):
        cs = create_initial_cs(4000, 3000, 2000, 10, 10, 10)
        y_top_right = cs.lines[0].b.y
        z_top_right = cs.lines[0].b.z
        self.assertEqual(y_top_right, -2000)
        self.assertEqual(z_top_right, 0)

if __name__ == '__main__':
    unittest.main()
