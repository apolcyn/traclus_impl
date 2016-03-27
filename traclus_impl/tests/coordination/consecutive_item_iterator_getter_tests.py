'''
Created on Jan 10, 2016

@author: Alex
'''
import unittest

from traclus_impl.coordination import consecutive_item_func_iterator_getter
from traclus_impl.tests.unit_base_tests import UnitBaseTests


class Test(UnitBaseTests):

    def mock_consec_items_func(self, a, b):
        return b - a

    def test_normal_case(self):
        list = [1, 2, 4, 7, 11]
        expected = [1, 2, 3, 4]
        res = consecutive_item_func_iterator_getter(consecutive_item_func=self.mock_consec_items_func, \
                                                     item_iterable=list)
        self.verify_iterable_works_more_than_once(iterable=res, list_ob=expected)
        
    def test_keeps_original_iterable(self):
        list = [1, 2, 4, 7, 11]
        expected = [1, 2, 3, 4]
        res = consecutive_item_func_iterator_getter(consecutive_item_func=self.mock_consec_items_func, \
                                                     item_iterable=list)
        self.verify_iterable_works_more_than_once(iterable=res, list_ob=expected)
        list = [1, 3, 6, 10, 15]
        self.verify_iterable_works_more_than_once(iterable=res, list_ob=expected)
        
    def test_not_enough_input(self):
        self.assertRaises(ValueError, \
                                     consecutive_item_func_iterator_getter, self.mock_consec_items_func, [4])
        self.assertRaises(ValueError, \
                                     consecutive_item_func_iterator_getter, self.mock_consec_items_func, [])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()