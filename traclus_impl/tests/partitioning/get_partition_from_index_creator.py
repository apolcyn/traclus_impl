'''
Created on Jan 9, 2016

@author: Alex
'''
import unittest
from partitioning.trajectory_partitioning import get_partition_from_index_creator


class GetPartitionFromIndexCreatorTest(unittest.TestCase):

    def test_normal_case(self):
        list = [1, 2, 3, 4, 5, 6]
        
        par_func_a = get_partition_from_index_creator(lambda a, b: a * b)
        self.assertEquals(par_func_a(list, 2, 4), 15)
        self.assertEquals(par_func_a(list, 0, 1), 2)

        par_func_b = get_partition_from_index_creator(lambda a, b: a - b)
        self.assertEquals(par_func_b(list, 3, 5), -2)
        self.assertEquals(par_func_b(list, 1, 3), -2)
        
    def test_bad_indices(self):
        func = get_partition_from_index_creator(lambda x, y: None)
        
        self.assertRaises(Exception, func, [2, 3], 1, 0)
        self.assertRaises(Exception, func, [1], 0, 1)
        self.assertRaises(Exception, func, [2, 3], 1, 1)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test']
    unittest.main()