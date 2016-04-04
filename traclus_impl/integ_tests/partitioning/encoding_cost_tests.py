'''
Created on Mar 31, 2016

@author: alexpolcyn
'''
import unittest
import math
from traclus_impl.geometry import Point, LineSegment
from traclus_impl.trajectory_partitioning import encoding_cost
from traclus_impl.distance_functions import angular_distance,\
    perpendicular_distance
from traclus_impl.representative_trajectory_average_inputs import DECIMAL_MAX_DIFF_FOR_EQUALITY


class EncodingCostTest(unittest.TestCase):

    def get_line_segs(self, points):
        return map(lambda i: LineSegment(points[i], points[i + 1]), 
                   range(0, len(points) - 1))
        
    def test_line_seg_distances(self):
        seg = LineSegment(Point(0, 0), Point(0, 2))
        other = LineSegment(Point(0, 0), Point(2, 2))
        
        perp_dist = perpendicular_distance(seg, other)
        ang_dist = angular_distance(seg, other)
        
        self.assertAlmostEquals(math.sqrt(2.0), perp_dist, delta=DECIMAL_MAX_DIFF_FOR_EQUALITY)
        self.assertAlmostEquals(math.sqrt(2.0), ang_dist, delta=DECIMAL_MAX_DIFF_FOR_EQUALITY)
    
    def test_right_angle_encoding_cost(self):
        points = [Point(0, 0), Point(0, 2), Point(2, 2)]
        line_segs = [LineSegment(Point(0, 0), Point(0, 2)), 
                     LineSegment(Point(0, 2), Point(2, 2))]
        
        #line_segs = self.get_line_segs(points)
        
        actual = encoding_cost(trajectory_line_segs=line_segs, 
                               low=0, high=len(line_segs), 
                               partition_line=LineSegment(points[0], points[2]), 
                               angular_dist_func=angular_distance, 
                               perpendicular_dist_func=perpendicular_distance)
        
        self.assertAlmostEquals(math.log(2 * math.sqrt(2.0), 2) + math.log(2 * math.sqrt(2.0), 2), 
                                actual, 
                                delta=DECIMAL_MAX_DIFF_FOR_EQUALITY)
                               
                                                        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()