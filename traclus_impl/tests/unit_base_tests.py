'''
Created on Jan 6, 2016

@author: Alex
'''
from traclus_impl.geometry import LineSegment, Point
from traclus_impl.representative_trajectory_average_inputs import DECIMAL_MAX_DIFF_FOR_EQUALITY
from traclus_impl.traclus_dbscan import TrajectoryLineSegment
import unittest


class UnitBaseTests(unittest.TestCase):
    def create_trajectory_line_seg(self, start, end, traj_id, original_position=None):
        return TrajectoryLineSegment(LineSegment(Point(start[0], start[1]), \
                                                              Point(end[0], end[1])), traj_id, original_position)
        
    def create_simple_line_seg(self, start, end):
        return LineSegment(Point(start[0], start[1]), Point(end[0], end[1]))
    
    def verify_iteration_raises(self, exception_type, iterable):
        func = lambda x: [h for h in x]
        self.assertRaises(exception_type, func, iterable)
    
    def lines_almost_equal(self, a, b):
        return abs(a.start.x - b.start.x) < DECIMAL_MAX_DIFF_FOR_EQUALITY and \
            abs(a.start.y - b.start.y) < DECIMAL_MAX_DIFF_FOR_EQUALITY and \
            abs(a.end.x - b.end.x) < DECIMAL_MAX_DIFF_FOR_EQUALITY and \
            abs(a.end.y - b.end.y) < DECIMAL_MAX_DIFF_FOR_EQUALITY        
    
    def verify_lines_almost_equal(self, a, b):
        self.assertAlmostEquals(a.start.x, b.start.x, delta=DECIMAL_MAX_DIFF_FOR_EQUALITY)
        self.assertAlmostEquals(a.start.y, b.start.y, delta=DECIMAL_MAX_DIFF_FOR_EQUALITY)
        self.assertAlmostEquals(a.end.x, b.end.x, delta=DECIMAL_MAX_DIFF_FOR_EQUALITY)
        self.assertAlmostEquals(a.end.y, b.end.y, delta=DECIMAL_MAX_DIFF_FOR_EQUALITY)

    def verify_iterable_equals_list(self, iterable_ob, list_ob):
        count = 0
        for item in iterable_ob:
            count += 1
        
        self.assertEqual(count, len(list_ob), 
                         "Lengths differ. Iterable length: " + str(count) + \
                         ". List length: " + str(len(list_ob)) + \
                         ". Iterable: " + str(iterable_ob) + \
                         ". List: " + str(list_ob))
        if count > 0:
            i = 0
            for item in iterable_ob:
                self.assertEquals(item, list_ob[i])
                i += 1
            self.assertEquals(i, count, "wasn't able to iterate over items a second time")
            
    def verify_iterable_works_more_than_once(self, iterable, list_ob):
        self.verify_iterable_equals_list(iterable, list_ob)
        self.verify_iterable_equals_list(iterable, list_ob)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()