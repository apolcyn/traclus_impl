'''
Created on Jan 20, 2016

@author: Alex
'''

from traclus_impl.coordination import run_traclus
from deer_file_reader import read_test_file
import os
import cProfile

""" This is useful for profiling performance on the datasets in this directory"""
def run_deer_stuff():
    file = os.path.join(os.path.dirname(__file__), "elk_1993.tra")
    points = read_test_file(file)
    traj_res = run_traclus(point_iterable_list=points, epsilon=32, min_neighbors=7, \
                                   min_num_trajectories_in_cluster=2, min_vertical_lines=7, min_prev_dist=0.0)
    print "heres the output: " + str(traj_res)
    print "about to print out the lines"
    for traj in traj_res:
        print "A new average trajectory:"
        for point in traj:
            print str(point)
    print "done"

if __name__ == '__main__':
    cProfile.run('run_deer_stuff()')
                