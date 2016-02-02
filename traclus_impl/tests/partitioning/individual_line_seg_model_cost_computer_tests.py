'''
Created on Jan 9, 2016

@author: Alex
'''
import unittest
from tests.unit_base_tests import UnitBaseTests
from partitioning.trajectory_partitioning import individual_line_seg_model_cost_computer
import math
from representative_trajectory_average_inputs import DECIMAL_MAX_DIFF_FOR_EQUALITY

class IndividualLineSegModelCostComputerTest(UnitBaseTests):

    def test_get_cost_normal_case(self):
        line_seg = self.create_simple_line_seg(start=(0, 0), end=(1, 1))
        self.assertAlmostEquals(individual_line_seg_model_cost_computer(line_seg), 0.5, \
                                delta=DECIMAL_MAX_DIFF_FOR_EQUALITY)
        
        line_seg = self.create_simple_line_seg(start=(0, 0), end=(4, 4))
        self.assertAlmostEquals(individual_line_seg_model_cost_computer(line_seg), math.log(math.sqrt(2.0) * 4, 2), \
                                delta=DECIMAL_MAX_DIFF_FOR_EQUALITY)

        line_seg = self.create_simple_line_seg(start=(1, 0), end=(1 + math.sqrt(3), 1))
        self.assertAlmostEquals(individual_line_seg_model_cost_computer(line_seg), 1, \
                                delta=DECIMAL_MAX_DIFF_FOR_EQUALITY)
        
        line_seg = self.create_simple_line_seg(start=(1, 0), end=(1.1, 0))
        self.assertAlmostEquals(individual_line_seg_model_cost_computer(line_seg), math.log(0.1, 2), \
                                delta=DECIMAL_MAX_DIFF_FOR_EQUALITY)
        
        line_seg = self.create_simple_line_seg(start=(2, 3), end=(2, 4.00001))
        self.assertAlmostEquals(individual_line_seg_model_cost_computer(line_seg), 0, \
                                delta=0.1) 
        
    def test_get_cost_bad_inputs(self):  
        line_seg = self.create_simple_line_seg(start=(2, 3), end=(2, 3))
        self.assertRaises(ValueError, individual_line_seg_model_cost_computer, line_seg) 

        line_seg = self.create_simple_line_seg(start=(2, 3), end=(2, 3))
        self.assertRaises(ValueError, individual_line_seg_model_cost_computer, line_seg) 


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()