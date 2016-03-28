'''
Created on Jan 19, 2016

@author: Alex
'''
from traclus_impl.geometry import Point

def read_test_file(file_name):
    file = open(file_name)
    num_dimensions = int(file.next())
    if num_dimensions != 2:
        raise Exception("didn't make this for this")
    num_traj = int(file.next())
    
    exp_id = 0
    all_traj = []
    for line in file:
        tokens = line.split()
        id = int(tokens[0])
        num_points = int(tokens[1])
        if id != exp_id:
            raise Exception("something wrong")
        traj = []
        for i in filter(lambda x: x % 2 == 0, xrange(0, num_points)):
            x = float(tokens[i + 2])
            try:
                y = float(tokens[i + 3])
            except IndexError:
                print "error on index " + str(i) + " with id " + str(id)
            traj.append(Point(x, y))
        all_traj.append(traj)
        exp_id += 1
    file.close()
    return all_traj