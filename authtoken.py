from redis import Redis
from pool import pool
import json
import binascii
import os

DEFAULT_TTL = 60 * 60 * 12 # 12 hours
TOKEN_LENGTH = 32

class AuthToken(object):
    """Representation of a token"""

    def __init__(self, token=None, key_prefix='v1', ttl=None):
        super(AuthToken, self).__init__()
        self.token = token
        self.key_prefix = key_prefix
        self.ttl = ttl or DEFAULT_TTL
        self.redis = Redis(connection_pool=pool)

    def verify(self):
        """Verify a defined token and return it's data"""
        data = self.redis.get(name=self.build())

        if data:
            data = json.loads(data)

        return data

    def generate(self):
        """Generate a new token"""
        self.token = binascii.hexlify(os.urandom(TOKEN_LENGTH))
        return self.token

    def build(self):
        """Formats a token for database"""
        return '{prefix}-{token}'.format(prefix=self.key_prefix, token=self.token)

    def save(self, data):
        """Save token to database"""
        if not self.token:
            raise AuthTokenException('No token given')

        if not data:
            raise AuthTokenException('No data given')

        return self.redis.setex(name=self.build(), value=json.dumps(data), time=self.ttl)

    def __str__(self):
        return self.token


class AuthTokenException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
