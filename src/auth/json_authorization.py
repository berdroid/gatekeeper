'''
Created on Mar 22, 2013

@author: ber
'''

from auth.abstract_authorization import AbstractAuthorizationm
from auth import AuthorizationFactory, IdentificationFail, AuthorizationFail
from lib.dict_obj import DictObj
import json
import datetime
import time



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
        
        
    def token_key(self, token):
        return token.kind, token.id


    def load_auth_data(self):
        with file(self.params.json_file, 'r') as auth_file:
            self.auth = json.load(auth_file, object_hook=DictObj)
            
        # token -> person
        self.tokens = dict()
        
        # build index token -> person
        for person in self.auth:
            for token in person.tokens:
                token.person = person
                self.tokens[self.token_key(token)] = token
                
                
    def check_time(self, time_spec, ts):
        if not ts.isoweekday() in time_spec.weekdays:
            return False
        
        begin = datetime.datetime.strptime(time_spec.begin, '%H:%M').time()
        end = datetime.datetime.strptime(time_spec.end, '%H:%M').time()
        
        if begin <= ts.time() <= end:
            return True
        
        return False


    def identify(self, token_key):
        self.load_auth_data()
        
        if token_key in self.tokens:
            return self.tokens[token_key]
        
        raise IdentificationFail('Could not identify person for token %s' % str(token_key))


    def authorize(self, token, gate, event_ts):
        person = token.person
        
        if person.blocked:
            raise AuthorizationFail('Person %s blocked' % (person.name,))
        
        if token.blocked:
            raise AuthorizationFail('Token %s blocked' % (token.name,))
        
        if not gate in person['gates']:
            raise AuthorizationFail('Person %s not allowed on gate: %s' % (person.name, gate))
        
        if not 'times' in person:
            return True
        
        for time  in person.times:
            if self.check_time(time, event_ts):
                return True
        
        raise AuthorizationFail('Person %s not allowed on gate: %s at %s' % (person['name'], gate, event_ts))

    

