import unittest
import defaults
import data
from classes import crosssection
import cs_collector

class TestInitialCS(unittest.TestCase):

    def test_cs_collector(self):
        defaults.optimize_for_cost_only = True
        defaults.optimize_for_spec_ei = False
        defaults.optimize_for_target_function = False
        cs1 = crosssection.crosssection(0,0,0)
        cs1.cost = 4
        data.cs_collection.append(cs1)

        cs2 = crosssection.crosssection(0,0,0)
        cs2.cost = 2
        data.cs_collection.append(cs2)

        cs3 = crosssection.crosssection(0,0,0)
        cs3.cost = 2
        data.cs_collection.append(cs3)

        cs4 = crosssection.crosssection(0,0,0)
        cs4.cost = 2
        data.cs_collection.append(cs4)



        best = cs_collector.get_best_cost()

        self.assertEqual(best[0].cost, 2)
        self.assertEqual(best[1].cost, 2)
        self.assertEqual(best[2].cost, 2)

if __name__ == '__main__':
    unittest.main()
