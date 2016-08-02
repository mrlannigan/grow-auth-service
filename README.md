# grow-auth-service

### Authentication Service API

Not accessible to the public

#### POST /v1/auth

Validates token with Google's token validation service and if it is valid, we then create an access_token the web application will use to create a connection to the Chat Service.

##### Body
* google_id_token - string

##### 200 Response
* access_token - string
* email - string
* email_verified - boolean
* name - string
* picture - string
* given_name - string
* family_name - string
* locale - string

##### 401 Unauthorized
* statusCode = 401
* error = 'Unauthorized'
* message - string

#### GET /v1/auth/token/<reqToken>

Used by Chat service to verify an access_token's validity. Will also return user's information that was gathered during authentication.

##### Path
* access_token - string

##### 200 Response
* email - string
* email_verified - boolean
* name - string
* picture - string
* given_name - string
* family_name - string
* locale - string

##### 401 Unauthorized
* statusCode = 401
* error = 'Unauthorized'
* message - string
