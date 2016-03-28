'''
Created on Jan 13, 2016

@author: Alex
'''
import unittest
from traclus_impl.tests.unit_base_tests import UnitBaseTests
from traclus_impl.line_segment_averaging import get_representative_line_from_trajectory_line_segments
from traclus_impl.geometry import Point

class FindRepresentativeLineSegmentsTest(UnitBaseTests):

    def testName(self):
        pass
    
    def test_simple_lines(self):
        traj_line_segments = [self.create_trajectory_line_seg(start=(0.0, 0.0), end=(1.0, 0.0), traj_id=0), \
                         self.create_trajectory_line_seg(start=(0.0, 1.0), end=(1.0, 1.0), traj_id=1)]
        res = get_representative_line_from_trajectory_line_segments(traj_line_segments, 1, 0)
        expected = [Point(0, 0.5), Point(1, 0.5)]
        for p in res:
            self.assertEquals(p.__class__, Point)
        self.verify_iterable_works_more_than_once(iterable=res, list_ob=expected)
        
    def test_three_lines(self):
        traj_line_segments = [self.create_trajectory_line_seg((0.0, 0.0), (2.0, 0.0), 0), \
                              self.create_trajectory_line_seg(start=(0.0, 1.0), end=(2.0, 1.0), traj_id=2), \
                              self.create_trajectory_line_seg(start=(0.0, 2.0), end=(2.0, 2.0), traj_id=1)]
        res = get_representative_line_from_trajectory_line_segments(traj_line_segments, 1, 0)
        expected = [Point(0, 1), Point(2, 1)]
        self.verify_iterable_works_more_than_once(iterable=res, list_ob=expected)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()