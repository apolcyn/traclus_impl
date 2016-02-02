'''
Created on Jan 8, 2016

@author: Alex
'''

class MutableFloat(object):
    def __init__(self, val):
        self.set_val(val)
        
    def set_val(self, val):
        if val == None:
            raise Exception("trying to set val to None")
        self.val = val
        
    def increment(self, other):
        self.val += other
    
    def multiply(self, other):
        self.val *= other
        
    def get_val(self):
        return self.val
    
class MutableNumber(MutableFloat):
    def __init__(self, val):
        MutableFloat.__init__(self, val)
