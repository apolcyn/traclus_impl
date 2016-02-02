'''
Created on Dec 31, 2015

@author: Alex
'''
import unittest
from _ctypes import ArgumentError
from traclus_dbscan.traclus_dbscan import TrajectoryLineSegment
from planar import LineSegment
from planar import Point

class TestTrajectoryLineSegments(unittest.TestCase):

    def test_creation(self):
        self.assertRaises((Exception, ArgumentError), TrajectoryLineSegment, \
                          LineSegment.from_points([Point(0, 0), Point(1, 1)]), -1)
        self.assertRaises((Exception, ArgumentError), TrajectoryLineSegment, None, 1)
        self.assertRaises((Exception, ArgumentError), TrajectoryLineSegment, \
                          LineSegment.from_points([Point(0, 0), Point(1, 1)]), None)



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_creation']
    unittest.main()