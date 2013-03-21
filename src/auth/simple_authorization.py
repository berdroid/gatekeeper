'''
Created on Mar 21, 2013

@author: ber
'''

from auth.abstract_authorization import AbstractAuthorizationm
from lib.dict_obj import DictObj
from auth import IdentificationFail, AuthorizationFail, AuthorizationFactory




class SimpleAuthorization (AbstractAuthorizationm):
    '''
    simple authorization instance: allow all known tokens in list at all times
    '''
    
    name = 'simple'


    DEFAULTS = DictObj(
        tokens = ( ),
    )
    
    
    def __init__(self, *args, **kwargs):
        '''
        set up the authorization instance
        '''
        super(SimpleAuthorization, self).__init__(*args, **kwargs)
        
        self.valid_tokens = set(self.params.tokens)
        
    
    def add_tokens(self, *tokens):
        self.valid_tokens.update(set(*tokens))
        
        
    def identify(self, token):
        if token in self.valid_tokens:
            return 'Someone'
        
        raise IdentificationFail('Could not identify person for token %s' % token)
    
    
    def authorize(self, identity, gate, event_ts):
        if identity == 'Someone':
            return True
        
        raise AuthorizationFail('Person not allowed in : %s' % identity)
    
    
AuthorizationFactory.register(SimpleAuthorization)


    
    