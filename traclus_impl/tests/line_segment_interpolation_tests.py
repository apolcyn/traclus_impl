'''
Created on Jan 5, 2016

@author: Alex
'''
import unittest
from traclus_impl.line_segment_averaging import interpolate_within_line_segment
from traclus_impl.geometry import LineSegment

class LineSegmentInterpolationTest(unittest.TestCase):

    def create_line_segment(self, start, end):
        return LineSegment.from_tuples(start, end)

    def setUp(self):
        pass

    def test_param_not_within_segment(self):
        line_seg = self.create_line_segment((0, 1), (3, 4))
        self.assertRaises(Exception, interpolate_within_line_segment, line_seg, 4.0001)
        self.assertRaises(Exception, interpolate_within_line_segment, line_seg, -0.00001)
    
    def test_line_right_up(self):
        line_seg = self.create_line_segment((1, 1), (5, 3))
        self.assertEquals(interpolate_within_line_segment(line_seg, 2.5), 1.75)
        self.assertEquals(interpolate_within_line_segment(line_seg, 2), 1.5)
        
    def test_line_right_down(self):
        line_seg = self.create_line_segment((1, 1), (5, -1))
        self.assertEquals(interpolate_within_line_segment(line_seg, 2), 0.5)
        
    def test_line_left_up(self):
        line_seg = self.create_line_segment((2, 2), (-2, 4))
        self.assertEquals(interpolate_within_line_segment(line_seg, 0.5), 2.75)
        
    def test_line_left_down(self):
        line_seg = self.create_line_segment((2, 2), (-2, 0))
        self.assertEquals(interpolate_within_line_segment(line_seg, 0.5), 1.25)
        self.assertEquals(interpolate_within_line_segment(line_seg, 1), 1.5)
        
    def test_at_end(self):
        line_seg = self.create_line_segment((2, 2), (4, 4))
        self.assertEquals(interpolate_within_line_segment(line_seg, 4), 4)
        
    def test_at_start(self):
        line_seg = self.create_line_segment((2, 2), (4, 4))
        self.assertEquals(interpolate_within_line_segment(line_seg, 2), 2)
        
    def test_vertical_line(self):
        line_seg = self.create_line_segment((2, 2), (2, 4))
        self.assertEquals(interpolate_within_line_segment(line_seg, 2), 3)
        
    def test_horizontal_line(self):
        line_seg = self.create_line_segment((2, 2), (5, 2))
        self.assertEquals(interpolate_within_line_segment(line_seg, 3), 2.0)
        self.assertEquals(interpolate_within_line_segment(line_seg, 3.5), 2)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()