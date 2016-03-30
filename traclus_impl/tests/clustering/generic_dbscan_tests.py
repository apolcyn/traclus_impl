'''
Created on Dec 30, 2015

@author: Alex
'''
import unittest
from traclus_impl.geometry import Point
from traclus_impl.generic_dbscan import ClusterCandidate, ClusterFactory, dbscan, ClusterCandidateIndex

class TestPoint(ClusterCandidate):
    def __init__(self, x, y):
        ClusterCandidate.__init__(self)
        self.point = Point(x, y)
        
    def distance_to_candidate(self, other_candidate):
        return self.point.distance_to(other_candidate.point)       

class DbScanTest(unittest.TestCase):
    
    def build_test_object(self, points, num_clusters, epsilon, min_neighbors):
        expected_clusters = [[] for i in xrange(0, num_clusters)]
        expected_noise = []
        test_points = map(lambda p: TestPoint(p[0], p[1]), points)
        
        for i in xrange(0, len(points)):
            if len(points[i]) > 2:
                expected_clusters[points[i][2]].append(test_points[i])
            else:
                expected_noise.append(test_points[i])

        return {'test_index': ClusterCandidateIndex(test_points, epsilon), 'expected_clusters': \
                expected_clusters, 'expected_noise': expected_noise, \
                'min_neighbors': min_neighbors}

    def setUp(self):
        self.test_cases = []
        test_ob = self.build_test_object([(0, 0)], 0, 0, 1)
        self.test_cases.append(test_ob)
        
        test_ob = self.build_test_object([(0, 0, 0)], 1, 1.0, 0)
        self.test_cases.append(test_ob)
        
        test_ob = self.build_test_object([(0, 0, 0), (0, 2, 1)], 2, 1.0, 0)
        self.test_cases.append(test_ob)
        
        test_ob = self.build_test_object([(0, 0, 0), (1, 0, 0), (2, 0, 0), (0, 1, 0), (1, 1, 0), (2, 1, 0)], 1, 1.0, 2)
        self.test_cases.append(test_ob)
        
        test_ob = self.build_test_object([(0, 0, 0), (1, 0, 0), (2, 0, 0), (0, 1, 0), (1, 1, 0), (2, 1, 0)], 1, 1.0, 3)
        self.test_cases.append(test_ob)
        
        test_ob = self.build_test_object([(0, 0, 0), (1, 0, 0), (2, 0, 0), (0, 1, 0), (1, 1, 0), (2, 1, 0)], 1, 1.0, 3)
        self.test_cases.append(test_ob)
        
        test_ob = self.build_test_object([(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1)], 0, 1.0, 4)
        self.test_cases.append(test_ob)
        
        test_ob = self.build_test_object([(0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0), \
                                          (4, 0, 1), (5, 0, 1), (4, 1, 1), (5, 1, 1)], 2, 1.0, 2)
        self.test_cases.append(test_ob)
        
        test_ob = self.build_test_object([(0, 0), (1, 0), (0, 1), (1, 1), \
                                          (4, 0), (5, 0), (4, 1), (5, 1)], 0, 1.0, 3)
        self.test_cases.append(test_ob)
        
        test_ob = self.build_test_object([(0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0), \
                                          (4, 0, 0), (5, 0, 0), (4, 1, 0), (5, 1, 0)], 1, 3.0, 3)
        self.test_cases.append(test_ob)
        
        test_ob = self.build_test_object([(2, 0, 0), (0, 1, 0), (1, 1, 0), (2, 1, 0), (3, 1, 0), \
                                          (0, 2, 0), (1, 2, 0)], 1, 1.0, 2)
        self.test_cases.append(test_ob)
        
        test_ob = self.build_test_object([(2, 0, 0), (0, 1, 0), (1, 1, 0), (2, 1, 0), (3, 1, 0), \
                                          (0, 2), (1, 2, 0)], 1, 1.0, 3)
        self.test_cases.append(test_ob)
        
    def lists_equivalent(self, a, b):
        set_a = set(a)
        set_b = set(b)
        
        if len(set_a) != len(a):
            raise Exception("list contains duplicates")
        
        if set_a.issubset(set_b) and set_b.issubset(set_a):
            return True
        else:
            return False
        
    def find_single_matching_cluster(self, expected_list, cluster_list):
        count = 0
        for other in cluster_list:
            if self.lists_equivalent(other.members, expected_list):
                count += 1    
        if count == 1:
            return True
        else:
            return False

    def test_dbscan(self):
        cluster_factory = ClusterFactory()
        for test_ob in self.test_cases:
            clusters = dbscan(test_ob['test_index'], \
                   test_ob['min_neighbors'], cluster_factory)
            for expected in test_ob['expected_clusters']:
                self.assertTrue(self.find_single_matching_cluster(expected, clusters), \
                                "couldn't find matching cluster in " + str(test_ob) + \
                                " in clusters: " + str(clusters))
            for point in test_ob['test_index'].candidates:
                self.assertTrue(point.is_classified())
            for point in test_ob['expected_noise']:
                self.assertTrue(point.is_noise())
            for single_cluster in clusters:
                for point in single_cluster.members:
                    self.assertEqual(single_cluster, point.cluster)
                    self.assertFalse(point.is_noise())

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()