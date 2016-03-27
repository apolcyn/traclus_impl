'''
Created on Jan 6, 2016

@author: Alex
'''
from traclus_impl.line_segment_averaging import get_mean_vertical_coordinate_in_line_segments
from traclus_impl.line_segment_averaging import number_average, \
    line_segment_averaging_set_iterable
from traclus_impl.linked_list import LinkedList
from traclus_impl.traclus_dbscan import TrajectoryLineSegmentFactory
import unittest

import unit_base_tests


def simple_func(num):
    return num

class LineSegmentAveragingTest(unit_base_tests.UnitBaseTests):    
    def test_bad_input(self):
        self.assertRaises(Exception, number_average, [], simple_func)
    
    def test_number_averaging_normal(self):
        self.assertEquals(number_average([0.0, 1.0, 2.0, 3, 4, 5], simple_func), 2.5)
        self.assertEquals(number_average([0.0, 1.0, 2.0, 3, 4, 5], simple_func), 2.5)
        self.assertEquals(number_average([0, 1, 2, 3, 4, 11], simple_func), 3.5)
        list = LinkedList()
        list.add_last(0)
        self.assertEquals(number_average(list, simple_func), 0)
        
    def test_line_segment_generator(self):
        lines = [self.create_trajectory_line_seg((0, 0), (1, 2), 0, 3), \
                 self.create_trajectory_line_seg((3, 2), (3, 4), 1, 2), \
                 self.create_trajectory_line_seg((4, 5), (2, 3), 2, 4)]
        test_ob = {'horizontal_position':3, 'lines': [] }
        for line in lines:
            test_ob['lines'].append(line)
        expected = map(lambda seg: {'horizontal_pos':3, 'line_seg': seg.line_segment }, lines)
        
        self.verify_iterable_works_more_than_once(line_segment_averaging_set_iterable(test_ob), expected)
        
    def test_empty_lines_for_line_segment_generator(self):
        test_ob = {'horizontal_position': 4, 'lines': []}
        self.verify_iterable_works_more_than_once(line_segment_averaging_set_iterable(test_ob), [])
        
    def test_line_segment_averaging_normal(self):
        lines = [self.create_simple_line_seg((0, 1), (1, 2)), \
                 self.create_simple_line_seg((0, 2), (1, 3)), \
                 self.create_simple_line_seg((0, 3), (1, 4)), \
                 self.create_simple_line_seg((0, 4), (1, 5))]
        traj_seg_factory = TrajectoryLineSegmentFactory()
        test_ob = {'lines': map(lambda x: traj_seg_factory.new_trajectory_line_seg(x, 0), lines), \
                   'horizontal_position': 0.5}
        self.assertEquals(get_mean_vertical_coordinate_in_line_segments(test_ob), 3.0)
        
    def test_line_segment_averaging_empty_input(self):
        test_ob = {'lines': [], 'horizontal_position': 0.5}
        self.assertRaises(Exception, get_mean_vertical_coordinate_in_line_segments, test_ob)
        
    def test_line_segment_averaging_bad_input(self):
        lines = [self.create_simple_line_seg((0, 1), (1, 2)), \
                 self.create_simple_line_seg((0, 2), (1, 3)), \
                 self.create_simple_line_seg((0, 3), (1, 4)), \
                 self.create_simple_line_seg((0, 4), (1, 5))]
        test_ob = {'lines': [], 'horizontal_position': 1.5}
        self.assertRaises(Exception, get_mean_vertical_coordinate_in_line_segments, test_ob)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()