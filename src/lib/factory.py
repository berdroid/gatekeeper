'''
Created on Mar 17, 2013

@author: ber
'''

class Factory (object):
    '''
    A factory to instantiate items
    '''


    def __init__(self, base=object):
        '''
        Instantiate the factory
        '''
        self.base = base
        self.items = { }
        
        
        
    def register(self, item):
        '''
        register an item class
        '''
        if not issubclass(item, self.base):
            raise TypeError('%s will only register sub classes of %s' % (self.__class__, self.base))
        
        self.items[item.name] = item
        return item
        
        
    
    def __call__(self, name, *args, **kwargs):
        """
        instantiate an item with a given name and pass args
        """
        return self.items[name](*args, **kwargs)