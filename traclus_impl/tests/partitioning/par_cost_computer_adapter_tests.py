'''
Created on Jan 9, 2016

@author: Alex
'''
import unittest
from tests.unit_base_tests import UnitBaseTests
from partitioning.trajectory_partitioning import part_cost_computer_adapter, no_part_cost_computer_adapter

class Test(UnitBaseTests):
    
    def mock_par_cost_func(self, trajectory_point_list, low_index, high_index, line_segment_iterable_getter, \
                            partition_line_getter, model_cost_computer, distance_func_computer, line_segment_creator):
        return str(low_index) + str(high_index) + line_segment_iterable_getter + \
            partition_line_getter + model_cost_computer + distance_func_computer + line_segment_creator
            
    def mock_no_par_cost_func(self, trajectory_point_list, low_index, high_index, \
                               line_segment_iterable_getter, model_cost_computer, line_segment_creator):
        return str(low_index) + str(high_index) + line_segment_iterable_getter + model_cost_computer + \
            line_segment_creator
            
    def create_mock_distance_func_computer_getter(self, val):
        def _func():
            return val
        return _func

    def test_par_cost_adapter(self):
        func = part_cost_computer_adapter(part_cost_func=self.mock_par_cost_func, line_segment_iterable_getter='a', \
                                          partition_line_getter='b', \
                                          distance_func_computer_getter=self.create_mock_distance_func_computer_getter('d'), line_segment_creator='x')
        self.assertEquals(func(trajectory_point_list=[1, 2], low_index=0, high_index=1, \
                               model_cost_computer='c'), "01abcdx")
        self.assertEquals(func(trajectory_point_list=[1, 2, 3], low_index=1, high_index=2, \
                               model_cost_computer='c'), "12abcdx")
        self.assertRaises(Exception, func, [0, 2], 1, 2)
        self.assertRaises(Exception, func, [2, 3, 4], 2, 1)
        
    def test_no_par_cost_adapter(self):
        func = no_part_cost_computer_adapter(no_part_cost_func=self.mock_no_par_cost_func, \
                                             line_segment_iterable_getter='a', line_segment_creator='c')
        self.assertEquals(func(trajectory_point_list=[3, 4, 5], low_index=1, \
                               high_index=2, model_cost_computer='b'), "12abc")
        self.assertEquals(func(trajectory_point_list=[3, 4, 5], low_index=0, \
                               high_index=2, model_cost_computer='b'), "02abc")
        self.assertRaises(Exception, func, [0, 2], 1, 2)
        self.assertRaises(Exception, func, [2, 3, 4], 2, 1)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()