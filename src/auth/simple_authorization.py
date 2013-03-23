'''
Created on Mar 21, 2013

@author: ber
'''

from auth.abstract_authorization import AbstractAuthorizationm
from lib.dict_obj import DictObj
from auth import IdentificationFail, AuthorizationFail, AuthorizationFactory



@AuthorizationFactory.register
class SimpleAuthorization (AbstractAuthorizationm):
    '''
    simple authorization instance: allow all known tokens in list at all times
    '''
    
    name = 'simple'


    DEFAULTS = DictObj(
        tokens = ( ),
        gates = ( ),
    )
    
    
    def __init__(self, *args, **kwargs):
        '''
        set up the authorization instance
        '''
        super(SimpleAuthorization, self).__init__(*args, **kwargs)
        
        self.valid_tokens = set(self.params.tokens)
        self.valid_gates = set(self.params.gates)
        print self.valid_tokens
        
    
    def add_tokens(self, *tokens):
        self.valid_tokens.update(set(tokens))
        
        
    def identify(self, token_key):
        if token_key in self.valid_tokens:
            token = DictObj(name='token_name', kind=token_key[0], id=token_key[1], blocked=False)
            person = DictObj(name='Someone', blocked=False)
            return token, person
        
        raise IdentificationFail('Could not identify person for token %s' % str(token_key))
    
    
    def authorize(self, token, person, gate, event_ts):
        if not person.blocked:
            if not self.valid_gates:
                return True
            elif gate in self.valid_gates:
                return True
        
        raise AuthorizationFail('Person not allowed in : %s' % person)

    
    