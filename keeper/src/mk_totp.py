

import otp
import json
import sys
import requests
from StringIO import StringIO


if __name__ == '__main__':
    TEMPLATE = 'Token: {{ "name": "{name}", "kind": "{kind}", "id": "{id}", "secret": "{secret}", "blocked": false, "person_id": 0 }},'
    
    template_name = sys.argv[1]
    
    secret = otp.OTP.gen_secret()
    id = otp.OTP.gen_secret()[:6]
    
    data = json.load(file(template_name), encoding='utf-8')
    
    try:
        data['TOTP']['secret'] = secret
        data['TOTP']['id'] = id
        kind = 'TOTP'
    except KeyError:
        data['COTP']['secret'] = secret
        data['COTP']['id'] = id
        kind = 'COTP'
    
    config_string = json.dumps(data, ensure_ascii=False, encoding='utf-8')
    print(config_string)
    
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
            print(TEMPLATE.format(name=id, id=id, secret=secret, kind=kind))
            sys.exit(0)
            
    print(r.text)
    sys.exit(1)
    
    