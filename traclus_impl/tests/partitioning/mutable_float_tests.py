'''
Created on Jan 8, 2016

@author: Alex
'''
import unittest

from traclus_impl.mutable_float import MutableFloat


class MutableFloatTest(unittest.TestCase):

    def test_all(self):
        num = MutableFloat(1.0)
        num.increment(3)
        num.increment(5)
        num.multiply(2)
        num.multiply(2)
        self.assertEquals(36, num.get_val())
        
    def test_bad_val(self):
        self.assertRaises(Exception, MutableFloat, None)
        m_float = MutableFloat(0)
        self.assertRaises(Exception, m_float.set_val, None)
        
    def test_closurability(self):
        num = MutableFloat(1.0)
        def add(other):
            num.increment(other)
            
        add(2.0)
        add(3.0)
        add(10)
        self.assertEquals(16, num.get_val())

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()