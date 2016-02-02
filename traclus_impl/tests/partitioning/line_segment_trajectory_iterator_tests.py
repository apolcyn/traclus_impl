'''
Created on Jan 7, 2016

@author: Alex
'''
import unittest
from partitioning.trajectory_partitioning import get_trajectory_line_segment_iterator
from partitioning.trajectory_partitioning import get_line_segment_from_points
from tests import unit_base_tests

class LineSegmentTrajectoryIteratorTest(unit_base_tests.UnitBaseTests):

    def get_mock_line_segment_from_points(self, num_a, num_b):
        return [num_a, num_b]

    def test_bad_indices(self):
        list = [1, 2, 3, 4]
        self.assertRaises(Exception, get_trajectory_line_segment_iterator, \
                          list, 2, 2, self.get_mock_line_segment_from_points)
        self.assertRaises(Exception, get_trajectory_line_segment_iterator, \
                          list, 2, 1, self.get_mock_line_segment_from_points)
        
    def test_single_segment_left(self):
        list = [1, 2, 3, 4]
        expected = [[2, 3]]
        iterator = get_trajectory_line_segment_iterator(list, 1, 2, self.get_mock_line_segment_from_points)
        self.verify_iterable_equals_list(iterator, expected)
        
        expected = [[3, 4]]
        iterator = get_trajectory_line_segment_iterator(list, 2, 3, self.get_mock_line_segment_from_points)
        self.verify_iterable_equals_list(iterator, expected)
        
    def test_normal_case(self):
        list = [1, 2, 3, 4, 5]
        expected = [[1, 2], [2, 3], [3, 4], [4, 5]]
        iterator = get_trajectory_line_segment_iterator(list, 0, 4, self.get_mock_line_segment_from_points)
        self.verify_iterable_equals_list(iterator, expected)
        
        expected = [[2, 3], [3, 4], [4, 5]]
        iterator = get_trajectory_line_segment_iterator(list, 1, 4, self.get_mock_line_segment_from_points)
        self.verify_iterable_equals_list(iterator, expected)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()