from flask import Flask, render_template, request, redirect, session, url_for
from classModel import app, db
from classModel import Preceptor, Padre, Asistencia, estudiante, Curso
import hashlib
from metodoburbuja import metodoBurbuja
from datetime import datetime

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/Ingreso', methods = ['POST', 'GET'])
def ingreso():
    if request.method == 'POST':
        usuario = request.form['usuario']               #RECUPERAMOS EL USUARIO
        contra = request.form['contraseña']             #RECUPERAMOS LA CONTRASEÑA INGRESADA
        contraseña =  hashlib.md5(bytes(contra, encoding='utf-8')) #CIFRAMOS LA CONTRASEÑA PARA COMPARARLA CON LA DE LA BASE DE DATOS POSTERIORMENTE
        objeto = Preceptor.query.filter_by(correo=usuario).first() #RECUPERAMOS EL OBJETO PRECEPTOR ATRAVEZ DE EL USUARIO
        if objeto == None:                                       #EN CASO DE QUE EL OBJETO SEA IGUAL NONE SIGNIFICA QUE NO ES UN PRECEPTOR
            objeto = Padre.query.filter_by(correo=usuario).first() #RECUPERAMOS EL OBJETO PADRE ATRAVEZ DE EL USUARIO
        if objeto == None:                              #EN CASO DE EL OBJETO SIGA SIENDO IGUAL A NONE SIGNIFICA QUE NO SE ENCONTRO EL USUARIO YA QUE NO PERTENECE A UN PRECEPTOR NI A UN PADRE REGISTRADO EN LA BASE DE DATOS
            return render_template('error.html', mensaje='Usuario no registrado') #SE DIRIGE A LA PAGINA QUE INFORMA QUE NO SE ENCONTRO EL USUARIO
        else:
            if contraseña.hexdigest() == objeto.clave: #EN CASO DE QUE SE ENCONTRARA EL USUARIO COMPARAMOS LA CONTRASEÑA INGRESADA CON LA CONTRASEÑA DEL OBJETO
                if isinstance(objeto,Preceptor):
                    session['usuario'] = usuario #GUARDAMOS EL USUARIO PARA UTILIZARLO LUEGO
                    return redirect(url_for('MenuPreceptor')) #SI ES PRECEPTOR REDIRIGIMOS AL MENU DE PRECEPTORES
                else:
                    return redirect(url_for('MenuPadres')) #SI ES PADRE REDIRIGIMOS AL MENU DE PADRES
            else:
                return render_template('error.html', mensaje='Contraseña incorrecta') #LA CONTRASEÑA ES INCORRECTA Y INFORMAMOS EL ERROR
    else:
        return render_template('index.html')

@app.route('/MenuPadres')
def MenuPadres():
    return render_template('papa.html')

@app.route('/MenuPreceptor', methods = ['POST', 'GET'])    #MENU PRECEPTOR
def MenuPreceptor():
    usuario = session.get('usuario') #RECUPERAMOS EL USUARIO 
    Prece = Preceptor.query.filter_by(correo=usuario).first() #RECUPERAMOS EL OBJETO PRECEPTOR ASOCIADO A ESE USUARIO
    return render_template('menuPreceptor.html', nombre=Prece.nombre, apellido=Prece.apellido)

@app.route('/RegistrarAsistencia', methods = ['POST', 'GET'])
def RegistrarAsistencia():
    usuario = session.get('usuario') #RECUPERAMOS EL USUARIO 
    Prece = Preceptor.query.filter_by(correo=usuario).first() #RECUPERAMOS EL OBJETO PRECEPTOR ASOCIADO A ESE USUARIO
    idPrece = Prece.id 
    cursos = Curso.query.all() #RECUPERAMOS TODOS LOS OBJETOS DE TIPO CURSO
    cursosPreceptor = [] #CREAMOS LISTA PARA GUARDAR TODOS LOS CURSOS PERTENECIENTES AL PRECEPTOR
    for curso in cursos:
        if curso.idPreceptor == idPrece: #SI EL IDPRECEPTOR DE UN CURSO COINCIDE CON EL ID DEL PRECEPTOR QUE INGRESO A LA PLATAFORMA GUARDAMOS EL CURSO EN LA LISTA
            cursosPreceptor.append(curso) 
    return render_template('consultarCurso.html', cursosPreceptor=cursosPreceptor)

@app.route('/ListaAlumnos', methods = ['POST', 'GET'])
def ListaAlumnos():
    if request.method == 'POST':
        cursoId = int(request.form['Opcion']) #RECUPERAMOS EL CURSO SELECCIONADO
        alumnos = estudiante.query.all() #RECUPERAMOS TODOS LOS OBJETOS DE TIPO ESTUDIANTE
        listaA = [] #CREAMOS LISTA PARA GUARDAR A TODOS LOS ESTUDIANTES PERTENECIENTES AL CURSO
        for alumno in alumnos:
            if cursoId == alumno.idcurso: #SI EL ID DEL CURSO COINCIDE CON EL ID DEL CURSO DEL ESTUDIANTE GUARDAMOS EL ESTUDIANTE EN LA LISTA
                listaA.append(alumno)
        listaOrdenada = metodoBurbuja(listaA) #ORDENAMOS LA LISTA CON EL METODO BURBUJA Y SOBRECARGANDO EL OPERADOR 
        return render_template('ListaAlumnos.html', lista=listaOrdenada)
    else:
        return "Ocurrio un error"
    

@app.route('/AsistenciaGuardada', methods = ['POST', 'GET']) 
def asistenciaGuardada():
    idAlumnos = request.form.getlist('alumno_id[]')
    tiposclases = request.form.getlist('tipo[]')                     #RECUPERAMOS LAS LISTAS DE LOS DATOS INGRESADOS A LA HORA DE REGISTRAR LAS ASISTENCIAS DEL CURSO
    asistencias = request.form.getlist('asistio[]')                 #(LISTA DE IDS, DE TIPOS DE CLASE, ASISTENCIAS Y JUSTIFICACIONES)
    justificaciones = request.form.getlist('justificacion[]')
    for i in range(len(tiposclases)):                               #DEBIDO A QUE TODOS LAS LISTAS TIENEN EL MISMO TAMAÑO PODEMOS ITERARLAS DE ESTA FORMA
        fechaa = datetime.now().date()
        idAlu=idAlumnos[i]
        tipoCla=int(tiposclases[i])                                 #CON LOS DATOS OBTENIDOS CREAMOS LOS ATRIBUTOS QUE ENVIAREMOS PARA CREAR EL OBJETO DE TIPO ASISTENCIA
        asistio = asistencias[i]
        justifica = justificaciones[i]
        nuevaAsistencia = Asistencia(fechaa, tipoCla, asistio, justifica, idAlu)  #CREAMOS EL OBJETO DE TIPO ASISTENCIA
        db.session.add(nuevaAsistencia)                                            #GUARDAMOS EL OBJETO EN LA BASE DE DATOS
    db.session.commit()                                     #REGISTRAMOS LOS CAMBIOS
    return render_template('asistenciaguardada.html')

@app.route('/consultarCurso', methods = ['POST', 'GET'])
def consultarCurso():
    usuario = session.get('usuario') #RECUPERAMOS EL USUARIO 
    Prece = Preceptor.query.filter_by(correo=usuario).first() #RECUPERAMOS EL OBJETO PRECEPTOR ASOCIADO A ESE ID
    idPrece = Prece.id 
    cursos = Curso.query.all()                              #RECUPERAMOS TODOS LOS OBJETOS DE TIPO CURSO
    cursosPreceptor = []                                     #CREAMOS LISTA PARA GUARDAR TODOS LOS CURSOS PERTENECIENTES AL PRECEPTOR
    for curso in cursos:
        if curso.idPreceptor == idPrece:                    #SI EL IDPRECEPTOR DE UN CURSO COINCIDE CON EL ID DEL PRECEPTOR QUE INGRESO A LA PLATAFORMA GUARDAMOS EL CURSO EN LA LISTA
            cursosPreceptor.append(curso)
    return render_template('consultarCurso2.html', cursosPreceptor=cursosPreceptor)
@app.route('/Informe', methods = ['POST', 'GET'])
def informe():
    if request.method == 'POST':
        cursoId = int(request.form['Opcion'])       #RECUPERAMOS EL CURSO SELECCIONADO
        alumnos = estudiante.query.all()            #RECUPERAMOS TODOS LOS ESTUDIANTES
        listaA = []                                 #CREAMOS LISTA PARA GUARDAR LOS ESTUDIANTES PERTENECIENTES AL CURSO
        listaP_aula = []
        listaP_ef = []
        listaA_aula_Jus = []                        #CREAMOS LISTAS PARA GUARDAR LA CANTIDAD DE ASISTENCIAS, INASISTENCIAS, ETC
        listaA_aula_Injus = []
        listaA_ef_Jus = []
        listaA_ef_Injus = []
        listaTotalAusentes = []
        for alumno in alumnos:          
            if cursoId == alumno.idcurso:            #SI EL ALUMNO PERTENECE A LA CLASE LO GUARDAMOS
                listaA.append(alumno)
        listaOrdenada = metodoBurbuja(listaA)       #ORDENAMOS LA LISTA CON EL METODO BURBUJA Y SOBRECARGANDO EL OPERADOR
        asistencias = Asistencia.query.all()        #RECUPERAMOS TODAS LAS ASISTENCIAS
        for alumno in listaOrdenada:                #ITERAMOS LOS ALUMNOS
            Paula=0
            Pef=0
            AaulaJ=0
            AaulaI = 0                              #INICIALIZAMOS EN 0 TODOS LOS CONTADORES PARA ITERARAR UN NUEVO ALUMNO
            AefJ=0
            AefI=0
            Atotal=0
            for asistencia in asistencias:                  #ITERAMOS LAS ASISTENCIAS PARA ENCONTRAR LAS PERTENECIENTES A CADA ALUMNO
                if asistencia.idestudiante == alumno.id:
                    if asistencia.codigoclase == 1:         #ASISTENCIA DE TIPO AULA
                        if asistencia.asistio == "s":       #EN CASO DE PRESENTE
                            Paula += 1
                        else:                               #EN CASO DE AUSENTE
                            if asistencia.justificacion == '':      #EN CASO DE QUE NO EXISTA UNA JUSTIFICACION
                                AaulaI += 1
                                Atotal += 1
                            else:                           #EN CASO DE QUE EL AUSENTE ESTE JUSTIFICADO, AQUI NO SE SUMA EL AUSENTE AL TOTAL
                                AaulaJ +=1
        
                    else:                       #ASISTENCIA DE TIPO EDUCACION FISICA
                        if asistencia.asistio == "s":       #EN CASO DE PRESENTE
                            Pef += 0.5
                        else:                    #EN CASO DE AUSENTE
                            if asistencia.justificacion == '':      #EN CASO DE QUE NO EXISTA UNA JUSTIFICACION
                                AefI += 0.5
                                Atotal += 0.5
                            else:                               #EN CASO DE QUE EXISTA JUSTIFICACION, AQUI NO SE SUMA EL AUSENTE AL TOTAL
                                AefJ += 0.5
            listaP_aula.append(Paula)
            listaP_ef.append(Pef)
            listaA_aula_Injus.append(AaulaI)
            listaA_aula_Jus.append(AaulaJ)              #UNA VEZ FINALIZADA LA ITERACION DE ASISTENCIAS GUARDAMOS LAS CANTIDADES EN SU LISTA CORRESPONDIENTE
            listaA_ef_Injus.append(AefI)                
            listaA_ef_Jus.append(AefJ)
            listaTotalAusentes.append(Atotal)
            
        n=len(listaOrdenada)            #GUARDAMOS LA CANTIDAD DE ALUMNOS Y POR LO TANTO LA CANTIDAD DE COMPONENTES DE TODAS LAS LISTAS, ESTO PARA ITERARLA EN EL ARCHIVO HTML
        
        return render_template('informe.html', n=n, lista=listaOrdenada, pa=listaP_aula, pef=listaP_ef, aai=listaA_aula_Injus, aaj=listaA_aula_Jus, aefi=listaA_ef_Injus, aefj=listaA_ef_Jus, totalA=listaTotalAusentes)



if __name__ == '__main__':
    app.run()
    