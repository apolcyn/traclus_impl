'''
Created on Dec 29, 2015

@author: Alex
'''
import math
    
def determine_longer_and_shorter_lines(line_a, line_b):
    if line_a.length < line_b.length:
        return (line_b, line_a)
    else:
        return (line_a, line_b)
    
    
def get_total_distance_function(perp_dist_func, angle_dist_func, parrallel_dist_func):
    def __dist_func(line_a, line_b, perp_func=perp_dist_func, angle_func=angle_dist_func, \
                    parr_func=parrallel_dist_func):
        return perp_func(line_a, line_b) + angle_func(line_a, line_b) + \
            parr_func(line_a, line_b)
    return __dist_func

def perpendicular_distance(line_a, line_b):
    longer_line, shorter_line = determine_longer_and_shorter_lines(line_a, line_b)
    dist_a = shorter_line.start.distance_to_projection_on(longer_line)
    dist_b = shorter_line.end.distance_to_projection_on(longer_line)
    
    if dist_a == 0.0 and dist_b == 0.0:
        return 0.0
    
    return (dist_a * dist_a + dist_b * dist_b) / (dist_a + dist_b)
    
def __perpendicular_distance(line_a, line_b):
    longer_line, shorter_line = determine_longer_and_shorter_lines(line_a, line_b)
    dist_a = longer_line.line.project(shorter_line.start).distance_to(shorter_line.start)
    dist_b = longer_line.line.project(shorter_line.end).distance_to(shorter_line.end)
    
    if dist_a == 0.0 and dist_b == 0.0:
        return 0.0
    else:
        return (math.pow(dist_a, 2) + math.pow(dist_b, 2)) / (dist_a + dist_b)

def angular_distance(line_a, line_b):
    longer_line, shorter_line = determine_longer_and_shorter_lines(line_a, line_b)
    sine_coefficient = shorter_line.sine_of_angle_with(longer_line)
    return abs(sine_coefficient * shorter_line.length)

#def __parrallel_distance(line_a, line_b):

def parrallel_distance(line_a, line_b):
    longer_line, shorter_line = determine_longer_and_shorter_lines(line_a, line_b)
    def __func(shorter_line_pt, longer_line_pt):
        return shorter_line_pt.distance_from_point_to_projection_on_line_seg(longer_line_pt, \
                                                                             longer_line)
    return min([longer_line.dist_from_start_to_projection_of(shorter_line.start), \
               longer_line.dist_from_start_to_projection_of(shorter_line.end), \
               longer_line.dist_from_end_to_projection_of(shorter_line.start), \
               longer_line.dist_from_end_to_projection_of(shorter_line.end)])
    
def dist_to_projection_point(line, proj):
    return min(proj.distance_to(line.start), proj.distance_to(line.end))