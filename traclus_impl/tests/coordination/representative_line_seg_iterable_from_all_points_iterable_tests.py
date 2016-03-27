'''
Created on Jan 13, 2016

@author: Alex
'''
import unittest

from traclus_impl.coordination import representative_line_seg_iterable_from_all_points_iterable
from traclus_impl.tests.unit_base_tests import UnitBaseTests


class RepresentativeLineSegIterableFromAllPointsIterableTest(UnitBaseTests):
    
    class MockTrajCluster():
        def __init__(self, name, num_traj_contained):
            self.trajectories = name
            self.num_traj_contained = num_traj_contained
            
        def num_trajectories_contained(self):
            return self.num_traj_contained
        
        def get_trajectory_line_segments(self):
            return self.trajectories
        
    def mock_get_representative_line_seg_from_trajectory_caller(self, trajectories):
        return trajectories
    
    def mock_get_cluster_iterable_from_all_points_iterable_caller(self, point_list):
        for point in point_list:
            yield self.MockTrajCluster(point[0], point[1])
    
    def test_normal_case(self):
        point_list = [("bill", 3), ("fred", 1), ("sally", 7)]
        expected = ["bill", "sally"]
        res = representative_line_seg_iterable_from_all_points_iterable(point_iterable_list=point_list, \
                                                              get_cluster_iterable_from_all_points_iterable_caller=self.mock_get_cluster_iterable_from_all_points_iterable_caller, \
                                                              get_representative_line_seg_from_trajectory_caller=self.mock_get_representative_line_seg_from_trajectory_caller, 
                                                              min_num_trajectories_in_cluster=3)
        self.verify_iterable_works_more_than_once(iterable=res, list_ob=expected)
        
    def test_not_enough_trajectories_in_any_clusters(self):
        point_list = [("bill", 3), ("fred", 1), ("sally", 7)]
        expected = []
        res = representative_line_seg_iterable_from_all_points_iterable(point_iterable_list=point_list, \
                                                              get_cluster_iterable_from_all_points_iterable_caller=self.mock_get_cluster_iterable_from_all_points_iterable_caller, \
                                                              get_representative_line_seg_from_trajectory_caller=self.mock_get_representative_line_seg_from_trajectory_caller, 
                                                              min_num_trajectories_in_cluster=9)
        self.verify_iterable_works_more_than_once(iterable=res, list_ob=expected)
        
    def test_no_clusters_resulted(self):
        point_list = [0, 1, 2, 3, 4, 5]
        expected = []
        no_clusters_func = lambda x: []
        res = representative_line_seg_iterable_from_all_points_iterable(point_iterable_list=point_list, \
                                                              get_cluster_iterable_from_all_points_iterable_caller=no_clusters_func, \
                                                              get_representative_line_seg_from_trajectory_caller=self.mock_get_representative_line_seg_from_trajectory_caller, 
                                                              min_num_trajectories_in_cluster=9)
        self.verify_iterable_works_more_than_once(iterable=res, list_ob=expected)
        
    def test_caller_func(self):
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()