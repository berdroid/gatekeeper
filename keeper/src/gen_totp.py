
import otp
import sys
import datetime


if __name__ == '__main__':
    
    secret = sys.argv[1]
    
    totp = otp.TOTP(secret)
    
    print(totp._timecode(totp._now()), totp._now().isoformat())
    print(totp.generate())


    cotp = otp.COTP(secret)
    print(cotp.generate())
    
    
    if len(sys.argv) > 2:
        res = totp.verify(sys.argv[2], window=2)
        print('TOTP:', res)
        
        res = cotp.verify(sys.argv[2], window=2)
        print('COTP:', res)
        
    