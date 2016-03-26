'''
Created on Feb 10, 2016

@author: Alex
'''
import unittest
from generic_dbscan import ClusterCandidate
from mutable_float import MutableFloat

class Test(unittest.TestCase):
    
    def mock_dist_to_other_candidate_func(self, other_candidate, mutable_number):
        mutable_number.increment()
        return 0

    def test_calls_dist_to_other_candidate_when_finding_candidates(self):
        counter = MutableFloat(0)
        
        def mock_dist_to_other_candidate_func(other_candidate):
            counter.increment(1)
            return 0
       
        candidate = ClusterCandidate()
        candidate.distance_to_candidate = mock_dist_to_other_candidate_func
        candidate.find_neighbors([1, 2, 3, 4, 5], epsilon=0)
        self.assertEquals(counter.get_val(), 5)        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_calls_dist_to_other_candidate_when_finding_candidates']
    unittest.main()