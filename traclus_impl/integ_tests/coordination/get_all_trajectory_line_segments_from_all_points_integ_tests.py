'''
Created on Jan 14, 2016

@author: Alex
'''
import unittest
from traclus_impl.geometry import Point

class GetAllTrajectoryLineSegmentsFromAllPointsIntegTest(unittest.TestCase):

    def test_normal_case(self):
        points = [[Point(0, 0), Point(1, 1), Point(2, 0), Point(3, 1), Point(4, 0)], \
                      [Point(0, 1), Point(1, 2), Point(2, 1), Point(3, 2), Point(4, 1)]]

        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()