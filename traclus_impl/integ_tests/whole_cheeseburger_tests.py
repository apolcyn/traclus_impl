'''
Created on Jan 13, 2016

@author: Alex
'''
import unittest
from tests.unit_base_tests import UnitBaseTests
from planar import Point
from coordination import the_whole_enchilada
import math
from representative_trajectory_average_inputs import DECIMAL_MAX_DIFF_FOR_EQUALITY

class JumboShrimpTest(UnitBaseTests):
    
    def verify_point_iterable_almost_equals_list(self, iterable, expected_list):
        total_count = 0
        
        for rep_line_seg in iterable:
            self.assertTrue(total_count < len(expected_list))
            count = 0
            for point in rep_line_seg:
                self.assertTrue(count < len(expected_list[total_count]))
                self.assertAlmostEquals(point.x, expected_list[total_count][count].x, delta=DECIMAL_MAX_DIFF_FOR_EQUALITY)
                self.assertAlmostEquals(point.y, expected_list[total_count][count].y, delta=DECIMAL_MAX_DIFF_FOR_EQUALITY)
                self.assertTrue(point.almost_equals(expected_list[total_count][count]))
                count += 1
            self.assertEquals(count, len(expected_list[total_count]))
            total_count += 1
        self.assertEquals(total_count, len(expected_list))
        
    def test_two_line_segs(self):
        points = [[Point(0, 1), Point(1, 1)], \
                  [Point(0, 0), Point(1, 0)]]
        expected = [[Point(0, 0.5), (1, 0.5)]]
        res = the_whole_enchilada(point_iterable_list=points, \
                                  epsilon=100, min_neighbors=1, min_num_trajectories_in_cluster=2, min_vertical_lines=2, min_prev_dist=1.0)
        self.verify_iterable_works_more_than_once(iterable=res, list_ob=expected)
        
    def test_two_line_segs_two_clusters(self):
        points = [[Point(0, 1), Point(1, 1)], \
                  [Point(0, 0), Point(1, 0)]]
        expected = [[Point(0, 1), Point(1, 1)], \
                  [Point(0, 0), Point(1, 0)]]
        res = the_whole_enchilada(point_iterable_list=points, \
                                  epsilon=0.5, min_neighbors=0, min_num_trajectories_in_cluster=1, min_vertical_lines=1, min_prev_dist=1.0)
        self.verify_iterable_works_more_than_once(iterable=res, list_ob=expected)
        
    def test_three_by_three_two_clusters(self):
        points = [[Point(0, 1), Point(2, 1), Point(4, 1)], \
                  [Point(0, 0), Point(2, 0), Point(4, 0)], \
                  [Point(0, 3), Point(2, 3), Point(4, 3)]]
        expected = [[Point(0, 0.5), Point(4, 0.5)], \
                  [Point(0, 3), Point(4, 3)]]
        res = the_whole_enchilada(point_iterable_list=points, \
                                  epsilon=1, min_neighbors=0, min_num_trajectories_in_cluster=1, min_vertical_lines=1, min_prev_dist=1.0)
        self.verify_iterable_works_more_than_once(iterable=res, list_ob=expected)
        
    def test_one_long_line_joins_two_short_lines(self):
        points = [[Point(0, 1), Point(20, 1), Point(40, 1), Point(60, 1), Point(80, 1)], \
                  [Point(0, 0), Point(20, 0)], \
                  [Point(60, 2), Point(80, 2)]]
        expected = [[Point(0, 0.5), Point(20, 0.5), Point(60, 1.5), Point(80, 1.5)]]
        res = the_whole_enchilada(point_iterable_list=points, \
                                  epsilon=1, min_neighbors=2, min_num_trajectories_in_cluster=3, min_vertical_lines=2, min_prev_dist=10.0)
        self.verify_iterable_works_more_than_once(iterable=res, list_ob=expected)
        
    def test_two_45_degree_line_segments(self):
        points = [[Point(0, 1), Point(1, 0)], \
                  [Point(1, 2), Point(2, 1)]]
        expected = [[Point(0.5, 1.5), Point(1.5, 0.5)]]
        res = the_whole_enchilada(point_iterable_list=points, \
                                  epsilon=math.sqrt(2.0), min_neighbors=1, min_num_trajectories_in_cluster=2, \
                                  min_vertical_lines=2, \
                                  min_prev_dist=math.sqrt(2.0) - DECIMAL_MAX_DIFF_FOR_EQUALITY)
        self.verify_point_iterable_almost_equals_list(iterable=res, expected_list=expected)
        
    def test_two_vertical_line_segments(self):
        points = [[Point(0, 0), Point(0, 1)], \
                  [Point(1, 0), Point(1, 1)]]
        expected = [[Point(0.5, 0.0), Point(0.5, 1)]]
        res = the_whole_enchilada(point_iterable_list=points, \
                                  epsilon=100, min_neighbors=0, min_num_trajectories_in_cluster=1, min_vertical_lines=1, min_prev_dist=0)
        self.verify_point_iterable_almost_equals_list(iterable=res, expected_list=expected)
        
    def test_two_minus_45_degree_lines_segs(self):
        points = [[Point(1, 0), Point(2, 1)], \
                  [Point(0, 1), Point(1, 2)]]
        expected = [[Point(0.5, 0.5), Point(1.5, 1.5)]]
        res = the_whole_enchilada(point_iterable_list=points, \
                                  epsilon=math.sqrt(2.0) + DECIMAL_MAX_DIFF_FOR_EQUALITY, \
                                  min_neighbors=1, min_num_trajectories_in_cluster=2, \
                                  min_vertical_lines=2, \
                                  min_prev_dist=math.sqrt(2.0) - DECIMAL_MAX_DIFF_FOR_EQUALITY)
        self.verify_point_iterable_almost_equals_list(iterable=res, expected_list=expected)
        
    def test_four_points_in_a_row_diagonally(self):
        points = [[Point(0, 0), Point(10, 10), Point(20, 20), Point(30, 30)]]
        expected = [[Point(0, 0), Point(30, 30)]]
        res = the_whole_enchilada(point_iterable_list=points, \
                                  epsilon=0, \
                                  min_neighbors=0, min_num_trajectories_in_cluster=1, \
                                  min_vertical_lines=1, \
                                  min_prev_dist=math.sqrt(2.0) - DECIMAL_MAX_DIFF_FOR_EQUALITY)
        self.verify_point_iterable_almost_equals_list(iterable=res, expected_list=expected)
        
    def test_four_points_in_a_row_slight_diagonally(self):
        points = [[Point(0, 0), Point(100, 10), Point(200, 20), Point(300, 30)]]
        expected = [[Point(0, 0), Point(300, 30)]]
        res = the_whole_enchilada(point_iterable_list=points, \
                                  epsilon=0, \
                                  min_neighbors=0, min_num_trajectories_in_cluster=1, \
                                  min_vertical_lines=1, \
                                  min_prev_dist=1)
        self.verify_point_iterable_almost_equals_list(iterable=res, expected_list=expected)
        
    def test_three_points_in_a_row_negative_diagonal(self):
        points = [[Point(0, 20), Point(10, 10), Point(20, 0)]]
        expected = [[Point(0, 20), Point(20, 0)]]
        res = the_whole_enchilada(point_iterable_list=points, \
                                  epsilon=0, \
                                  min_neighbors=0, min_num_trajectories_in_cluster=1, \
                                  min_vertical_lines=1, \
                                  min_prev_dist=(2 * math.sqrt(2.0) - DECIMAL_MAX_DIFF_FOR_EQUALITY))
        self.verify_point_iterable_almost_equals_list(iterable=res, expected_list=expected)
        
    def test_parrallel_distance_joins_two_lines_segs(self):
        points = [[Point(0, 0), Point(1, 0)], \
                  [Point(2, 0), Point(3, 0)]]
        expected = [[Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0)]]
        res = the_whole_enchilada(point_iterable_list=points, \
                                  epsilon=1, \
                                  min_neighbors=1, min_num_trajectories_in_cluster=2, \
                                  min_vertical_lines=1, \
                                  min_prev_dist=1)
        self.verify_point_iterable_almost_equals_list(iterable=res, expected_list=expected)

    def test_partition_happens_with_three_points_in_a_row_horizontally(self):
        points = [[Point(0, 0), Point(2, 0), Point(4, 0)]]
        expected = [[Point(0, 0), Point(4, 0)]]
        res = the_whole_enchilada(point_iterable_list=points, \
                                  epsilon=0, \
                                  min_neighbors=0, min_num_trajectories_in_cluster=1, \
                                  min_vertical_lines=1, \
                                  min_prev_dist=4)
        self.verify_iterable_works_more_than_once(iterable=res, list_ob=expected)
        self.verify_point_iterable_almost_equals_list(iterable=res, expected_list=expected)
        
    def test_three_vertical_points_in_a_row(self):
        points = [[Point(0, 0), Point(0, 2), Point(0, 4)]]
        expected = [[Point(0, 0), Point(0, 4)]]
        res = the_whole_enchilada(point_iterable_list=points, \
                                  epsilon=1, \
                                  min_neighbors=0, min_num_trajectories_in_cluster=1, \
                                  min_vertical_lines=1, \
                                  min_prev_dist=1)
        self.verify_point_iterable_almost_equals_list(iterable=res, expected_list=expected)
        
    def test_three_vertical_points_in_a_row_small_spacing(self):
        points = [[Point(0, 0), Point(0, 1.1), Point(0, 2.2)]]
        expected = [[Point(0, 0), Point(0, 2.2)]]
        res = the_whole_enchilada(point_iterable_list=points, \
                                  epsilon=1, \
                                  min_neighbors=0, min_num_trajectories_in_cluster=1, \
                                  min_vertical_lines=1, \
                                  min_prev_dist=1)
        self.verify_point_iterable_almost_equals_list(iterable=res, expected_list=expected)
        
    def test_three_vertical_points_in_a_row_sub_two_dist(self):
        points = [[Point(0, 0), Point(0, 2), Point(0, 4)]]
        expected = [[Point(0, 0), Point(0, 4)]]
        res = the_whole_enchilada(point_iterable_list=points, \
                                  epsilon=1, \
                                  min_neighbors=0, min_num_trajectories_in_cluster=1, \
                                  min_vertical_lines=1, \
                                  min_prev_dist=1)
        self.verify_point_iterable_almost_equals_list(iterable=res, expected_list=expected)
        
    def test_single_line_seg(self):
        points = [[Point(0, 0), Point(2, 0)]]
        expected = [[Point(0, 0), Point(2, 0)]]
        res = the_whole_enchilada(point_iterable_list=points, \
                                  epsilon=1, \
                                  min_neighbors=0, min_num_trajectories_in_cluster=1, \
                                  min_vertical_lines=1, \
                                  min_prev_dist=1)
        self.verify_point_iterable_almost_equals_list(iterable=res, expected_list=expected)
        
    def test_normal_turning_line(self):
        points = [[Point(0, 0), Point(20, 20), Point(40, 0), Point(60, 20), Point(80, 0)]]
        expected = [[Point(0, 0), Point(20, 20), Point(40, 0), Point(60, 20), Point(80, 0)]]
        res = the_whole_enchilada(point_iterable_list=points, \
                                  epsilon=100, \
                                  min_neighbors=3, min_num_trajectories_in_cluster=1, \
                                  min_vertical_lines=1, \
                                  min_prev_dist=1)
        self.verify_point_iterable_almost_equals_list(iterable=res, expected_list=expected)
        
    def test_trajectory_loops_around(self):
        points = [[Point(0, 1000.0), Point(1000.0, 2000.0), Point(2000.0, 1000.0), Point(1000.0, 0), Point(0, 1000.0)]]
        expected = [[Point(0, 1000), Point(1000, 1000), Point(2000, 1000)]]
        res = the_whole_enchilada(point_iterable_list=points, \
                                  epsilon=3000, \
                                  min_neighbors=3, min_num_trajectories_in_cluster=1, \
                                  min_vertical_lines=1, \
                                  min_prev_dist=10)
        self.verify_point_iterable_almost_equals_list(iterable=res, expected_list=expected)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()