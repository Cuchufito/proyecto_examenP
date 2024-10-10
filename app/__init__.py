from flask import Flask

app = Flask(__name__)

# importar referenciales
from app.rutas.referenciales.persona.persona_routes import permod
from app.rutas.referenciales.sexo.sexo_routes import sexmod  #sexo
from app.rutas.referenciales.paises.pais_routes import paimod
from app.rutas.referenciales.nacionalidad.nacio_routes import naciomod
from app.rutas.referenciales.ciudad.ciudad_routes import ciumod
from app.rutas.referenciales.estado_civil.estado_civil_routes import estacivmod  #estado civil
from app.rutas.referenciales.ocupacion.ocupacion_routes import ocupmod  #ocupacion
from app.rutas.referenciales.servicio.servicio_routes import servimod  #servicio
from app.rutas.referenciales.estado_servicio.estado_servicio_routes import estaservimod  #estado del servicio
from app.rutas.referenciales.vehiculo.vehiculo_routes import vehimod
from app.rutas.referenciales.mecanico.mecanico_routes import mecamod
from app.rutas.referenciales.repuesto.repuesto_routes import repumod
from app.rutas.referenciales.turno.turno_routes import turmod
from app.rutas.referenciales.inicio.inicio_routes import inimod
from app.rutas.referenciales.proveedor.proveedor_routes import provemod
from app.rutas.referenciales.kilometraje.kilometraje_routes import kilomod
from app.rutas.referenciales.marca.marca_routes import marmod
from app.rutas.referenciales.modelo.modelo_routes import modemod
from app.rutas.referenciales.placa.placa_routes import placamod

# registrar referenciales
modulo0 = '/referenciales'
app.register_blueprint(permod, url_prefix=f'{modulo0}/persona')
app.register_blueprint(sexmod, url_prefix=f'{modulo0}/sexo')  #sexo
app.register_blueprint(paimod, url_prefix=f'{modulo0}/paises')
app.register_blueprint(naciomod, url_prefix=f'{modulo0}/nacionalidad')
app.register_blueprint(ciumod, url_prefix=f'{modulo0}/ciudad')
app.register_blueprint(estacivmod, url_prefix=f'{modulo0}/estadocivil')  #estado civil
app.register_blueprint(ocupmod, url_prefix=f'{modulo0}/ocupacion')  #ocupacion
app.register_blueprint(servimod, url_prefix=f'{modulo0}/servicios') #servicios
app.register_blueprint(estaservimod, url_prefix=f'{modulo0}/estadoservicio')  #estado del servicio
app.register_blueprint(vehimod, url_prefix=f'{modulo0}/vehiculos')
app.register_blueprint(mecamod, url_prefix=f'{modulo0}/mecanicos')
app.register_blueprint(repumod, url_prefix=f'{modulo0}/repuestos')
app.register_blueprint(turmod, url_prefix=f'{modulo0}/turnos')
app.register_blueprint(inimod, url_prefix=f'{modulo0}/inicico')
app.register_blueprint(provemod, url_prefix=f'{modulo0}/proveedor')
app.register_blueprint(kilomod, url_prefix=f'{modulo0}/kilometraje')
app.register_blueprint(marmod, url_prefix=f'{modulo0}/marca')
app.register_blueprint(modemod, url_prefix=f'{modulo0}/modelo')
app.register_blueprint(placamod, url_prefix=f'{modulo0}/placa')





from app.rutas.referenciales.persona.persona_api import perapi
from app.rutas.referenciales.sexo.sexo_api import sexapi
from app.rutas.referenciales.paises.pais_api import paisapi
from app.rutas.referenciales.nacionalidad.nacio_api import nacioapi
from app.rutas.referenciales.ciudad.ciudad_api import ciuapi
from app.rutas.referenciales.estado_civil.estado_civil_api import estacivapi
from app.rutas.referenciales.ocupacion.ocupacion_api import ocupapi
from app.rutas.referenciales.servicio.servicio_api import serviapi
from app.rutas.referenciales.estado_servicio.estado_servicio_api import estaserviapi
from app.rutas.referenciales.vehiculo.vehiculo_api import veapi
from app.rutas.referenciales.mecanico.mecanico_api import mecapi
from app.rutas.referenciales.repuesto.repuesto_api import repuapi
from app.rutas.referenciales.turno.turno_api import turapi
from app.rutas.referenciales.proveedor.proveedor_api import proapi
from app.rutas.referenciales.kilometraje.kilometraje_api import kiloapi
from app.rutas.referenciales.marca.marca_api import marcapi
from app.rutas.referenciales.modelo.modelo_api import modelapi
from app.rutas.referenciales.placa.placa_api import placapi




#persona
version1 = '/api/v1'
app.register_blueprint(perapi, url_prefix=version1)

#sexo
version1 = '/api/v1'
app.register_blueprint(sexapi, url_prefix=version1)

#Pais
version1 = '/api/v1'
app.register_blueprint(paisapi, url_prefix=version1)

#nacionalaidad
version1 = '/api/v1'
app.register_blueprint(nacioapi ,url_prefix=version1)

#Ciudad
version1 = '/api/v1'
app.register_blueprint(ciuapi, url_prefix=version1)



#Estado civil
version1 = '/api/v1'
app.register_blueprint(estacivapi, url_prefix=version1)

#ocupacion
version1 = '/api/v1'
app.register_blueprint(ocupapi, url_prefix=version1)

#servicio
version1 = '/api/v1'
app.register_blueprint(serviapi, url_prefix=version1)

#Estado del servcio
version1 = '/api/v1'
app.register_blueprint(estaserviapi, url_prefix=version1)

version1 = '/api/v1'
app.register_blueprint(veapi, url_prefix=version1)

version1 = '/api/v1'
app.register_blueprint(mecapi, url_prefix=version1)

version1 = '/api/v1'
app.register_blueprint(repuapi, url_prefix=version1)

version1 = '/api/v1'
app.register_blueprint(turapi, url_prefix=version1)

version1 = '/api/v1'

version1 = '/api/v1'
app.register_blueprint(proapi, url_prefix=version1)

# 
version1 = '/api/v1'
app.register_blueprint(kiloapi, url_prefix=version1)  

version1 = '/api/v1'
app.register_blueprint(marcapi, url_prefix=version1) 

version1 = '/api/v1'
app.register_blueprint(modelapi, url_prefix=version1) 

version1 = '/api/v1'
app.register_blueprint(placapi, url_prefix=version1) 
















from flask import render_template, request, redirect, url_for

@app.route('/buscar', methods=['GET'])
def buscar():
    # Obtener el término de búsqueda del formulario
    termino = request.args.get('termino').lower()

    # Definir las rutas posibles
    rutas = {
        'ciudad': 'ciudad.ciudadIndex',
    'ciudades': 'ciudad.ciudadIndex',  # Agregado
    'pais': 'pais.paisIndex',
    'paises': 'pais.paisIndex',  # Agregado
    'nacionalidad': 'nacionalidad.nacionalidadIndex',
    'nacionalidades': 'nacionalidad.nacionalidadIndex',  # Agregado
    'ocupacion': 'ocupacion.ocupacionIndex',
    'ocupaciones': 'ocupacion.ocupacionIndex',  # Agregado
    'estado civil': 'estadocivil.estadocivilIndex',
    'estados civiles': 'estadocivil.estadocivilIndex',  # Agregado
    'sexo': 'sexo.sexoIndex',
    'sexos': 'sexo.sexoIndex',  # Agregado
    'persona': 'persona.personaIndex',
    'personas': 'persona.personaIndex',  # Agregado
    'cita': 'estadocita.estadocitaIndex',
    'citas': 'estadocita.estadocitaIndex',  # Agregado
    'especialidad': 'especialidad.especialidadIndex',
    'especialidades': 'especialidad.especialidadIndex',  # Agregado
    'dias': 'dia.diaIndex',
    'dia': 'dia.diaIndex',  # Agregado
    'kilometraje': 'kilometraje.kilometrajeIndex',
    'kilometrajes': 'kilometraje.kilometrajeIndex',  # Agregado
    'duracion consulta': 'duracionconsulta.duracionconsultaIndex',
    'duraciones consulta': 'duracionconsulta.duracionconsultaIndex',  # Agregado
    'turno': 'turno.turnoIndex',
    'turnos': 'turno.turnoIndex',  # Agregado
    'test utilizados': 'instrumento.instrumentoIndex',
    'tests utilizados': 'instrumento.instrumentoIndex',  # Agregado
    'tratamientos': 'tratamiento.tratamientoIndex',
    'tratamiento': 'tratamiento.tratamientoIndex'  # Agregado
    }

    # Verificar si el término coincide con alguna clave en rutas
    if termino in rutas:
        # Redirigir a la página correspondiente
        return redirect(url_for(rutas[termino]))
    else:
        # Renderizar una página con un mensaje de "no encontrado"
        return render_template('no_encontrado.html', termino=termino)
    
from flask import render_template, request, redirect, url_for

@app.route('/login')
def login():
    return render_template('login.html')





      # Importar el blueprint de rutas principales

def create_app():
    app = Flask(__name__)
    
    # Registrar los Blueprints
    app.register_blueprint()

    return app






# from flask import Flask, render_template, request, redirect, url_for, flash

# app = Flask(__name__)
# app.secret_key = 'mi_secreto'  # Necesario para mostrar mensajes flash

# # Usuarios de ejemplo (puedes conectar a una base de datos)
# users = {
#     'admin': '6814403',
#     'usuario': '6814403'
# }

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     error = None
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
        
#         # Validar credenciales
#         if username in users and users[username] == password:
#             return redirect(url_for('dashboard'))
#         else:
#             error = 'Credenciales inválidas. Intente de nuevo.'
    
#     return render_template('login.html', error=error)

# @app.route('/dashboard')
# def dashboard():
#     return "¡Bienvenido al Dashboard!"

# if __name__ == '__main__':
#     app.run(debug=True)
