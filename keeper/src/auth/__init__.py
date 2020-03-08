

class AuthError (Exception):
    pass


class IdentificationFail (Exception):
    pass


class AuthentificationFail (Exception):
    pass


class AuthorizationFail (Exception):
    pass



from lib import factory
from auth.abstract_authorization import AbstractAuthorization


AuthorizationFactory = factory.Factory(base=AbstractAuthorization)

import simple_authorization
import json_authorization

