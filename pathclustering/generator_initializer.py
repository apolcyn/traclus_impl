'''
Created on Jan 6, 2016

@author: Alex
'''

class GeneratorInitializer:
    '''
    classdocs
    '''
    def __init__(self, generator_func, *args):
        self.generator_func = generator_func
        self.args = args
        
    def __iter__(self):
        return self.generator_func(*self.args)
    
        