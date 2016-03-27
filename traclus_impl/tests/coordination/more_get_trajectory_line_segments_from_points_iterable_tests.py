'''
Created on Jan 10, 2016

@author: Alex
'''
import unittest

from traclus_impl.coordination import get_trajectory_line_segments_from_points_iterable
from traclus_impl.mutable_float import MutableNumber
from traclus_impl.tests.unit_base_tests import UnitBaseTests


class GetTrajectoryLineSegmentsFromPointsTest(UnitBaseTests):

    class MockTrajectoryLineSegFactory:
        def new_trajectory_line_seg(self, line_segment, trajectory_id):
            return (line_segment[1] - line_segment[0]) * trajectory_id
        
    def create_mock_partitioning_func(self, keeper_func):
        index = MutableNumber(0)
        def _func(trajectory_point_list):
            for x in trajectory_point_list:
                if keeper_func(x):
                    yield index.get_val()
                index.increment(1)
                
        return _func
    
    def mock_line_segment_from_points_func(self, a, b):
        return [a, b]

    def test_normal_case(self):
        list = [0, 1, 2, 3, 6, 5, 12]
        partitioning_func = self.create_mock_partitioning_func(keeper_func=lambda x: True if x % 2 == 0 else False)
        traj_id = 4
        expected = [8, 16, 24]
        res = get_trajectory_line_segments_from_points_iterable(point_iterable=list, \
                                                                trajectory_line_segment_factory=self.MockTrajectoryLineSegFactory(), \
                                                                trajectory_id=traj_id, \
                                                                trajectory_partitioning_func=partitioning_func, \
                                                                line_seg_from_points_func=self.mock_line_segment_from_points_func)
        self.verify_iterable_works_more_than_once(res, expected)
        
    def test_normal_case_odd_filter_function(self):
        list = [3, 0, 5, 2, 9, 4, 15]
        partitioning_func = self.create_mock_partitioning_func(keeper_func=lambda x: True if x % 2 == 1 else False)
        traj_id = 3
        expected = [6, 12, 18]
        res = get_trajectory_line_segments_from_points_iterable(point_iterable=list, \
                                                                trajectory_line_segment_factory=self.MockTrajectoryLineSegFactory(), \
                                                                trajectory_id=traj_id, \
                                                                trajectory_partitioning_func=partitioning_func, \
                                                                line_seg_from_points_func=self.mock_line_segment_from_points_func)
        self.verify_iterable_works_more_than_once(res, expected)
        
    def test_empty_input(self):
        list = []
        partitioning_func = self.create_mock_partitioning_func(keeper_func=lambda x: True if x % 2 == 0 else False)
        traj_id = 4
        self.assertRaises(ValueError, get_trajectory_line_segments_from_points_iterable, list, \
                                                                self.MockTrajectoryLineSegFactory(), \
                                                                traj_id, \
                                                                partitioning_func, \
                                                                self.mock_line_segment_from_points_func)
        
    def test_single_input(self):
        list = [9]
        partitioning_func = self.create_mock_partitioning_func(keeper_func=lambda x: True if x % 2 == 0 else False)
        traj_id = 4
        self.assertRaises(ValueError, get_trajectory_line_segments_from_points_iterable, list, \
                                                                self.MockTrajectoryLineSegFactory(), \
                                                                traj_id, \
                                                                partitioning_func, \
                                                                self.mock_line_segment_from_points_func)
        
    def test_bad_first_index(self):
        list = [1, 1, 2, 3, 6, 5, 12]
        partitioning_func = self.create_mock_partitioning_func(keeper_func=lambda x: True if x % 2 == 0 else False)
        traj_id = 4
        self.assertRaises(ValueError, get_trajectory_line_segments_from_points_iterable, list, \
                                                                self.MockTrajectoryLineSegFactory(), \
                                                                traj_id, \
                                                                partitioning_func, \
                                                                self.mock_line_segment_from_points_func)
        
    def test_bad_last_index(self):
        list = [0, 1, 2, 3, 6, 5, 13]
        partitioning_func = self.create_mock_partitioning_func(keeper_func=lambda x: True if x % 2 == 0 else False)
        traj_id = 4
        self.assertRaises(ValueError, get_trajectory_line_segments_from_points_iterable, list, \
                                                                self.MockTrajectoryLineSegFactory(), \
                                                                traj_id, \
                                                                partitioning_func, \
                                                                self.mock_line_segment_from_points_func)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()