'''
Created on Jan 10, 2016

@author: Alex
'''
import unittest

from traclus_impl.coordination import filter_by_indices
from traclus_impl.tests.unit_base_tests import UnitBaseTests


class IndexFilteringTest(UnitBaseTests):

    def test_normal_case(self):
        indices = [0, 3, 5]
        vals = ['a', 'b', 'c', 'd', 'e', 'f']
        expected = ['a', 'd', 'f']
        res = filter_by_indices(good_indices=indices, vals=vals)
        self.verify_iterable_works_more_than_once(res, expected)
        
    def test_two_values(self):
        indices = [0, 1]
        vals = ['a', 'b']
        expected = ['a', 'b']
        res = filter_by_indices(good_indices=indices, vals=vals)
        self.verify_iterable_works_more_than_once(res, expected)
        
    def test_single_value_case(self):
        indices = [0]
        vals = ['a']
        self.assertRaises(ValueError, filter_by_indices, indices, vals)
        
    def test_indices_too_high(self):
        indices = [0, 3, 5]
        vals = ['a', 'b', 'c', 'd', 'e']
        self.assertRaises(ValueError, filter_by_indices, indices, vals)
        
    def test_nonzero_first_index(self):
        self.assertRaises(ValueError, filter_by_indices, [1, 3, 5], [2, 4, 2, 3, 4, 5])
        
    def test_last_index_not_included(self):
        self.assertRaises(ValueError, filter_by_indices, [0, 3, 4], [2, 4, 2, 2, 3, 4])
                
    def test_empty_input(self):
        self.assertRaises(ValueError, filter_by_indices, [],[])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_normal_case']
    unittest.main()