from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='static')
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

class Preceptor(db.Model):
    __tablename__ = 'preceptor'
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(30), nullable = False)
    apellido = db.Column(db.String(30), nullable = False)
    correo = db.Column(db.String(30), unique = True, nullable = False)
    clave = db.Column(db.String(30), nullable = False)
    
    def toJson(self):
        d = dict(
            id = self.id,
            nombre= self.nombre,
            apellido = self.apellido,
            correo = self.correo,
            clave=self.clave
        )
        return d
class Padre(db.Model):
    __tablename__ = 'padre'
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(30), nullable = False)
    apellido = db.Column(db.String(30), nullable = False)
    correo = db.Column(db.String(30), unique = True, nullable = False)
    clave = db.Column(db.String(30), nullable = False)
    def toJson(self):
        d = dict(
            id = self.id,
            nombre= self.nombre,
            apellido = self.apellido,
            correo = self.correo,
            clave=self.clave
        )
        return d
class estudiante(db.Model):
    __tablename__ = 'estudiante'
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(30), nullable = False)
    apellido = db.Column(db.String(30), nullable = False)
    dni = db.Column(db.String(20), unique = True, nullable = False)
    idcurso = db.Column(db.Integer, db.ForeignKey('Curso.id'))
    idpadre = db.Column(db.Integer, db.ForeignKey('Padre.id'))
    
    def __gt__(self, otroEstudiante):
        nom1 = self.apellido + self.nombre
        nom2 = otroEstudiante.apellido + otroEstudiante.nombre
        return nom1 > nom2
    def toJson(self):
        d = dict(
            id = self.id,
            nombre= self.nombre,
            apellido = self.apellido,
            dni = self.dni,
            idcurso=self.idcurso,
            idpadre=self.idpadre
        )
        return d
    
class Asistencia(db.Model):
    __tablename__ = 'asistencia'
    id = db.Column(db.Integer, primary_key = True)
    fecha = db.Column(db.DateTime)
    codigoclase = db.Column(db.Integer)
    asistio = db.Column(db.String(1))
    justificacion = db.Column(db.String(30))
    idestudiante = db.Column(db.Integer, db.ForeignKey('estudiante.id'))
    
    def __init__(self, fecha, cod, asis, jus, idE):
        self.fecha = fecha
        self.codigoclase = cod
        self.asistio = asis
        self.justificacion = jus
        self.idestudiante = idE

        
    def toJson(self):
        d = dict(
            id = self.id,
            fecha= self.nombre,
            codigoclase = self.apellido,
            asistio = self.correo,
            justificacion=self.clave,
            idEstudiante=self.idEstudiante
        )
        return d
    def __str__(self):
        return "id asistencia: " + str(self.id) + "Codigo clase: " + str(self.codigoclase) + "Asistio: " + self.asistio
class Curso(db.Model):
    __tablename__ = 'curso'
    id = db.Column(db.Integer, primary_key = True)
    anio = db.Column(db.Integer)
    division = db.Column(db.Integer)
    idPreceptor = db.Column(db.Integer, db.ForeignKey('Preceptor.id'))
    
    def toJson(self):
        d = dict(
            id = self.id,
            anio= self.anio,
            division = self.division,
            idPreceptor = self.idPreceptor
        )
        return d