'''
Created on Mar 24, 2016

@author: Alex
'''
import math
from traclus_impl.geometry import LineSegment, Point, Vec2
from traclus_impl.representative_trajectory_average_inputs import DECIMAL_MAX_DIFF_FOR_EQUALITY
import unittest


class GeometryTest(unittest.TestCase):
    horizontal_line = LineSegment.from_tuples((0, 0), (2, 0))
    vertical_line = LineSegment.from_tuples((0, 0), (0, 2))
    line_at_45_degrees = LineSegment.from_tuples((0, 0), (1, 1))
    line_at_30_degrees = LineSegment.from_tuples((2, 2), (2 + math.sqrt(3.0), 3))
    line_at_60_degrees = LineSegment.from_tuples((0, 0), (1, math.sqrt(3.0)))
    line_at_135_degrees = LineSegment.from_tuples((3, 4), (2, 5))
    line_at_225_degrees = LineSegment.from_tuples((3, 4), (1, 2))
    line_at_315_degrees = LineSegment.from_tuples((-1, -1), (0, -2))
    
    def test_all_sine_coefficient_computing(self):
        actual = GeometryTest.horizontal_line.sine_of_angle_with(GeometryTest.line_at_45_degrees)
        self.assertEquals(1.0 / math.sqrt(2.0), actual)
        
        actual = GeometryTest.line_at_30_degrees.sine_of_angle_with(GeometryTest.line_at_60_degrees)
        self.assertEquals(0.5, actual)
        
        actual = GeometryTest.line_at_60_degrees.sine_of_angle_with(GeometryTest.line_at_30_degrees)
        self.assertEquals(-0.5, actual)
        
        actual = GeometryTest.line_at_135_degrees.sine_of_angle_with(GeometryTest.line_at_45_degrees)
        self.assertAlmostEquals(-1, actual, delta=DECIMAL_MAX_DIFF_FOR_EQUALITY)
        
        actual = GeometryTest.line_at_225_degrees.sine_of_angle_with(GeometryTest.line_at_45_degrees)
        self.assertEquals(0, actual)
        
        actual = GeometryTest.line_at_225_degrees.sine_of_angle_with(GeometryTest.line_at_135_degrees)
        self.assertAlmostEquals(-1, actual, delta=DECIMAL_MAX_DIFF_FOR_EQUALITY)
        
        actual = GeometryTest.line_at_315_degrees.sine_of_angle_with(GeometryTest.line_at_45_degrees)
        self.assertAlmostEquals(1, actual, delta=DECIMAL_MAX_DIFF_FOR_EQUALITY)
        
    def test_distance_to_projection_computing(self):
        def run_test_case(point, start, end, expected):
            line_seg = LineSegment.from_tuples(start, end)
            point = Point(point[0], point[1])
            self.assertAlmostEquals(expected, point.distance_to_projection_on(line_seg), \
                                    delta=DECIMAL_MAX_DIFF_FOR_EQUALITY)
            
        run_test_case((3.5, 4.5), (3, 3), (5, 5), math.sqrt(2.0) / 2.0)
        run_test_case((4.5, 3.5), (3, 3), (5, 5), math.sqrt(2.0) / 2.0)
        run_test_case((-4, 5), (10, 10), (11, 10), 5)
        run_test_case((-4, 5), (10, 10), (10, 11), 14)
        run_test_case((-5, -5), (-7, -4), (-6, -2), math.sqrt(1.0 + 4.0))
        run_test_case((0, 0), (4, 2), (4, 6), 4.0)
        run_test_case((0, 2), (4, 2), (4, 6), 4.0)
        
    def test_rotation(self):
        def run_test_case(vector, angle, expected):
            actual = vector.rotated(angle)
            self.assertAlmostEquals(expected.x, actual.x, delta=DECIMAL_MAX_DIFF_FOR_EQUALITY)
            self.assertAlmostEquals(expected.y, actual.y, delta=DECIMAL_MAX_DIFF_FOR_EQUALITY)
            
        run_test_case(Vec2(0, 1), -90, Vec2(1, 0))
        run_test_case(Vec2(math.sqrt(2.0), 0), 45, Vec2(1, 1))

        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_does_sine_of_angle_correctly']
    unittest.main()