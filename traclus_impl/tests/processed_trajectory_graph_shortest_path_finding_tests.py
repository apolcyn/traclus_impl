'''
Created on Feb 20, 2016

@author: Alex
'''
import unittest


class FilteredTrajectoryGraphPathFindingTest(unittest.TestCase):

    def test_compute_shortest_path(self):
        class MockPtNode:
            def __init__(self, neighbors):
                self.neighbors = neighbors


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()