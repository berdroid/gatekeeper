

import otp


if __name__ == '__main__':
    
    secret = otp.OTP.gen_secret()
    print(secret)