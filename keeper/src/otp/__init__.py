import random
import hmac
import hashlib
import base64
import datetime
import time
import struct
import itertools



class OTP (object):
    
    CHARS = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ234567')
    
    @classmethod 
    def gen_secret(cls, bits=256):
        return ''.join(random.choice(cls.CHARS) for _ in range(bits/8))
    
    
    def __init__(self, secret, digits=6, digest=hashlib.sha1):
        self.secret = self._byte_secret(secret)
        self.digits = digits
        self.digest = digest


    def _cmp_otp(self, theirs, mine):
        theirs = (theirs + '#'*self.digits)[:self.digits]
        c = sum(itertools.imap(lambda a, b: a==b, theirs, mine))
        return c == self.digits


    def _hash(self, bytes):
        hasher = hmac.new(self.secret, bytes, self.digest)
        return bytearray(hasher.digest())


    def _code(self, hash):
        offset = hash[-1] & 0xf
        code = struct.unpack('>L', str(hash)[offset:offset+4])[0] & 0x7fffffff
        str_code = str(code % 10 ** self.digits)

        return str_code.rjust(self.digits, '0')


    def gen_otp(self, value):
        if value < 0:
            raise ValueError('value must be positive integer')

        hash = self._hash(self._bytes64(value))
        return self._code(hash)


    def _byte_secret(self, secret):
        missing_padding = len(secret) % 8
        if missing_padding != 0:
            secret += '=' * (8 - missing_padding)
        return base64.b32decode(secret, casefold=True)


    def _bytes64(self, i, padding=8):
        """
        Turns an integer to the OATH specified
        bytestring, which is fed to the HMAC
        along with the secret
        """
        return struct.pack('>Q', i)
    
    

class TOTP (OTP):
    
    def __init__(self, secret, digits=6, digest=hashlib.sha1, interval=30):
        super(TOTP, self).__init__(secret, digits, digest)
        self.interval = interval
        
    
    def _at(self, point_in_time, offset=0):
        if not isinstance(point_in_time, datetime.datetime):
            point_in_time = datetime.datetime.fromtimestamp(int(point_in_time))
            
        return self.gen_otp(self._timecode(point_in_time) + offset)
    
    
    def generate(self):
        return self._at(self._now())
    
    
    def verify(self, code, point_in_time=None, window=0):
        if point_in_time is None:
            point_in_time = self._now()

        if not isinstance(point_in_time, datetime.datetime):
            point_in_time = datetime.datetime.fromtimestamp(int(point_in_time))
            
        for offset in range(-window, window+1):
            if self._cmp_otp(code, self._at(point_in_time, offset)):
                return True
            
        return False


    def _now(self):
        return datetime.datetime.now()


    def _timecode(self, point_in_time):
        seconds = time.mktime(point_in_time.timetuple())
        return int(seconds / self.interval)




class COTP (TOTP):

    def __init__(self, secret, digits=16, digest=hashlib.sha256, interval=30):
        super(COTP, self).__init__(secret, digits, digest, interval)


    def _code(self, hash):
        offset = hash[-1] & 0xf
        return base64.b32encode(str(hash))[offset:offset+self.digits]



