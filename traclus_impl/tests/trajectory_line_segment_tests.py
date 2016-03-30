'''
Created on Dec 31, 2015

@author: Alex
'''
from _ctypes import ArgumentError
from traclus_impl.generic_dbscan import ClusterCandidate
from traclus_impl.geometry import Point, LineSegment
from traclus_impl.traclus_dbscan import TrajectoryLineSegment, \
    TrajectoryLineSegmentCandidateIndex
import unittest

import unit_base_tests


class TestTrajectoryLineSegments(unit_base_tests.UnitBaseTests):

    def test_creation(self):
        self.assertRaises((Exception, ArgumentError), TrajectoryLineSegment, \
                          LineSegment(Point(0, 0), Point(1, 1)), -1)
        self.assertRaises((Exception, ArgumentError), TrajectoryLineSegment, None, 1)
        self.assertRaises((Exception, ArgumentError), TrajectoryLineSegment, \
                          LineSegment(Point(0, 0), Point(1, 1)), None)
        
    def test_num_neighbor_counting(self):
        line_segment = TrajectoryLineSegment(self.create_simple_line_seg((0, 0), (1, 1)), 1)
        line_segment.distance_to_candidate = lambda x: 0.0
        mock_canididates = [1, 2, 3, 4, 5, 6]
        index = TrajectoryLineSegmentCandidateIndex(mock_canididates, epsilon=0.1)

        self.assertRaises(Exception, line_segment.get_num_neighbors)
        index.find_neighbors_of(line_segment)
        self.assertEquals(line_segment.get_num_neighbors(), 6)
        
    def test_num_neighbor_counting_raises_if_num_neighbors_change(self):
        line_segment = TrajectoryLineSegment(self.create_simple_line_seg((0, 0), (1, 1)), 1)
        line_segment.distance_to_candidate = lambda x: 0.0
        mock_canididates = [1, 2, 3, 4, 5, 6]
        index = TrajectoryLineSegmentCandidateIndex(mock_canididates, epsilon=0.1)
        
        self.assertRaises(Exception, line_segment.get_num_neighbors)
        index.find_neighbors_of(line_segment)
        self.assertEquals(line_segment.get_num_neighbors(), 6)
        mock_canididates.append(7)
        self.assertRaises(Exception, index.find_neighbors_of, \
                          candidates=mock_canididates)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_creation']
    unittest.main()