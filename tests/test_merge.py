import unittest
from initial_cs import create_initial_cs
from classes import stiffener as st
from classes import plate_code as plcd
from classes import crosssection

class TestMerge(unittest.TestCase):

    def test_empty(self):
        initial_cs = create_initial_cs(4000, 3000, 2000, 20, 20, 20)
        stiffeners = []
        final_cs = st.merge(initial_cs, stiffeners)
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
        final_cs = st.merge(initial_cs, stiffeners)
        length = len(final_cs.lines)
        self.assertEqual(length, 14)
        stiffener_1_line_3 = final_cs.get_line(st_number = 1, st_pl_position = 3)
        st_1_3_length = stiffener_1_line_3.get_length_tot()
        self.assertEqual(st_1_3_length, 200)
        line_top_right = final_cs.get_line(tpl_number = 5)
        code_5 = plcd.plate_code(1,0,5,0,0)
        self.assertEqual(line_top_right.code, code_5)
        self.assertEqual(line_top_right.a.y, -1150)

if __name__ == '__main__':
    unittest.main()
