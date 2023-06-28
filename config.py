import os
basedir=os.path.abspath(os.path.dirname(__file__)) ##Obtiene la ruta absoluta del directorio base del archivo actual en el sistema de archivos.
database_path=os.path.join(basedir,'database','datosMod.db') ##Crea la ruta completa del archivo de la base de datos.
SECRET_KEY = 'clave1234' 
SQLALCHEMY_DATABASE_URI = f'sqlite:///{database_path}' ##establece la URI de la base de datos para SQLAlchemy
SQLALCHEMY_TRACK_MODIFICATIONS = False