'''
Created on Feb 11, 2016

@author: Alex
'''
import unit_base_tests
import unittest
from traclus_impl.parameter_estimation import find_entropy

class EntropyCalculationTest(unit_base_tests.UnitBaseTests):
    
    class DummyTrajLineSeg:
        def __init__(self, num_neighbors):
            self.num_neighbors = num_neighbors
            
        def get_num_neighbors(self):
            return self.num_neighbors

    def test_zero_neighbors_each(self):
        dummy_line_segs = [self.DummyTrajLineSeg(0)] * 8
        expected = 3.0
        result = find_entropy(dummy_line_segs)
        self.assertEquals(expected, result)
        
    def test_one_big_neighborhood(self):
        dummy_line_segs = [self.DummyTrajLineSeg(4)] * 4
        expected = 2.0
        result = find_entropy(dummy_line_segs)
        self.assertEquals(expected, result)
        
    def test_different_amount_of_neighbors(self):
        dummy_line_segs = [self.DummyTrajLineSeg(0)] * 2
        dummy_line_segs.append(self.DummyTrajLineSeg(1))
        expected = 1.5
        result = find_entropy(dummy_line_segs)
        self.assertEquals(expected, result)        
    


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()