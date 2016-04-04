'''
Created on Apr 3, 2016

@author: alexpolcyn
'''
import unittest
import os
import json
from traclus_impl.geometry import Point
from traclus_impl.trajectory_partitioning import call_partition_trajectory

class TestHairyPartitioning(unittest.TestCase):
    FILENAME = os.path.join(os.path.dirname(os.path.realpath(__file__)), "hairy_partitioning.txt")

    def test_doesnt_blow_up(self):
        traj = None
        with open(TestHairyPartitioning.FILENAME, 'r') as input:
            dict = json.loads(input.read())
            traj = map(lambda p: Point(**p), dict)
            
        call_partition_trajectory(traj)
            


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()