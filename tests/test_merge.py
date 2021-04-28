import unittest
from initial_cs import create_initial_cs
from classes import stiffener as st
from classes import plate_code as plcd
from classes import crosssection
from classes import merge
import math

class TestMerge(unittest.TestCase):

    def test_empty(self):
        initial_cs = create_initial_cs(4000, 3000, 2000, 20, 20, 20)
        stiffeners = []
        final_cs = merge.merge(initial_cs, stiffeners)
        length = len(final_cs.lines)
        line_4 = final_cs.get_line(pl_type = 0, pl_position = 4, tpl_number = 4)
        code_4 = plcd.plate_code(4,0,4,0,0)
        self.assertEqual(length, 4)
        self.assertEqual(line_4.code, code_4)

    def test_stiffeners_top(self):
        initial_cs = create_initial_cs(4000, 3000, 2000, 20, 20, 20)
        stiffener_1 = st.create_stiffener_global(1, 1, 1000, 0, 0, 300, 200, 200, 15)
        stiffener_2 = st.create_stiffener_global(1, 2, -1000, 0, 0, 300, 200, 200, 15)
        stiffeners = [stiffener_1, stiffener_2]
        final_cs = merge.merge(initial_cs, stiffeners)
        length = len(final_cs.lines)
        self.assertEqual(length, 14)
        stiffener_1_line_3 = final_cs.get_line(st_number = 1, st_pl_position = 3)
        st_1_3_length = stiffener_1_line_3.get_length_tot()
        self.assertEqual(st_1_3_length, 200)
        line_top_right = final_cs.get_line(tpl_number = 5)
        code_5 = plcd.plate_code(1,0,5,0,0)
        self.assertEqual(line_top_right.code, code_5)
        self.assertEqual(line_top_right.a.y, -1150)

    def test_stiffeners_everywhere(self):
        initial_cs = create_initial_cs(4000, 4000, 2000, 20, 20, 20)
        stiffener_1 = st.create_stiffener_global(1, 1, 1000, 0, 0, 300, 200, 200, 15)
        stiffener_2 = st.create_stiffener_global(1, 2, -1000, 0, 0, 300, 200, 200, 15)
        stiffener_3 = st.create_stiffener_global(2, 3, -2000, 1000, 3*math.pi/2, 200, 100, 100, 10)
        stiffener_4 = st.create_stiffener_global(3, 4, -1000, 2000, math.pi, 300, 200, 200, 15)
        stiffener_5 = st.create_stiffener_global(3, 5, 1000, 2000, math.pi, 300, 200, 200, 15)
        stiffener_6 = st.create_stiffener_global(4, 6, 2000, 1000, math.pi/2, 200, 100, 100, 10)
        stiffeners = [stiffener_1, stiffener_2, stiffener_3, stiffener_4, stiffener_5, stiffener_6]
        final_cs = merge.merge(initial_cs, stiffeners)
        length = len(final_cs.lines)
        self.assertEqual(length, 34)
        last_line = final_cs.get_line(tpl_number = 16)
        code_16 = plcd.plate_code(4,0,16,0,0)
        self.assertEqual(last_line.code, code_16)

if __name__ == '__main__':
    unittest.main()
