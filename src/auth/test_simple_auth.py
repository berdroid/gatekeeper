'''
Created on Mar 21, 2013

@author: ber
'''
import unittest
import lib.logger
from auth.simple_authorization import SimpleAuthorization
import datetime
from auth import IdentificationFail, AuthorizationFail


class Test(unittest.TestCase):

    KIND = 'em4100'
    GOOD_TOKEN = '06-34-00-45-8e'
    BAAD_TOKEN = '06-34-00-47-8e'
    
    GOOD_GATE = 'main_gate'
    BAAD_GATE = 'back_door'
    

    def setUp(self):
        self.log = lib.logger.StringIOLogger()
        auth_params = { 'tokens':((self.KIND, self.GOOD_TOKEN),), 'gates':(self.GOOD_GATE,) }
        self.auth = SimpleAuthorization(params = auth_params, logger = self.log)


    def tearDown(self):
        del self.auth
        self.log.close()
        del self.log


    def test_accepted_token(self):
        self.assertTrue(
            self.auth.check(
                token=(self.KIND, self.GOOD_TOKEN), 
                gate=self.GOOD_GATE, 
                event_ts=datetime.datetime.now()
            ), 
            'Failed to accept known token'
        )


    def test_unknown_token(self):
        with self.assertRaises(IdentificationFail):
            self.auth.check(
                token=(self.KIND, self.BAAD_TOKEN), 
                gate=self.GOOD_GATE, 
                event_ts=datetime.datetime.now(),
            )


    def test_add_token(self):
        with self.assertRaises(IdentificationFail):
            self.auth.check(
                token=(self.KIND, self.BAAD_TOKEN), 
                gate=self.GOOD_GATE, 
                event_ts=datetime.datetime.now(),
            )

        self.auth.add_tokens((self.KIND, self.BAAD_TOKEN))
        
        self.assertTrue(
            self.auth.check(
                token=(self.KIND, self.BAAD_TOKEN), 
                gate=self.GOOD_GATE, 
                event_ts=datetime.datetime.now()
            ), 
            'Failed to accept added token'
        )


    def test_bad_gate(self):
        with self.assertRaises(AuthorizationFail):
            self.auth.check(
                token=(self.KIND, self.GOOD_TOKEN), 
                gate=self.BAAD_GATE, 
                event_ts=datetime.datetime.now(),
            )
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_accepted_token']
    unittest.main()