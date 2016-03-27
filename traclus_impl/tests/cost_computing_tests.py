'''
Created on Dec 29, 2015

@author: Alex
'''
import math
from traclus_impl.geometry import Point
from traclus_impl.trajectory import Trajectory
import unittest


class TrajectoryCostTests(unittest.TestCase):
    
    DECIMAL_PRECISION = 11

    def build_test_object(self, points, model_cost, encoding_cost, start, end):
        traj = Trajectory(0)
        traj.points.extend(map(lambda point: Point(point[0], point[1]), points))
        return {'trajectory': traj, 'model_cost': model_cost, \
               'encoding_cost': encoding_cost, 'total_cost': model_cost + encoding_cost, \
               'start': start, 'end': end}
        
    def setUp(self):
        self.test_trajectories = []
        points = [(0, 0), (1, 0), (2, 0)]
        test_object = self.build_test_object(points, math.log(2.0, 2), 0.0, 0, 2)
        self.test_trajectories.append(test_object)
        
        points = [(0, 0), (1, 0), (1, 1)]
        model_cost = math.log(math.sqrt(2.0), 2)
        encoding_cost = math.log(math.sqrt(2.0), 2) + math.log(math.sqrt(2.0), 2)
        test_object = self.build_test_object(points, model_cost, encoding_cost, 0, 2)
        self.test_trajectories.append(test_object)
        
        points = [(0, 0), (1, math.sqrt(3.0)), (2, math.sqrt(3.0)), (3, 0)]
        model_cost = math.log(3.0, 2)
        encoding_cost = math.log(3.0 * math.sqrt(3.0), 2) + math.log(2 * math.sqrt(3.0), 2)
        test_object = self.build_test_object(points, model_cost, encoding_cost, 0, 3)
        self.test_trajectories.append(test_object)
        
        points = [(0, 0), (1, 0), (1, 1), (1, 2), (2, 2), (3, 2), \
                  (3, 3), (3, 4), (4, 4), (5, 4), (5, 5)]
        model_cost = math.log(3 * math.sqrt(2.0), 2)
        encoding_cost = math.log(3 * math.sqrt(2.0), 2) + math.log(3 * math.sqrt(2.0), 2)
        test_object = self.build_test_object(points, model_cost, encoding_cost, 2, 8)
        self.test_trajectories.append(test_object)
                                
        points = [(9, 5), (0, 2), (2 * math.sqrt(3.0), 4), (2 * math.sqrt(3.0), 0)]
        model_cost = math.log(4.0, 2)
        encoding_cost = math.log(4 * math.sqrt(3.0), 2) + math.log(4.0 * math.sqrt(3.0), 2)
        self.test_trajectories.append(self.build_test_object(points, model_cost, encoding_cost, 1, 3))
        
        points = [(0, 0), (1, 0), (4, 3)]
        test_object = self.build_test_object(points, 0.0, 0.0, 0, 1)
        self.test_trajectories.append(test_object)
        
    def test_costs(self):
        for test_case in self.test_trajectories:
            model_cost = test_case['trajectory'].model_cost(test_case['start'], test_case['end'])
            encoding_cost = test_case['trajectory'].encoding_cost(test_case['start'], test_case['end'])
            self.assertAlmostEqual(model_cost, test_case['model_cost'], \
                                   TrajectoryCostTests.DECIMAL_PRECISION, \
                                   "model cost incorrect for " + str(test_case) + \
                                   " found " + str(model_cost))
            self.assertAlmostEqual(encoding_cost, test_case['encoding_cost'], \
                                   TrajectoryCostTests.DECIMAL_PRECISION, \
                                   "encoding cost incorrect for " + str(test_case) + \
                                   " found " + str(encoding_cost))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()