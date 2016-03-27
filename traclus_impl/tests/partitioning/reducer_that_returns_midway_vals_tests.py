'''
Created on Jan 9, 2016

@author: Alex
'''
import unittest

from traclus_impl.tests.unit_base_tests import UnitBaseTests
from traclus_impl.trajectory_partitioning import get_number_list_reducer_that_returns_each_midway_val


class ReducerThatReturnsMidwayValsTests(UnitBaseTests):

    def test_reducer_that_retuns_midway_vals(self):
        mult_by_10 = lambda x: x * 10
        in_list = [0, 1, 2, 3, 4, 5]
        expected = [0, 10, 30, 60, 100, 150]
        out_list = map(get_number_list_reducer_that_returns_each_midway_val(mult_by_10), in_list)
        
        self.verify_iterable_works_more_than_once(expected, out_list)
        
    def test_single_item_list_midway_val_returner(self):
        add_10 = lambda x: x + 10
        in_list = [3]
        expected = [13]
        out_list = map(get_number_list_reducer_that_returns_each_midway_val(add_10), in_list)
        
        self.verify_iterable_works_more_than_once(expected, out_list)
        
    def test_empty__list_midway_val_returner(self):
        add_10 = lambda x: x + 10
        in_list = []
        expected = []
        out_list = map(get_number_list_reducer_that_returns_each_midway_val(add_10), in_list)
        
        self.verify_iterable_works_more_than_once(expected, out_list)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()