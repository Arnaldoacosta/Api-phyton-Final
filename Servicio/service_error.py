
from flask import jsonify
from flask_api import FlaskAPI, status


class ApiException(Exception):
    
    def getCode():
        return None

    def __init__(self, payload=None):
        Exception.__init__(self)       
        #self.status_code = self.status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class NotFound(ApiException):
    message='error de la exepcion'
    status_code=status.HTTP_400_BAD_REQUEST

class Created(ApiException):
    message='Registro creado exitosamente'
    status_code=status.HTTP_201_CREATED

