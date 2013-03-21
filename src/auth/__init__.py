

class AuthError (Exception):
    pass


class IdentificationFail (Exception):
    pass


class AuthorizationFail (Exception):
    pass



from lib import factory


AuthorizationFactory = factory.Factory()

import simple_authorization
