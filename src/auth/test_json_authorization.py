'''
Created on Mar 22, 2013

@author: ber
'''
import unittest
import lib.logger
from auth.json_authorization import JsonAuthorization
import datetime
from auth import IdentificationFail, AuthorizationFail
import tempfile


class Test(unittest.TestCase):

    GOOD_TOKEN = 'em4100(06-34-00-45-8e)'
    GOOD_NAME  = 'Bernhard'
    BAAD_TOKEN = 'em4100(06-34-00-47-8e)'
    
    GOOD_GATE = 'main_gate'
    BAAD_GATE = 'back_door'
    
    AUTH_FILE = """
    [
        {
            "name": "%(GOOD_NAME)s",
            "gates": [ "%(GOOD_GATE)s" ],
            "tokens": [ "%(GOOD_TOKEN)s", "ghi-012"]
        }
    ]
    """ % dict(
        GOOD_NAME=GOOD_NAME,
        GOOD_GATE=GOOD_GATE,
        GOOD_TOKEN=GOOD_TOKEN
    )
    

    def setUp(self):
        self.log = lib.logger.StringIOLogger()
        self.fd, self.file_name = tempfile.mkstemp()
        self.write_auth(self.AUTH_FILE)
        auth_params = { 'json_file':self.file_name }
        self.auth = JsonAuthorization(params = auth_params, logger = self.log)


    def tearDown(self):
        del self.auth
        self.log.close()
        del self.log
        
        
    def write_auth(self, auth):
        with file(self.file_name, 'w') as f:
            f.write(auth)


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
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()