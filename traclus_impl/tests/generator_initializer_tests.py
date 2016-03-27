'''
Created on Jan 6, 2016

@author: Alex
'''
from traclus_impl.generator_initializer import GeneratorInitializer
import unittest

from unit_base_tests import UnitBaseTests


def classless_generator(list):
    for item in list:
        yield item
        
def classless_multi_item(list, filter_a, filter_b):
    for item in list:
        if item in filter_a and item in filter_b:
            yield item

class GeneratorInitializerTest(UnitBaseTests):
    
    def simple_generator(self, list):
        for item in list:
            yield item
            
    def filter_generator(self, nums, nums_to_keep):
        for item in nums:
            if item in nums_to_keep:
                yield item

    def test_empty_lists(self):        
        actual = GeneratorInitializer(self.simple_generator, [])
        self.verify_iterable_works_more_than_once(actual, [])
        
    def test_classless_multi_item(self):
        actual = GeneratorInitializer(classless_multi_item, [1, 3, 7, 5], (2, 3, 7), (2, 3, 5))
        self.verify_iterable_works_more_than_once(actual, [3])

        
    def test_classless_generator(self):
        actual = GeneratorInitializer(classless_generator, [1, 2, 3])
        self.verify_iterable_works_more_than_once(actual, [1, 2, 3])
        
    def test_filter_generator(self):
        actual = GeneratorInitializer(self.filter_generator, [1, 4, 3, 2, 5], (1, 2, 4))
        self.verify_iterable_works_more_than_once(actual, [1, 4, 2])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()