

import otp
import json
import sys
import requests
from StringIO import StringIO


if __name__ == '__main__':
    
    template_name = sys.argv[1]
    
    secret = otp.OTP.gen_secret()
    
    data = json.load(file(template_name), encoding='utf-8')
    data['TOTP']['secret'] = secret
    
    config_string = json.dumps(data, ensure_ascii=False, encoding='utf-8')
    
    files = {
        'file': (template_name, StringIO(config_string), 'application/octet-stream'),
    }
    
    headers = {
    }
    
    r = requests.post('https://file.io/?expires=1d', files=files, headers=headers)    
    
    if r.status_code == requests.codes.ok:
        resp = r.json()
        
        if resp['success']:
            print('Download code: {key}'.format(**resp))
            print('Token: {{ "name": "", "kind": "totp", "id": "{}", "blocked": false, "person_id": 0 }},'.format(secret))
            sys.exit(0)
            
    print(r.text)
    sys.exit(1)
    
    