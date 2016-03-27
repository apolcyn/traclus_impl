'''
Created on Dec 29, 2015

@author: Alex
'''
import math
from traclus_impl.distance_functions import parrallel_distance, perpendicular_distance, \
    angular_distance, get_total_distance_function
from traclus_impl.geometry import LineSegment
from traclus_impl.mutable_float import MutableFloat, MutableNumber
import unittest 


class DistanceFunctionTest(unittest.TestCase):
    
    DECIMAL_PRECISION = 11

    def build_test_object(self, perp_dist, parr_dist, angle_dist):
        return {'perp_dist': perp_dist, 'parr_dist': parr_dist, \
                 'angle_dist': angle_dist, 'lines': []}
    
    def add_line(self, test_object, start_a, end_a, start_b, end_b):
        line = LineSegment.from_tuples((start_a, end_a), (start_b, end_b))
        test_object['lines'].append(line)
 
    def setUp(self):
        self.test_lines = []
        
        temp = self.build_test_object(2.0, 0.0, 0.0)
        self.add_line(temp, 0, 0, 2, 0)
        self.add_line(temp, 0, 2, 2, 2)
        self.test_lines.append(temp)
        
        temp = self.build_test_object(2.0, 2.0, 0.0)
        self.add_line(temp, 0, 0, 2, 0)
        self.add_line(temp, 4, 2, 10, 2)
        self.test_lines.append(temp)
        
        temp = self.build_test_object(10.0/3, 2.0, 2.0)
        self.add_line(temp, 0, 0, 2, 0)
        self.add_line(temp, 4, 2, 4, 6)
        self.test_lines.append(temp)
        
        temp = self.build_test_object(math.sqrt(2), 3 * math.sqrt(2), math.sqrt(2))
        self.add_line(temp, 0.0, 0.0, 2.0, 0.0)
        self.add_line(temp, 4.0, 4.0, 6.0, 6.0)
        self.test_lines.append(temp)
        
        temp = self.build_test_object(0.0, 0.0, 0.0)
        self.add_line(temp, 0.0, 2.0, 4.3, 8.3)
        self.add_line(temp, 0.0, 2.0, 4.3, 8.3)
        
        temp = self.build_test_object(0.0, 0.0, 0.0)
        self.add_line(temp, 0.0, 2.0, 2.0, 2.0)
        self.add_line(temp, 0.0, 2.0, 2.0, 2.0)
        
    def test_perpendicular_distance(self):
        self.distance_test(perpendicular_distance, 'perp_dist')
        
    def test_parrallel_distance(self):
        self.distance_test(parrallel_distance, 'parr_dist')
        
    def test_angle_distance(self):
        self.distance_test(angular_distance, 'angle_dist')
        
    def distance_test(self, distance_func, distance_type):
        for line_pair in self.test_lines:
            dist = distance_func(line_pair['lines'][0], line_pair['lines'][1])
            other = distance_func(line_pair['lines'][1], line_pair['lines'][0])
            self.assertAlmostEqual(dist, other, \
                            DistanceFunctionTest.DECIMAL_PRECISION, \
                            "distance measure not symmetric. " + \
                             "found distance of " + str(dist) + " and " + str(other))
            self.assertAlmostEqual(dist, line_pair[distance_type], 
                            DistanceFunctionTest.DECIMAL_PRECISION, \
                             "incorrect distance measure for " + str(line_pair) + \
                             " found distance of " + str(dist))  
            
    def test_total_dist_func(self):
        perp_func = lambda x, y: x + y
        angle_dist = lambda x, y: x * y
        parrallel_dist = lambda x, y: 100 * x + 100 * y
        
        total_dist_func = get_total_distance_function(perp_func, angle_dist, parrallel_dist)
        self.assertEquals(total_dist_func(3, 4), 7 + 12 + 700)
        self.assertEquals(total_dist_func(7, 5), 12 + 35 + 1200)
        
    def total_dist_func_interesting_funcs(self):
        summer = lambda x, y: x + y
        multiplier = lambda x, y: x * y
        def mean_func():
            total = MutableFloat(0.0)
            count = MutableNumber(0)
            def func(num):
                total.increment(num)
                count.increment(1)
                return total.get_val() / count
        
        def get_averager(mean_computer):
            def func(list):
                map(mean_computer, list)
            return func
            
        averager = mean_func()
        perp_func = lambda x, y: reduce(summer, x) + reduce(summer, y)
        angle_func = lambda x, y: get_averager(mean_func())(x) + get_averager(mean_func())(y)
        parr_func = lambda x, y: reduce(multiplier, x) + reduce(multiplier, y)
        
        a = [2, 3, 4]
        b = [5, 6, 7]
        total_dist_func = get_total_distance_function(perp_dist_func=perp_func, \
                                                      angle_dist_func=angle_func, parrallel_dist_func=parr_func)
        self.assertEquals(total_dist_func(a, b), 9 + 3 + 24 + 18 + 6 + 210)
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()