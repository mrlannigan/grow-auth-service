from flask import Response
from json import dumps

class User(object):
    """Authorized user object"""
    def __init__(self, email=None, email_verified=None, name=None, picture=None, given_name=None, family_name=None, locale=None, **kwargs):
        super(User, self).__init__()
        self.email=email
        self.email_verified=bool(email_verified)
        self.name=name
        self.picture=picture
        self.given_name=given_name
        self.family_name=family_name
        self.locale=locale or 'en'

    def toDict(self):
        return dict({
            'email': self.email,
            'email_verified': self.email_verified,
            'name': self.name,
            'picture': self.picture,
            'given_name': self.given_name,
            'family_name': self.family_name,
            'locale': self.locale
        })

    def __str__(self):
        return dumps(self.toDict())

    def response(self):
        return Response(response=str(self), mimetype='application/json')
