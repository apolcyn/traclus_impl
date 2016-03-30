'''
Created on Mar 29, 2016

@author: alexpolcyn
'''
import unittest
from traclus_impl.traclus_dbscan import TrajectoryLineSegment
from traclus_impl.geometry import LineSegment
from traclus_impl.traclus_dbscan import RtreeTrajectoryLineSegmentCandidateIndex
from unittest.case import SkipTest

class RtreeClusterCandidateIndexTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(RtreeClusterCandidateIndexTest, cls).setUpClass()
        try:
            import rtree
        except ImportError:
            raise SkipTest("rtree not importable, skipping tests, " \
                           "can't use the class under test")

    class MockDistanceCandidate(TrajectoryLineSegment):
        def __init__(self, distances, line_segment, id):
            TrajectoryLineSegment.__init__(self, 
                                           line_segment, 
                                           trajectory_id=0, 
                                           id=id)
            self.distances = distances
            
        def distance_to_candidate(self, other_candidate):
            return self.distances[other_candidate.id]
                        
    def test_only_looks_at_segments_that_intersect_with_candidates_bounding_box(self):
        distances = [0.0, 0.0, 0.0, 0.0]
        epsilon = 1.0
        line_segs = [LineSegment.from_tuples((0, 1), (1, 0)), 
                     LineSegment.from_tuples((0, 2), (1, 1)),
                     LineSegment.from_tuples((0, 4.5), (1, 3.5)),
                     LineSegment.from_tuples((0, 5.5), (1, 4.5))]
        candidates = []
        i = 0
        for seg in line_segs:
            candidates.append(self.MockDistanceCandidate(distances, seg, i))
            i += 1
        
        index = RtreeTrajectoryLineSegmentCandidateIndex(candidates=candidates, 
                                                         epsilon=epsilon)
        expected_neighbors = [[candidates[1]], 
                              [candidates[0], candidates[2]],
                              [candidates[1], candidates[3]], 
                              [candidates[2]]]
                    
        i = 0
        for cand in candidates:
            actual_neighbors = index.find_neighbors_of(cand)
            self.assertEquals(len(expected_neighbors[i]), len(actual_neighbors), 
                              "length test failed on index :" + str(i))
            for neighbor in actual_neighbors:
                self.assertIn(neighbor, expected_neighbors[i], 
                              "membership test failed on index: " + str(i))
            i += 1



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()