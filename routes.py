from app import app
from errors import (Unauthorized, BadRequest)
from authtoken import AuthToken
from flask import (jsonify, request)
from user import User

@app.route('/v1/auth/token')
def getToken():
    reqToken = request.args.get('token')

    if not reqToken:
        raise BadRequest('Invalid token')

    token = AuthToken(token=reqToken)

    data = token.verify()

    if not data:
        raise Unauthorized('No valid token')

    user = User(**data)

    return user.response()
