import unittest
from initial_cs import create_initial_cs
from classes import stiffener as st


class TestMerge(unittest.TestCase):

    def test_empty(self):
        initial_cs = ics.create_initial_cs(4000, 3000, 2000, 20, 20, 20)
        stiffeners = []
        final_cs = st.merge(initial_cs, stiffeners)
        length = len(final_cs)
        self.assertEqual(length, 4)

if __name__ == '__main__':
    unittest.main()
