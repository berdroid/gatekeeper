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
import os


class Test(unittest.TestCase):

    GOOD_NAME  = 'Bernhard'

    KIND = 'em4100'
    GOOD_TOKEN = '06-34-00-45-8e'
    BAAD_TOKEN = '06-34-00-47-8e'
    
    GOOD_GATE = 'main_gate'
    BAAD_GATE = 'back_door'
    
    AUTH_FILE = """
    {
        "persons": [
            {
                "id": 1,
                "name": "Bernhard",
                "blocked": false,
                "gates": [ "%(GOOD_GATE)s" ]
            },
            {
                "id": 2,
                "name": "Emil",
                "blocked": false,
                "gates": [ "%(GOOD_GATE)s" ],
                "times": [
                    { "weekdays": [ 1, 2, 3, 4, 5 ], "begin": "09:00", "end": "12:00" },
                    { "weekdays": [ 1, 2, 3, 4, 5 ], "begin": "13:00", "end": "17:00" },
                    { "weekdays": [ 6, 7 ], "begin": "09:15", "end": "10:00" }
                ]
            },
            {
                "id": 3,
                "name": "Emilly",
                "blocked": true,
                "gates": [ "%(GOOD_GATE)s" ]
            }
        ],
        "tokens": [
            { "name": "101", "kind": "em4100", "id": "06-34-00-45-8e", "blocked": false, "person_id": 1 },
            { "name": "102", "kind": "em4100", "id": "ghi-012",        "blocked": true, "person_id": 1 },
            { "name": "103", "kind": "em4100", "id": "TokenEmil1",     "blocked": false, "person_id": 2 },
            { "name": "104", "kind": "em4100", "id": "ghi-932",        "blocked": false, "person_id": 2 },
            { "name": "103", "kind": "em4100", "id": "TokenEmilly1",   "blocked": false, "person_id": 3 },
            { "name": "104", "kind": "em4100", "id": "strange",        "blocked": true, "person_id": null }
        ]
    }
    """ % dict(
        GOOD_NAME=GOOD_NAME,
        GOOD_GATE=GOOD_GATE,
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
        os.close(self.fd)
        os.remove(self.file_name)
        self.fd = None
        self.file_name = None
        
        
    def write_auth(self, auth):
        with file(self.file_name, 'w') as f:
            f.write(auth)
            
            
    def make_ts(self, weekday, hours, minutes):
        d = datetime.date(2013, 3, 3) + datetime.timedelta(days=weekday)
        t = datetime.time(hours, minutes)
        return datetime.datetime.combine(d, t)


    def test_accepted_token(self):
        self.assertTrue(
            self.auth.check(
                token=(self.KIND, self.GOOD_TOKEN), 
                gate=self.GOOD_GATE, 
                event_ts=datetime.datetime.now()
            ), 
            'Failed to accept known token'
        )


    def test_blocked_token(self):
        with self.assertRaises(AuthorizationFail):
            self.auth.check(
                token=(self.KIND, 'ghi-012'),
                gate=self.GOOD_GATE, 
                event_ts=datetime.datetime.now(),
            )


    def test_blocked_token2(self):
        with self.assertRaises(IdentificationFail):
            self.auth.check(
                token=(self.KIND, 'strange'),
                gate=self.GOOD_GATE, 
                event_ts=datetime.datetime.now(),
            )


    def test_unknown_token(self):
        with self.assertRaises(IdentificationFail):
            self.auth.check(
                token=(self.KIND, self.BAAD_TOKEN),
                gate=self.GOOD_GATE, 
                event_ts=datetime.datetime.now(),
            )


    def test_bad_gate(self):
        with self.assertRaises(AuthorizationFail):
            self.auth.check(
                token=(self.KIND, self.GOOD_TOKEN),
                gate=self.BAAD_GATE, 
                event_ts=datetime.datetime.now(),
            )
            

    def test_good_time1(self):
        self.assertTrue(
            self.auth.check(
                token=(self.KIND, 'TokenEmil1'),
                gate=self.GOOD_GATE, 
                event_ts=self.make_ts(1, 10, 22)
            ), 
        )
            

    def test_bad_time1(self):
        with self.assertRaises(AuthorizationFail):
            self.auth.check(
                token=(self.KIND, 'TokenEmil1'),
                gate=self.GOOD_GATE, 
                event_ts=self.make_ts(6, 10, 22)
            ) 
            

    def test_good_time2(self):
        self.assertTrue(
            self.auth.check(
                token=(self.KIND, 'TokenEmil1'),
                gate=self.GOOD_GATE, 
                event_ts=self.make_ts(1, 17, 0)
            ), 
        )
            

    def test_bad_time2(self):
        with self.assertRaises(AuthorizationFail):
            self.auth.check(
                token=(self.KIND, 'TokenEmil1'),
                gate=self.GOOD_GATE, 
                event_ts=self.make_ts(1, 17, 1)
            )
            

    def test_good_time3(self):
        self.assertTrue(
            self.auth.check(
                token=(self.KIND, 'TokenEmil1'),
                gate=self.GOOD_GATE, 
                event_ts=self.make_ts(1, 9, 15)
            ), 
        )
            

    def test_bad_time3(self):
        self.assertTrue(
            self.auth.check(
                token=(self.KIND, 'TokenEmil1'),
                gate=self.GOOD_GATE, 
                event_ts=self.make_ts(1, 9, 14)
            ), 
        )
            

    def test_blocked_person(self):
        with self.assertRaises(AuthorizationFail):
            self.auth.check(
                token=(self.KIND, 'TokenEmilly1'),
                gate=self.GOOD_GATE, 
                event_ts=self.make_ts(1, 17, 1)
            )
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()