from Modelo.model_notasMaterias import NotaMateria
from flask import jsonify
import json
from app import Response
from flask_api import FlaskAPI, status
from Servicio.Exception_api import *
import requests
from Servicio.Internal_errors import CodeInternalError
from Servicio.global_variable import ADD_NEW,UPDATE


Listamaterias = ['Administración de proyectos', 
     'Algoritmo',
     'Análisis y metodología de sistemas',
     'Ética profesional', 
     'Estadística',
     'Estructura de datos',
     'Introducción a la informática',
     'Seguridad e integridad de sistemas',
     'Sistemas administrativos',
     'Taller de creactividad e innovación',
     'Taller de prácticas de sistemas',
     'Taller VI']

def getNotamateriaToAlumnoIDbyNombreMateria(idalumno,argumentos):
    isvalidArgs(argumentos)
    nombremateria=argumentos.get("nombremateria")
    if (nombremateria):
        nombremateria_string = nombremateria.replace('"', '');
        retorno=isNumber(nombremateria_string)
        if (not(isNumber(nombremateria_string))):         
            notamateria=NotaMateria.getNotamateriaToAlumnoIDbyNombreMateria(idalumno,nombremateria)
            cantidadRegistros=notamateria.rowcount
            if (notamateria.rowcount==0):
                raise NotFound('El recurso buscado no existe.', CodeInternalError.ERROR_INTERNAL_13_REQUEST_DATA_NOT_MATCHED)
                #return ('',status.HTTP_204_NO_CONTENT)
            elif (notamateria.rowcount==1):
                    resultadojson1=[]                  
                    for itm in notamateria:
                        return (NotaMateria.serializarManual(itm.notamateria_id,itm.alumno_fk,itm.nombremateria,itm.notafinal))
                        '''
                        notatemporal1=NotaMateria.serializarManual(itm.notamateria_id,itm.alumno_fk,itm.nombremateria,itm.notafinal)
                        resultadojson1.append(notatemporal1)
                    return jsonify(resultadojson1)
                    '''
            else:
                resultadojson=[]
                for itm in notamateria:
                    notatemporal=NotaMateria.serializarManual(itm.notamateria_id,itm.alumno_fk,itm.nombremateria,itm.notafinal)
                    resultadojson.append(notatemporal)
                return jsonify(resultadojson) 
        else:
            raise BadResquest('Nombremateria no puede ser un número.', CodeInternalError.ERROR_INTERNAL_13_REQUEST_DATA_NOT_MATCHED)
    else:
        raise NotFound('El recurso buscado no existe.', CodeInternalError.ERROR_INTERNAL_13_REQUEST_DATA_NOT_MATCHED)
    #if (argumentos.get("nombremateria")):


#region add materia
def addNotaMateria(request,alumnoid):
    if (not(isNumber(alumnoid))):
        raise BadResquest('AlumnoID no es un tipo de dato valido.', CodeInternalError.ERROR_INTERNAL_13_REQUEST_DATA_NOT_MATCHED)
    notamateria=setNotaMateria(request,ADD_NEW,alumnoid)
    json_recibido=request.json
    nombremateria=json_recibido['nombremateria']
    existe=nombremateria in Listamaterias
    if (not(existe)):
        raise BadResquest('No existe el nombre de la materia', CodeInternalError.ERROR_INTERNAL_13_REQUEST_DATA_NOT_MATCHED)
    if (NotaMateria.existsNombreMateriaToAlumnoID(notamateria.alumno_fk,nombremateria)==True):
        raise Conflict('Existe una nota para esta materia.', CodeInternalError.ERROR_INTERNAL_14_REQUEST_DATA_DUPLICATED)
    else:
        try:
            notamateria.save()
            retorno_id=notamateria.__repr__()
            notamateria_created=notamateria.getNotaMateriaByNotamateriaID(retorno_id)
            return jsonify(alumnoid=notamateria_created.alumno_fk,
                           notamateriaid=notamateria_created.notamateria_id,
                           nombremateria=notamateria_created.nombremateria,
                           notafinal=notamateria_created.notafinal,
                            ), status.HTTP_201_CREATED
            return (retorno_id)
        except Exception as identifier:
            raise InternalServerError('Error relacionado con base de datos', CodeInternalError.ERROR_INTERNAL_11_CONEXION_BD)              
#endregion 

#region get all nota s manteria by ALUMNO ID
def getNotasMateriasByAlumnoID(alumnoid):
    if not(isNumber(alumnoid)):
        raise BadResquest('AlumnoID no es un tipo de dato valido.', CodeInternalError.ERROR_INTERNAL_13_REQUEST_DATA_NOT_MATCHED)
    try:
        obj=NotaMateria.getNotasMateriasByAlumnoID(alumnoid)
    except Exception as identifier:
        raise InternalServerError('Error relacionado con base de datos.', CodeInternalError.ERROR_INTERNAL_11_CONEXION_BD)          
    if (obj is not None and len(obj)>1):
        json_Str=jsonify([e.serializar() for e in obj]) 
        return json_Str
    elif (obj is not None and len(obj)==1):
        for itm in obj:
            return NotaMateria.serializarManual(itm.notamateria_id,itm.alumno_fk,itm.nombremateria,itm.notafinal)
    else:
        raise NotFound('El recurso buscado no existe.', CodeInternalError.ERROR_INTERNAL_13_REQUEST_DATA_NOT_MATCHED)
#endregion

#region get one notamanteriaID to an AlumnoID
def getNotasMateriasToAlumnoIDbyNotaMateriaID(alumnoid,materiaid):
    if (not(isNumber(alumnoid))):
        raise BadResquest(identifier, CodeInternalError.ERROR_INTERNAL_13_REQUEST_DATA_NOT_MATCHED)
    elif (not(isNumber(materiaid))):
        raise BadResquest(identifier, CodeInternalError.ERROR_INTERNAL_13_REQUEST_DATA_NOT_MATCHED)
    try:
        notamateria=NotaMateria.getNotaMateriaNotamateriaIDToAlumnoID(materiaid,alumnoid)
    except Exception as identifier:
        raise InternalServerError('Error relacionado en base de datos.', CodeInternalError.ERROR_INTERNAL_11_CONEXION_BD)          
    if notamateria is not None:
        return jsonify  (alumno_id=notamateria.alumno_fk,
                        notamateria_id=notamateria.notamateria_id,
                        nombremateria=notamateria.nombremateria,
                        notafinal=notamateria.notafinal,
                        )
    else:
        raise NotFound('No se encontraron los datos solicitados.',CodeInternalError.ERROR_INTERNAL_12_REQUEST_NOT_FOUND)
#endregion


#region Get all NotasMaterias
def getNotasMaterias():
    materias=NotaMateria.buscarNotasMaterias()
    json_Str=jsonify([e.serializar() for e in materias]) 
    return json_Str
    '''page=NotaMateria.buscarNotasMaterias()
    final_list = []
    for element in page:
       final_list.append(element)
    return jsonify(final_list), status_code'''
#endregion
    

#region Update notamateria
def updateNotaMateria(request,alumnoid,notamateriaid): 
    try:
        json_recibido=request.json
        nombremateria=json_recibido['nombremateria']
        notafinal=request.json['notafinal']
    except Exception as identifier:
        raise BadResquest('Estructa de Json incorrecta.',CodeInternalError.ERROR_INTERNAL_10_JSON_BAD_FORMED) 
    #se valida el nro de la nota
    if (not(isNumber(alumnoid))):
        raise BadResquest('AlumnoID no es un tipo de dato valido.', CodeInternalError.ERROR_INTERNAL_13_REQUEST_DATA_NOT_MATCHED)
    elif (not(isNumber(notamateriaid))):
        raise BadResquest('NotamateriaID no es un tipo de dato valido.', CodeInternalError.ERROR_INTERNAL_13_REQUEST_DATA_NOT_MATCHED)
    if (not(isNumber(notafinal))):
        raise BadResquest('Nota final no es un tipo de dato valido.', CodeInternalError.ERROR_INTERNAL_13_REQUEST_DATA_NOT_MATCHED)
    isValidNotaFinal(notafinal)
    existe=nombremateria in Listamaterias
    if (not(existe)):
        raise BadResquest('No existe el nombre de la materia.', CodeInternalError.ERROR_INTERNAL_13_REQUEST_DATA_NOT_MATCHED)
    #Si el objeto recibido es igual que en la base devuelve el mismo. Si no lo es, se valida que no este actualizando
    #la materia_id con un nombre de materia ya existente.
    if (NotaMateria.existsMateriaIDToAlumnoID(alumnoid,notamateriaid)):
        notaMateria_base=NotaMateria.getNotaMateriaNotamateriaIDToAlumnoID(notamateriaid,alumnoid)
        if (notaMateria_base.nombremateria==nombremateria and notaMateria_base.notafinal==notafinal):
            return jsonify(alumnoid=alumnoid,
                    notamateriaid=notamateriaid,
                    nombremateria=nombremateria,
                    notafinal=notafinal,
                    )
        else:
            if (NotaMateria.existsNombreMateriaToAlumnoID(alumnoid,nombremateria)):
                notamateria_existente=NotaMateria.getNotaMateriaByNombreMateria(alumnoid, nombremateria)
                if (notamateria_existente.notamateria_id!=notaMateria_base.notamateria_id):
                    raise Conflict('Existe otra materia con el mismo nombre.', CodeInternalError.ERROR_INTERNAL_14_REQUEST_DATA_DUPLICATED)
                else:          
                    notamateria=NotaMateria.getNotaMateriaByNotamateriaID(notamateriaid)
                    notamateria.nombremateria=nombremateria
                    notamateria.notafinal=notafinal
                    notamateria.save()
                    notamateria_updated=NotaMateria.getNotaMateriaByNotamateriaID(notamateriaid)
                    return jsonify(alumnoid=notamateria_updated.alumno_fk,
                                notamateriaid=notamateria_updated.notamateria_id,
                                nombremateria=notamateria_updated.nombremateria,
                             notafinal=notamateria_updated.notafinal,
                            )
            else:
                notamateria=NotaMateria.getNotaMateriaByNotamateriaID(notamateriaid)
                notamateria.nombremateria=nombremateria
                notamateria.notafinal=notafinal
                notamateria.save()
                notamateria_updated=NotaMateria.getNotaMateriaByNotamateriaID(notamateriaid)
                return jsonify(alumnoid=notamateria_updated.alumno_fk,
                    notamateriaid=notamateria_updated.notamateria_id,
                    nombremateria=notamateria_updated.nombremateria,
                    notafinal=notamateria_updated.notafinal,
                    )
    else:
        raise BadResquest('Los datos recibidos no coinciden.',CodeInternalError.ERROR_INTERNAL_13_REQUEST_DATA_NOT_MATCHED) 
    #aca termina la posta#
    
#region Update notamateria byAlumnoID
def updateNotaMateriasByAlumnoID(id):
    try:      
        obj=NotaMateria.buscarMateriasByAlumnoID(id)
        json_str=jsonify([e.serializar() for e in obj])
        return (json_str)
    except Exception as e:
	    return(str(e))
#endregion 

#region delete notamaterias
def deleteNotaMateria(alumnoid,notamateriaid):    
    if (not(isNumber(notamateriaid))):
        BadResquest('NotamateriaID no es un tipo de dato valido.', CodeInternalError.ERROR_INTERNAL_13_REQUEST_DATA_NOT_MATCHED)
    if (not(isNumber(alumnoid))):
        BadResquest('AlumnoID no es un tipo dato valido.', CodeInternalError.ERROR_INTERNAL_13_REQUEST_DATA_NOT_MATCHED)
    if (not(NotaMateria.existsMateriaIDToAlumnoID(alumnoid,notamateriaid))):
        raise NotFound('No existe la materia para el alumno asociado.', CodeInternalError.ERROR_INTERNAL_12_REQUEST_NOT_FOUND)   
    try:
        notamateria_delete=NotaMateria.getNotaMateriaByNotamateriaID(notamateriaid)
        notamateria_delete.delete()
        return ('',status.HTTP_204_NO_CONTENT)
    except Exception as identifier:
        raise InternalServerError('Error relacionado con base de datos.', CodeInternalError.ERROR_INTERNAL_11_CONEXION_BD)   
#endregion     

#region Common Methods
def setNotaMateria(request,action,alumnoid=0):
    try:  
        request.get_json()
    except Exception as identifier:
        raise BadResquest('Estructura de archivo invalida.',CodeInternalError.ERROR_INTERNAL_10_JSON_BAD_FORMED)
    isValidDataType(request)
    isValidNotaFinal(request.json['notafinal']) 
    if (action):
        notamateria=NotaMateria(
            alumnoid,
            request.json['nombremateria'],
            request.json['notafinal'],
            0,
            ADD_NEW
        )
    #else:
     #   try:  
      #      notamateria=NotaMateria(
      #          request.json['alumno_id'],
       #         request.json['nombremateria'],
       #         request.json['notafinal'],
        #        request.json['notamateria_id'],
        #        UPDATE
        #    )
     #   except Exception as identifier:
        #    raise BadResquest('Estructura de archivo invalida',CodeInternalError.ERROR_INTERNAL_10_JSON_BAD_FORMED)'''
    return notamateria

def isValidDataType(request):
    if (str((request.json['nombremateria'])).isnumeric()):
        raise BadResquest('Nombre de materia no es un tipo de dato valido.',CodeInternalError.ERROR_INTERNAL_13_REQUEST_DATA_NOT_MATCHED)
    elif (not(isNumber((request.json['notafinal'])))):
        raise BadResquest('Nota final no es un tipo de dato valido.',CodeInternalError.ERROR_INTERNAL_13_REQUEST_DATA_NOT_MATCHED)


''' Valida que sea entero'''         
def isNumber(attribute):
    try:
        int(attribute)
        return True
    except:
        return False

'''Valida cantidad de argumentos'''
def isvalidArgs(argumento): 
    vec=[]
    for it in argumento:
        vec.append(it)
    cantidad_Arg=(len(vec))
    if cantidad_Arg>1:
        raise NotFound('Cantidad de argumentos no soportado.',CodeInternalError.ERROR_INTERNAL_13_REQUEST_DATA_NOT_MATCHED)


#region bussiness rules
def isValidNotaFinal(notafinal):
    if (int(notafinal)>=11 or int(notafinal)<1):
        raise BadResquest('Se requiere una nota entre 1 y 10.',CodeInternalError.ERROR_INTERNAL_13_REQUEST_DATA_NOT_MATCHED)
#endregion 


