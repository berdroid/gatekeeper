'''
Created on Mar 17, 2013

@author: ber
'''

class Factory (object):
    '''
    A factory to instantiate items
    '''


    def __init__(self):
        '''
        Instantiate the factory
        '''
        self.items = { }
        
        
        
    def register(self, item):
        '''
        register an item class
        '''
        self.items[item.name] = item
        return item
        
        
    
    def __call__(self, name, *args, **kwargs):
        """
        instantiate an item with a given name and pass args
        """
        return self.items[name](*args, **kwargs)