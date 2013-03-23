

class AuthError (Exception):
    pass


class IdentificationFail (Exception):
    pass


class AuthorizationFail (Exception):
    pass



from lib import factory
from auth.abstract_authorization import AbstractAuthorizationm


AuthorizationFactory = factory.Factory(base=AbstractAuthorizationm)

import simple_authorization
import json_authorization

