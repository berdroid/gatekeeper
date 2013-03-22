'''
Created on Mar 22, 2013

@author: ber
'''

from auth.abstract_authorization import AbstractAuthorizationm
from auth import AuthorizationFactory, IdentificationFail, AuthorizationFail
from lib.dict_obj import DictObj
import json



@AuthorizationFactory.register
class JsonAuthorization (AbstractAuthorizationm):
    '''
    simple authorization instance: allow all known tokens in list at all times
    '''
    
    name = 'json_file'


    DEFAULTS = DictObj(
        json_file = None,
    )
    
    
    def __init__(self, *args, **kwargs):
        '''
        set up the authorization instance
        '''
        super(JsonAuthorization, self).__init__(*args, **kwargs)


    def load_auth_data(self):
        with file(self.params.json_file, 'r') as auth_file:
            self.auth = json.load(auth_file)
            
        # token -> person
        self.persons = dict()
        
        # build index token -> person
        for person in self.auth:
            for token in person['tokens']:
                self.persons[token] = person


    def identify(self, token):
        self.load_auth_data()
        
        if token in self.persons:
            return self.persons[token]
        
        raise IdentificationFail('Could not identify person for token %s' % token)


    def authorize(self, person, gate, event_ts):
        if not gate in person['gates']:
            raise AuthorizationFail('Person %s not allowed on gate: %s' % (person['name'], gate))
        
        if not 'times' in person:
            return True
        
        raise AuthorizationFail('Person %s not allowed on gate: %s at %s' % (person['name'], gate, event_ts))

    

