'''
Created on Jan 19, 2016

@author: Alex
'''
import unittest
from traclus_impl.geometry import Point
from deer_file_reader import read_test_file
import os

class Test(unittest.TestCase):

    def test_reads_file(self):
        expected = [[Point(1, 2), Point(3, 4)], \
                    [Point(2, 4), Point(6, 8)], \
                    [Point(1, 3), Point(5, 7)], \
                    [Point(9, 8)]]
        res = read_test_file(os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                             "dummy_input.txt"))
        exp_iter = iter(expected)
        for traj in res:
            exp_line = exp_iter.next()
            self.assertListEqual(exp_line, traj)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_reads_file']
    unittest.main()