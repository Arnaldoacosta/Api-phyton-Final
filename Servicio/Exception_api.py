
from flask import jsonify
from flask_api import FlaskAPI, status



class ApiExceptionServ(Exception):
    
    def getCode():
        return None

    '''def __init__(self, payload=None):
        Exception.__init__(self)       
        #self.status_code = self.status_code
        self.payload = payload
        self.errointerno=errointerno'''

    def __init__(self, message_interno, cod_interno=None, payload=None):
        Exception.__init__(self)
        #self.message = message
        self.message_interno=message_interno
        self.cod_interno=cod_interno
        #if status_code is not None:
        #    self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['Detalle'] = self.message
        rv['cod_interno'] = self.cod_interno 
        rv['mensaje_interno'] = self.message_interno       
        return rv

class NotFound(ApiExceptionServ):
    message='Recurso no encontrado.'
    status_code=status.HTTP_404_NOT_FOUND

class InternalServerError(ApiExceptionServ):
    message='Error interno.'
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR

class BadResquest(ApiExceptionServ):
    message='Solicitud incorrecta.'
    status_code=status.HTTP_400_BAD_REQUEST


class Conflict(ApiExceptionServ):
    message='Recurso en conflicto.'
    status_code=status.HTTP_409_CONFLICT

