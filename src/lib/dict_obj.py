'''
Created on Mar 18, 2013

@author: ber
'''

class DictObj (dict):
    '''
    a dictionary allowing access via attributes
    '''


    def __init__(self, *args, **kwargs):
        '''
        initialize
        '''
        super(DictObj, self).__init__(*args, **kwargs)
        
        
    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError('Attribute not found as key in dict: %s' % name)
        
