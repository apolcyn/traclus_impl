'''
Created on Jan 9, 2016

@author: Alex
'''
import unittest
from traclus_impl.tests.unit_base_tests import UnitBaseTests
from traclus_impl.geometry import Point
from traclus_impl.trajectory_partitioning import call_partition_trajectory

class SimpleLinePartitioningIntegTest(UnitBaseTests):

    def test_simple_line_segment(self):
        trajectory = [Point(0, 0), Point(1, 1)]
        expected_par = [0, 1]
        self.verify_iterable_works_more_than_once(expected_par, \
                                                  call_partition_trajectory(trajectory_point_list=trajectory))
    def test_obvious_NOT_partition(self):
        trajectory = [Point(0, 0), Point(1, 1), Point(2, 0)]
        expected_par = [0, 1, 2]
        self.verify_iterable_works_more_than_once(expected_par, \
                                                  call_partition_trajectory(trajectory_point_list=trajectory))
        
    def test_longer_obvious_NOT_partition(self):
        trajectory = [Point(0, 0), Point(1, 1), Point(2, 0), Point(3, 1), Point(4, 0)]
        expected_par = [0, 1, 2, 3, 4]
        self.verify_iterable_works_more_than_once(call_partition_trajectory(trajectory_point_list=trajectory), 
                                                  expected_par)
        
    def test_obvious_partition(self):
        trajectory = [Point(0, 0), Point(10000, 1), Point(20000, 0)]
        expected_par = [0, 2]
        self.verify_iterable_works_more_than_once(expected_par, \
                                                  call_partition_trajectory(trajectory_point_list=trajectory))
        
    def test_longer_obvious_partition(self):
        trajectory = [Point(0, 0), Point(10000, 1), Point(20000, 0), Point(30000, 2), Point(40000, 1)]
        expected_par = [0, 4]
        self.verify_iterable_works_more_than_once(expected_par, \
                                                  call_partition_trajectory(trajectory_point_list=trajectory))
    
    def test_not_enough_points(self):
        self.assertRaises(ValueError, call_partition_trajectory, [Point(1, 1)])
        self.assertRaises(ValueError, call_partition_trajectory, [])
        
    def test_three_points_horizontal(self):
        traj = [Point(0, 0), Point(1.6, 0), Point(4.4, 0)]
        expected_par = [0, 2]
        self.verify_iterable_works_more_than_once(call_partition_trajectory(trajectory_point_list=traj), \
                                                  expected_par)  
        
    def test_three_points_horizontal_2_spacing(self):
        traj = [Point(0, 0), Point(2, 0), Point(4, 0)]
        expected_par = [0, 2]
        self.verify_iterable_works_more_than_once(call_partition_trajectory(trajectory_point_list=traj), \
                                                  expected_par)  
        
    def test_three_points_horizontal_big_spacing(self):
        traj = [Point(0, 0), Point(200, 0), Point(444, 0)]
        expected_par = [0, 2]
        self.verify_iterable_works_more_than_once(call_partition_trajectory(trajectory_point_list=traj), \
                                                  expected_par)
        
    def test_three_points_in_a_row_diagonal(self):
        traj = [Point(0, 0), Point(10, 10), Point(20, 20)]
        expected_par = [0, 2]
        self.verify_iterable_works_more_than_once(call_partition_trajectory(trajectory_point_list=traj), \
                                                  expected_par)   
        
    def test_three_points_in_a_row_diagonal_shorter_real_short(self):
        traj = [Point(0, 0), Point(0.2, 0.2), Point(0.4, 0.4)]
        expected_par = [0, 2]
        self.verify_iterable_works_more_than_once(call_partition_trajectory(trajectory_point_list=traj), \
                                                  expected_par)   
        
    def test_three_points_in_a_row_diagonal_shorter(self):
        traj = [Point(0, 0), Point(1, 1), Point(2, 2)]
        expected_par = [0, 2]
        self.verify_iterable_works_more_than_once(call_partition_trajectory(trajectory_point_list=traj), \
                                                  expected_par)  
        
    def test_doesnt_partition_diamond(self):
        traj = [Point(0, 10), Point(10, 20), Point(20, 10), Point(10, 0), Point(0, 10)]     
        expected_par = [0, 1, 2, 3, 4]
        self.verify_iterable_works_more_than_once(call_partition_trajectory(trajectory_point_list=traj),
                                            expected_par) 
        
    def test_doesnt_partition_big_diamond(self):
        traj = [Point(0, 100), Point(100, 200), Point(200, 100), Point(100, 0), Point(0, 100)]     
        expected_par = [0, 1, 2, 3, 4]
        self.verify_iterable_works_more_than_once(call_partition_trajectory(trajectory_point_list=traj),
                                            expected_par) 

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()