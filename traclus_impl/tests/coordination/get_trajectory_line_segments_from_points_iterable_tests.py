'''
Created on Jan 13, 2016

@author: Alex
'''
import unittest

from traclus_impl.coordination import get_all_trajectory_line_segments_iterable_from_all_points_iterable
from traclus_impl.coordination import get_trajectory_line_segments_from_points_iterable
from traclus_impl.tests.unit_base_tests import UnitBaseTests


class GetTrajectoryLineSegmentsFromPointsIterableTest(UnitBaseTests):
    
    class MockTrajectoryLineSegFactory():
        def new_trajectory_line_seg(self, line_seg, trajectory_id):
            return (trajectory_id + line_seg[1]) * line_seg[0]
        
    def mock_partition_func(self, trajectory_point_list):
        cur_index = 0
        for x in trajectory_point_list:
            if x % 2 == 0:
                yield cur_index
            cur_index += 1
            
    def mock_line_seg_from_points_func(self, point_a, point_b):
        return [point_a, point_b] 
    
    def test_normal_case(self):
        points = [0, 1, 2, 3, 4, 5, 6]
        expected_line_segs = [0, 18, 44]
        res = get_trajectory_line_segments_from_points_iterable(point_iterable=points, \
                                                                trajectory_line_segment_factory=self.MockTrajectoryLineSegFactory(), \
                                                                trajectory_id=5, \
                                                                trajectory_partitioning_func=self.mock_partition_func, \
                                                                line_seg_from_points_func=self.mock_line_seg_from_points_func)
        self.verify_iterable_works_more_than_once(res, expected_line_segs)
        
    def test_no_line_segs(self):
        points = [2, 1]
        self.assertRaises(Exception, get_trajectory_line_segments_from_points_iterable, points, \
                          self.MockTrajectoryLineSegFactory, 5, self.mock_partition_func, \
                          self.mock_line_seg_from_points_func)
        
    def test_single_line_segs(self):
        points = [2, 1, 4]
        expected_line_segs = [18]
        res = get_trajectory_line_segments_from_points_iterable(point_iterable=points, \
                                                                trajectory_line_segment_factory=self.MockTrajectoryLineSegFactory(), \
                                                                trajectory_id=5, \
                                                                trajectory_partitioning_func=self.mock_partition_func, \
                                                                line_seg_from_points_func=self.mock_line_seg_from_points_func)
        self.verify_iterable_equals_list(iterable_ob=res, list_ob=expected_line_segs)
        
        
    def mock_get_line_segs_from_points_func(self, point_iterable, \
                                                       trajectory_id, \
                                                       trajectory_line_segment_factory, \
                                                       trajectory_partitioning_func, \
                                                       line_seg_from_points_func):
        for point in point_iterable:
            yield str(point) + str(trajectory_line_segment_factory) + str(trajectory_id) \
            + str(trajectory_partitioning_func) + str(line_seg_from_points_func)
        
    def test_get_ALL_trajectory_line_segs_from_ALL_points_iterable(self):
        point_list = [[0, 1], [5, 6]]
        expected = ["0a0bc", "1a0bc", "5a1bc", "6a1bc"]
        res = get_all_trajectory_line_segments_iterable_from_all_points_iterable(point_iterable_list=point_list, \
                                                                                 get_line_segs_from_points_func=self.mock_get_line_segs_from_points_func, \
                                                                                 trajectory_line_segment_factory='a', \
                                                                                 trajectory_partitioning_func='b', \
                                                                                 line_seg_from_points_func='c')
        self.verify_iterable_works_more_than_once(iterable=res, list_ob=expected)
        
    def test_get_ALL_trajectory_line_segs_from_ALL_points_iterable_single_line_seg(self):
        point_list = [[0]]
        expected = ["0a0bc"]
        res = get_all_trajectory_line_segments_iterable_from_all_points_iterable(point_iterable_list=point_list, \
                                                                                 get_line_segs_from_points_func=self.mock_get_line_segs_from_points_func, \
                                                                                 trajectory_line_segment_factory='a', \
                                                                                 trajectory_partitioning_func='b', \
                                                                                 line_seg_from_points_func='c')
        self.verify_iterable_works_more_than_once(iterable=res, list_ob=expected)
        
    def mock_get_lines_seg_from_points_return_nothing(self, point_iterable, \
                                                       trajectory_id, \
                                                       trajectory_line_segment_factory, \
                                                       trajectory_partitioning_func, \
                                                       line_seg_from_points_func):
        return []
        
    def test_get_ALL_trajectory_line_segs_from_ALL_points_iterable_no_line_segs_returned(self):
        point_list = [[0]]
        self.assertRaises(Exception, iter, get_all_trajectory_line_segments_iterable_from_all_points_iterable, \
                          point_list, self.mock_get_lines_seg_from_points_return_nothing, \
                          'a', 'b', 'c')
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()