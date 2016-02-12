'''
Created on Feb 11, 2016

@author: Alex
'''
import math

def find_entropy(all_line_segs):
    def _get_neighbors(seg):
        return seg.get_num_neighbors() + 1
    
    sum_total_neighborhood_size = reduce(lambda x, y: x + y, \
                                         map(_get_neighbors, all_line_segs))
    
    def _probability_func(line_seg, sum_total_neighborhood_size):
        return _get_neighbors(line_seg) * 1.0 / sum_total_neighborhood_size
    
    def _single_entry_entropy(line_seg):
        prob_value = _probability_func(line_seg, sum_total_neighborhood_size)
        return prob_value * math.log(prob_value, 2)
    
    return -1 * reduce(lambda x, y: x + y, map(_single_entry_entropy, all_line_segs))