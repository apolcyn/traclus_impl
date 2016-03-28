'''
Created on Jan 20, 2016

@author: Alex
'''

from traclus_impl.coordination import the_whole_enchilada
from deer_file_reader import read_test_file
import os
import cProfile

""" This is useful for profiling performance on the datasets in tehi directory"""
def run_deer_stuff():
    file = os.path.dirname(__file__) + "\\deer_1995.tra"
    points = read_test_file(file)
    traj_res = the_whole_enchilada(point_iterable_list=points, epsilon=40, min_neighbors=7, \
                                   min_num_trajectories_in_cluster=2, min_vertical_lines=7, min_prev_dist=0.0)
    print "heres the output: " + str(traj_res)
    print "about to print out the lines"
    for traj in traj_res:
        print "A new average trajectory:"
        for point in traj:
            print "    x: " + str(point.x) + ", y: " + str(point.y)
    print "done"

if __name__ == '__main__':
    cProfile.run('run_deer_stuff()')
                