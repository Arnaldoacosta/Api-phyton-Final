from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask import jsonify
db=SQLAlchemy()

class NotaMateria(db.Model):
    __tablename__ = 'notamateria'
    __table_args__ = {'extend_existing': True}
    

    notamateria_id = db.Column(db.Integer, primary_key=True)
    alumno_fk = db.Column(db.Integer)
    nombremateria = db.Column(db.String(2))
    notafinal = db.Column(db.Integer)

    def __init__(self,alumno,nombremateria,notafinal,notamateriaid,isNew):
        self.alumno_fk=alumno,  
        self.nombremateria=nombremateria,
        self.notafinal=notafinal,
        if (not(isNew)):
            self.notamateria_id=notamateriaid       

    def save(self):
        db.session.add(self)
        db.session.commit()      

    def __repr__(self):
        return '{}'.format(self.notamateria_id)

    @staticmethod
    def getNotasMaterias():
            #NotaMateria.query(func.count(User.id))
        return NotaMateria.query.order_by(NotaMateria.alumno_fk).all() 

    @staticmethod
    def getNotaMateriaByNotamateriaID(notamateria_id):
        return NotaMateria.query.filter_by(notamateria_id=notamateria_id).first()

    @staticmethod
    def getNotaMateriaNotamateriaIDToAlumnoID(notamateria_id,alumnoid):
        return NotaMateria.query.filter_by(notamateria_id=notamateria_id, alumno_fk=alumnoid).first()

    @staticmethod
    def getNotaMateriaToAlumnoIDByNotamateriaIDNombreMateria(notamateria_id,alumnoid,nombremateria):
        return NotaMateria.query.filter_by(notamateria_id=notamateria_id, alumno_fk=alumnoid,nombremateria=nombremateria).first()

    @staticmethod
    def getNotaMateriaByNombreMateria(alumnoid,nombremateria):
        return NotaMateria.query.filter_by(nombremateria=nombremateria,alumno_fk=alumnoid).first()

    @staticmethod
    def getNotasMateriasByAlumnoID(id):
        return NotaMateria.query.filter_by(alumno_fk=id).order_by(NotaMateria.nombremateria).all()
        '''query = NotaMateria.query.filter(User.name.like('%ed')).order_by(User.id)'''
        '''return NotaMateria.query.filter_by(alumno_fk=id).first_or_404(description='No existe datos con el ID ={}'.format(id))'''
    #session.query(User).filter_by(name='jack').count() hacer esto para verificar si fue eliminado

    @staticmethod
    def existsNombreMateriaToAlumnoID(alumnoid,nombremateria):
        exists = bool(NotaMateria.query.filter_by(alumno_fk=alumnoid, nombremateria=nombremateria).first())
        return exists

    @staticmethod
    def existsMateriaIDToAlumnoID(alumnoid,notamateriaid):
         exists = bool(NotaMateria.query.filter_by(alumno_fk=alumnoid, notamateria_id=notamateriaid).first())
         return exists

    @staticmethod
    def getNotamateriaToAlumnoIDbyNombreMateria(idalumno,nombremateria):
        materia_buscar=str(nombremateria)
        materia_buscar = materia_buscar.replace('"', '');
        cmd = "Select * from notamateria where nombremateria ILIKE'" + "%" + materia_buscar+ "%'" + " and alumno_fk=" + str(idalumno)
        #cmd = "Select * from notamateria where nombremateria like'" + "%" + materia_buscar+ "%'" + " and alumno_fk=:alumno" 
        #result = db.engine.execute(text(cmd),alumno=idalumno) 
        result = db.engine.execute(text(cmd))  
        return result

    def delete(self):
        db.session.delete(self)
        db.session.commit() 

    def serializar(self):
        return {
            'notamateria_id': self.notamateria_id,
            'alumno_id': self.alumno_fk,
            'nombremateria':self.nombremateria,
            'notafinal':self.notafinal                   
        }
        
    def serializarManual(notamateria_id,alumno_fk,nombremateria,notafinal):
        return {
            'notamateria_id': notamateria_id,
            'alumno_id': alumno_fk,
            'nombremateria':nombremateria,
            'notafinal':notafinal                   
        }