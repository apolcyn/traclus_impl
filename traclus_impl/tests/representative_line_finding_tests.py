'''
Created on Jan 6, 2016

@author: Alex
'''
import unittest
from traclus_impl.representative_line_finding import get_average_vector, get_rotated_line_segment
from unit_base_tests import UnitBaseTests
from traclus_impl.geometry import Vec2
import math
from traclus_impl.representative_trajectory_average_inputs import DECIMAL_MAX_DIFF_FOR_EQUALITY

class RepresentativeLineFindingTests(UnitBaseTests):

    def test_get_average_vector(self):
        lines = [self.create_simple_line_seg((0, 0), (1, 1)), \
                 self.create_simple_line_seg((1, 1), (3, -7)), \
                 self.create_simple_line_seg((1, 0), (-4, 4)), \
                 self.create_simple_line_seg((4, 2), (1, -3))]
        self.assertEquals(get_average_vector(lines), Vec2(11, -8))
        self.assertEquals(get_average_vector([self.create_simple_line_seg((0, 1), (2, 9))]), Vec2(2, 8))
        
    def test_gets_average_vector_of_diamond(self):
        lines = [self.create_simple_line_seg((0, 100), (100, 200)), \
                 self.create_simple_line_seg((100, 200), (200, 100)), \
                 self.create_simple_line_seg((200, 100), (100, 0)), \
                 self.create_simple_line_seg((100, 0), (0, 100))]
        self.assertEquals(get_average_vector(lines), Vec2(400, 0))

    def test_get_average_vector_empty_input(self):
        self.assertRaises(Exception, get_average_vector, [])
        self.assertRaises(Exception, get_average_vector, None)
        
    def test_get_rotated_line_segment_right_hemisphere(self):
        before = self.create_simple_line_seg((0, 1), (1, 2))
        after = self.create_simple_line_seg((1 / math.sqrt(2.0), 1 / math.sqrt(2.0)), \
                                            (math.sqrt(2.0) + 1 / math.sqrt(2.0), 1 / math.sqrt(2.0)))
        self.assertTrue(get_rotated_line_segment(before, -45).almost_equals(after))
        self.assertTrue(get_rotated_line_segment(after, 45).almost_equals(before))
        
    def test_basic_central_rotate_45(self):
        before = self.create_simple_line_seg((0, 0), (1, 1))
        after = self.create_simple_line_seg((0, 0), (math.sqrt(2), 0))
        self.assertTrue(get_rotated_line_segment(before, -45).almost_equals(after))
        self.assertTrue(get_rotated_line_segment(after, 45).almost_equals(before))
        
    def test_basic_central_rotate_90(self):
        before = self.create_simple_line_seg((0, 0), (0, 1))
        after = self.create_simple_line_seg((0, 0), (1, 0))
        self.assertTrue(get_rotated_line_segment(before, -90).almost_equals(after))
        self.assertTrue(get_rotated_line_segment(after, 90).almost_equals(before))
        
    def test_basic_centrial_rotate_90_left_hemi(self):
        before = self.create_simple_line_seg((0, 0), (-1, 0))
        after = self.create_simple_line_seg((0, 0), (0, -1))
        self.assertTrue(get_rotated_line_segment(before, 90).almost_equals(after))
        self.assertTrue(get_rotated_line_segment(after, -90).almost_equals(before))
        
    def test_rotate_by_zero(self):
        test_ob = self.create_simple_line_seg((0, 1), (1, 2))
        self.assertEquals(get_rotated_line_segment(test_ob, 0.0), test_ob)
        
    def test_rotate_by_30(self):
        before = self.create_simple_line_seg((1, math.sqrt(3.0)), (math.sqrt(3.0), 1))
        after = self.create_simple_line_seg((math.sqrt(3.0), 1), (2, 0))
        self.assertTrue(get_rotated_line_segment(before, -30).almost_equals(after))
        self.assertTrue(get_rotated_line_segment(after, 30).almost_equals(before))
        
    def test_bad_angle(self):
        test_ob = self.create_simple_line_seg((0, 1), (1, 2))
        self.assertRaises(Exception, get_rotated_line_segment, test_ob, -90.1)
        self.assertRaises(Exception, get_rotated_line_segment, test_ob, 90.1)
        self.assertRaises(Exception, get_rotated_line_segment, test_ob, 181)
        self.assertRaises(Exception, get_rotated_line_segment, test_ob, -181)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()