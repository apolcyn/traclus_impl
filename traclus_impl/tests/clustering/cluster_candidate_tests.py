'''
Created on Feb 10, 2016

@author: Alex
'''
import unittest
from traclus_impl.generic_dbscan import ClusterCandidate, ClusterCandidateIndex
from traclus_impl.mutable_float import MutableFloat

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
        index = ClusterCandidateIndex([1, 2, 3, 4, 5], epsilon=0)
        candidate.distance_to_candidate = mock_dist_to_other_candidate_func
        index.find_neighbors_of(cluster_candidate=candidate)
        self.assertEquals(counter.get_val(), 5)        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_calls_dist_to_other_candidate_when_finding_candidates']
    unittest.main()