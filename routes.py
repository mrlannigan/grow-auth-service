from app import app
from errors import (Unauthorized, BadRequest, APIError)
from authtoken import AuthToken
from flask import (jsonify, request, Response)
import json
from user import User
import urllib2

@app.route('/v1/auth/token/<reqToken>')
def getToken(reqToken):
    if not reqToken:
        raise BadRequest('Invalid token')

    token = AuthToken(token=reqToken)

    data = token.verify()

    if not data:
        raise Unauthorized('No valid token')

    user = User(**data)

    return user.response()

@app.route('/v1/auth', methods=['POST'])
def createAuthentication():
    if not request.headers['Content-Type'] == 'application/json':
        raise BadRequest('Invalid request body, must be application/json')

    try:
        data = request.get_json()
    except Exception as e:
        raise BadRequest('Invalid json body: {0}'.format(e))

    if not data['google_id_token']:
        raise BadRequest('Missing google_id_token from body')

    idToken = data['google_id_token']

    try:
        gopen = urllib2.urlopen('https://www.googleapis.com/oauth2/v3/tokeninfo?id_token={0}'.format(idToken))
    except urllib2.URLError as e:
        etype = APIError
        if e.code == 400:
            etype = Unauthorized
        raise etype(message='Google verification failed: {} {}'.format(e.code, e.reason))

    try:
        gres = json.loads(gopen.read())
    except Exception as e:
        raise APIError(message='Google verification failed: {}'.format(e.message))

    user = User(**gres)

    token = AuthToken()
    token.generate()

    resp = user.toDict()

    token.save(data=resp)

    resp['access_token'] = str(token)

    return Response(response=json.dumps(resp), content_type='application/json')
