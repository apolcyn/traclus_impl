'''
Created on Mar 23, 2016

@author: Alex
'''
import math

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def distance_to(self, other_point):
        diff_x = other_point.x - self.x
        diff_y = other_point.y - self.y
        return math.sqrt(math.pow(diff_x, 2) + math.pow(diff_y, 2))
    
    def dot_product_with(self, other_point):
        return self.x * other_point.x + self.y * other_point.y
    
    def distance_from_point_to_projection_on_line_seg(self, point, line_segment):
        dot_product = (self.x - line_segment.start.x) * line_segment.unit_vector.x + \
        (self.y - line_segment.start.y) * line_segment.unit_vector.y
        
        proj_x = dot_product * line_segment.unit_vector.x + line_segment.start.x
        proj_y = dot_product * line_segment.unit_vector.y + line_segment.start.y
        
        return math.sqrt(math.pow(point.x - proj_x, 2) + \
                         math.pow(point.y - proj_y, 2))
    
    def distance_to_projection_on(self, line_segment):
        return self.distance_from_point_to_projection_on_line_seg(self, line_segment)
        
        
class LineSegment(object):
    @staticmethod
    def from_tuples(start, end):
        return LineSegment(Point(start[0], start[1]), Point(end[0], end[1]))
    
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.length = start.distance_to(end)
        
        unit_x = (end.x - start.x) / self.length
        unit_y = (end.y - start.y) / self.length
        self.unit_vector = Point(unit_x, unit_y)
        
    def sine_of_angle_with(self, other_line_segment):
        return self.unit_vector.x * other_line_segment.unit_vector.y - \
        self.unit_vector.y * other_line_segment.unit_vector.x
                
    