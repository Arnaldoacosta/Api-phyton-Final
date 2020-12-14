
from flask import jsonify
from flask_api import FlaskAPI, status

'''class ApiException(Exception):  
    def getCode():
        return None

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class NotFound(ApiException):
   
    def getCode():
        return 404
'''

class APIException(Exception):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ''

    def __init__(self, detail=None):
        if detail is not None:
            self.detail = detail

    def __str__(self):
        return self.detail


class NotFound(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Malformed request.'
