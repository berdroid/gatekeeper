import random
import hmac
import base64



class OTP (object):
    
    CHARS = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ234567')
    
    @classmethod 
    def gen_secret(cls, bits=256):
        return ''.join(random.choice(cls.CHARS) for _ in range(bits/8))
    
    
    def __init__(self, secret, digits=6, digest='SHA1'):
        self.secret = secret,
        self.digits = digits
        self.digest = digest
        
        
    def gen_otp(self, value):
        """
        :param value: the HMAC counter value to use as the OTP value.
            Usually either the counter, or the computed integer based on the Unix timestamp
        """
        if value < 0:
            raise ValueError('value must be positive integer')
        hasher = hmac.new(self.byte_secret(), self.int_to_bytestring(value), self.digest)
        hmac_hash = bytearray(hasher.digest())
        offset = hmac_hash[-1] & 0xf
        code = ((hmac_hash[offset] & 0x7f) << 24 |
                (hmac_hash[offset + 1] & 0xff) << 16 |
                (hmac_hash[offset + 2] & 0xff) << 8 |
                (hmac_hash[offset + 3] & 0xff))
        str_code = str(code % 10 ** self.digits)
        while len(str_code) < self.digits:
            str_code = '0' + str_code

        return str_code


    def byte_secret(self):
        missing_padding = len(self.secret) % 8
        if missing_padding != 0:
            self.secret += '=' * (8 - missing_padding)
        return base64.b32decode(self.secret, casefold=True)


