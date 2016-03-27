'''
Created on Jan 8, 2016

@author: Alex
'''
import unittest

from traclus_impl.mutable_float import MutableNumber
from traclus_impl.tests.unit_base_tests import UnitBaseTests
from traclus_impl.trajectory_partitioning import partition_trajectory


class PartitioningTest(UnitBaseTests):
    
    def get_mock_cost_computer(self, cost_table):
        def func(list, low, high, model_cost_computer, cost_table=cost_table):
            if cost_table[low][high] == None:
                raise Exception("hit an invalid index")
            model_cost_computer()
            return cost_table[low][high]
        return func
    
    def create_mock_model_cost_getter_func(self, dummy_individual_line_seg_model_cost_computer):
        def _mock_model_cost_computer_getter(provided_individual_cost_computer):
            self.assertEquals(dummy_individual_line_seg_model_cost_computer, provided_individual_cost_computer)
            def _cost_computer():
                provided_individual_cost_computer.increment(1)
                return provided_individual_cost_computer.get_val() - 1
            
            return _cost_computer
        return _mock_model_cost_computer_getter
    
    def test_gets_borders(self):
        par_cost_table = [[None, None], [None, None]]
        no_par_cost_table = [[None, None], [None, None]]
        list = [None] * 2
        expected = [0, 1]
        mock_individual_cost_computer = MutableNumber(0)
        actual = partition_trajectory(list, self.get_mock_cost_computer(par_cost_table), \
                                      self.get_mock_cost_computer(no_par_cost_table), \
                                      self.create_mock_model_cost_getter_func(mock_individual_cost_computer), \
                                      mock_individual_cost_computer)
        self.verify_iterable_works_more_than_once(expected, actual)
        self.assertEquals(mock_individual_cost_computer.get_val(), 0)
        
    def test_get_borders_of_three_item_list(self):
        par_cost_table = [[None, None, 4], [None, None, None], [None, None, None]]
        no_par_cost_table = [[None, None, 5], [None, None, None], [None, None, None]]
        list = [None] * 3
        expected = [0, 2]
        mock_individual_cost_computer = MutableNumber(0)
        actual = partition_trajectory(list, self.get_mock_cost_computer(par_cost_table), \
                                      self.get_mock_cost_computer(no_par_cost_table), \
                                      self.create_mock_model_cost_getter_func(mock_individual_cost_computer), \
                                      mock_individual_cost_computer)
        self.verify_iterable_works_more_than_once(expected, actual)
        self.assertEquals(mock_individual_cost_computer.get_val(), 1 * 2)
        
    def test_get_all_of_three_item_list(self):
        par_cost_table = [[None, None, 6], [None, None, None], [None, None, None]]
        no_par_cost_table = [[None, None, 5], [None, None, None], [None, None, None]]
        list = [None] * 3
        expected = [0, 1, 2]
        mock_individual_cost_computer = MutableNumber(0)
        actual = partition_trajectory(list, self.get_mock_cost_computer(par_cost_table), \
                                      self.get_mock_cost_computer(no_par_cost_table), \
                                      self.create_mock_model_cost_getter_func(mock_individual_cost_computer), \
                                      mock_individual_cost_computer)
        self.verify_iterable_works_more_than_once(expected, actual)
        self.assertEquals(mock_individual_cost_computer.get_val(), 1 * 2)
        
    def test_get_all_of_four_item_list(self):
        par_cost_table = \
        [[None, None, 3, 3], \
         [None, None, None, 4], \
         [None, None, None, None], \
         [None, None, None, None]]
        
        no_par_cost_table = \
        [[None, None, 2, 2], \
         [None, None, None, 3], \
         [None, None, None, None], \
         [None, None, None, None]]
        
        list = [None] * 4
        expected = [0, 1, 2, 3]
        mock_individual_cost_computer = MutableNumber(0)
        actual = partition_trajectory(list, self.get_mock_cost_computer(par_cost_table), \
                                      self.get_mock_cost_computer(no_par_cost_table), \
                                      self.create_mock_model_cost_getter_func(mock_individual_cost_computer), \
                                      mock_individual_cost_computer)
        self.verify_iterable_works_more_than_once(expected, actual)
        self.assertEquals(mock_individual_cost_computer.get_val(), 2 * 2)
        
    def test_get_some_of_four_item_list(self):
        par_cost_table = \
        [[None, None, 2, 3], \
         [None, None, None, None], \
         [None, None, None, None], \
         [None, None, None, None]]
        
        no_par_cost_table = \
        [[None, None, 2, 2], \
         [None, None, None, None], \
         [None, None, None, None], \
         [None, None, None, None]]
        
        list = [None] * 4
        
        expected_partition = [0, 2, 3]
        mock_individual_cost_computer = MutableNumber(0)
        actual = partition_trajectory(list, self.get_mock_cost_computer(par_cost_table), \
                                      self.get_mock_cost_computer(no_par_cost_table), \
                                      self.create_mock_model_cost_getter_func(mock_individual_cost_computer), \
                                      mock_individual_cost_computer)
        self.verify_iterable_equals_list(actual, expected_partition)
        self.assertEquals(mock_individual_cost_computer.get_val(), 2 * 2)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()