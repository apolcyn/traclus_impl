'''
Created on Dec 31, 2015

@author: Alex
'''
import unittest
from traclus_impl.traclus_dbscan import TrajectoryCluster, TrajectoryLineSegment
from traclus_impl.traclus_dbscan import TrajectoryLineSegmentFactory
from traclus_impl.tests.unit_base_tests import UnitBaseTests
from argparse import ArgumentError

class TrajectoryClusterTests(UnitBaseTests):

    def build_test_object(self, line_segments, expected_count, num_trajectories, expected_error = False):
        return {'geometry': line_segments, 'num_trajectories': num_trajectories, \
                'expected_count': expected_count }
        
    class Item:
        def __init__(self, trajectory_id):
            self.trajectory_id = trajectory_id
        
    def new_line_seg(self, trajectory_id):
        return self.Item(trajectory_id)

    def setUp(self):
        self.test_cases = []
        
        line_segs = [self.new_line_seg(0), self.new_line_seg(1), self.new_line_seg(2), self.new_line_seg(3)]
        self.test_cases.append(self.build_test_object(line_segs, 4, 4))
        
        line_segs = [self.new_line_seg(0), self.new_line_seg(0), self.new_line_seg(2), self.new_line_seg(3)]
        self.test_cases.append(self.build_test_object(line_segs, 3, 4))
        
        line_segs = [self.new_line_seg(0), self.new_line_seg(0), self.new_line_seg(0), self.new_line_seg(0)]
        self.test_cases.append(self.build_test_object(line_segs, 1, 1000))
        
        line_segs = [self.new_line_seg(10000), self.new_line_seg(90), self.new_line_seg(23), self.new_line_seg(23)]
        self.test_cases.append(self.build_test_object(line_segs, 3, 10001))
        
        self.test_cases.append(self.build_test_object([], 0, 100000))

    def create_cluster(self, segments, num_trajectories):
        cluster = TrajectoryCluster()
        
        for single_segment in segments:
            cluster.add_member(single_segment)
            
        return cluster

    def test_trajectory_counting(self):
        for test_ob in self.test_cases:
            cluster = self.create_cluster(test_ob['geometry'], test_ob['num_trajectories'])
            self.assertEqual(test_ob['expected_count'], cluster.num_trajectories_contained(), \
                            " found " + str(cluster.num_trajectories_contained()) + " for " + str(test_ob))
                                
    def test_trajectory_factory(self):
        line_seg = self.create_simple_line_seg((0, 0), (1, 1))
        expected = TrajectoryLineSegment(line_seg, 1)
        res = TrajectoryLineSegmentFactory().new_trajectory_line_seg(line_seg, trajectory_id=1)
        self.assertEquals(res.line_segment, expected.line_segment)
        self.assertEquals(res.trajectory_id, expected.trajectory_id)

    def test_trajectory_factory_bad_input(self):
        line_seg = self.create_simple_line_seg((0, 0), (1, 1))
        self.assertRaises(Exception, TrajectoryLineSegmentFactory().new_trajectory_line_seg, line_seg, -1)
        self.assertRaises(Exception, TrajectoryLineSegmentFactory().new_trajectory_line_seg, None, 1)
        self.assertRaises(Exception, TrajectoryLineSegmentFactory().new_trajectory_line_seg, line_seg, None)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()