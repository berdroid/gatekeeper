'''
Created on Mar 21, 2013

@author: ber
'''

from lib.dict_obj import DictObj
from auth import AuthError



class AbstractAuthorization (object):
    '''
    abstract class for identification and authorization of access to a gate
    '''

    name = '*'
    
    DEFAULTS = DictObj(

    )


    def __init__(self, params, logger):
        '''
        set up the authorization instance
        '''
        self.log = logger
        self.check_params(params)
        
        self.log.log('Authorizer %s: %s' % (self.name, self.params))
        
        self.active = True


    def check_params(self, params):
        self.params = DictObj(self.DEFAULTS)
        self.params.update(params)
        
        if None in self.params.itervalues():
            raise AuthError('Authorization type %s is missing required parameters' % (self.name,))


    def check(self, token_key, gate, event_ts):
        token, person = self.identify(token_key)
        result = self.authorize(token, person, gate, event_ts)
        return result, token, person
    
    
    def identify(self, token_key):
        raise NotImplementedError()
    
    
    def authorize(self, identity, gate, event_ts):
        raise NotImplementedError()
    
    