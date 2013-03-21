'''
Created on Mar 21, 2013

@author: ber
'''
import unittest
import lib.logger
from auth.simple_authorization import SimpleAuthorization
import datetime
from auth import IdentificationFail


class Test(unittest.TestCase):

    GOOD_TOKEN = 'em4100(06-34-00-45-8e)'
    BAAD_TOKEN = 'em4100(06-34-00-47-8e)'
    
    GOOD_GATE = 'main_gate'
    BAAD_GATE = 'back_door'
    

    def setUp(self):
        self.log = lib.logger.StringIOLogger()
        auth_params = { 'tokens':(self.GOOD_TOKEN, ) }
        self.auth = SimpleAuthorization(params = auth_params, logger = self.log)


    def tearDown(self):
        del self.auth
        self.log.close()
        del self.log


    def test_accepted_token(self):
        self.assertTrue(
            self.auth.check(
                token=self.GOOD_TOKEN, 
                gate=self.GOOD_GATE, 
                event_ts=datetime.datetime.now()
            ), 
            'Failed to accept known token'
        )


    def test_unknown_token(self):
        with self.assertRaises(IdentificationFail):
            self.auth.check(
                token=self.BAAD_TOKEN,
                gate=self.GOOD_GATE, 
                event_ts=datetime.datetime.now(),
            )
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_accepted_token']
    unittest.main()