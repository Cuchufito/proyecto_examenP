from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# ───── IMPORTAR BLUEPRINTS DE VISTAS ─────
from app.rutas.referenciales.persona.persona_routes import permod
from app.rutas.referenciales.sexo.sexo_routes import sexmod
from app.rutas.referenciales.paises.pais_routes import paimod
from app.rutas.referenciales.nacionalidad.nacio_routes import naciomod
from app.rutas.referenciales.ciudad.ciudad_routes import ciumod
from app.rutas.referenciales.estado_civil.estado_civil_routes import estacivmod
from app.rutas.referenciales.ocupacion.ocupacion_routes import ocupmod
from app.rutas.referenciales.recepciones.recepcion_routes import recemod
from app.rutas.referenciales.estado_servicio.estado_servicio_routes import estaservimod
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

# ───── REGISTRAR BLUEPRINTS DE VISTAS ─────
modulo0 = '/referenciales'
app.register_blueprint(permod, url_prefix=f'{modulo0}/persona')
app.register_blueprint(sexmod, url_prefix=f'{modulo0}/sexo')
app.register_blueprint(paimod, url_prefix=f'{modulo0}/paises')
app.register_blueprint(naciomod, url_prefix=f'{modulo0}/nacionalidad')
app.register_blueprint(ciumod, url_prefix=f'{modulo0}/ciudad')
app.register_blueprint(estacivmod, url_prefix=f'{modulo0}/estadocivil')
app.register_blueprint(ocupmod, url_prefix=f'{modulo0}/ocupacion')
app.register_blueprint(recemod, url_prefix=f'{modulo0}/recepciones')
app.register_blueprint(estaservimod, url_prefix=f'{modulo0}/estadoservicio')
app.register_blueprint(vehimod, url_prefix=f'{modulo0}/vehiculos')
app.register_blueprint(mecamod, url_prefix=f'{modulo0}/mecanicos')
app.register_blueprint(repumod, url_prefix=f'{modulo0}/repuestos')
app.register_blueprint(turmod, url_prefix=f'{modulo0}/turnos')
app.register_blueprint(inimod, url_prefix=f'{modulo0}/inicio')
app.register_blueprint(provemod, url_prefix=f'{modulo0}/proveedor')
app.register_blueprint(kilomod, url_prefix=f'{modulo0}/kilometraje')
app.register_blueprint(marmod, url_prefix=f'{modulo0}/marca')
app.register_blueprint(modemod, url_prefix=f'{modulo0}/modelo')
app.register_blueprint(placamod, url_prefix=f'{modulo0}/placa')

# ───── IMPORTAR Y REGISTRAR BLUEPRINTS DE API ─────
version1 = '/api/v1'
from app.rutas.referenciales.persona.persona_api import perapi
from app.rutas.referenciales.sexo.sexo_api import sexapi
from app.rutas.referenciales.paises.pais_api import paisapi
from app.rutas.referenciales.nacionalidad.nacio_api import nacioapi
from app.rutas.referenciales.ciudad.ciudad_api import ciuapi
from app.rutas.referenciales.estado_civil.estado_civil_api import estacivapi
from app.rutas.referenciales.ocupacion.ocupacion_api import ocupapi
from app.rutas.referenciales.recepciones.recepcion_api import recepapi
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

# Registrar todos los endpoints API bajo el prefijo /api/v1
app.register_blueprint(perapi, url_prefix=version1)
app.register_blueprint(sexapi, url_prefix=version1)
app.register_blueprint(paisapi, url_prefix=version1)
app.register_blueprint(nacioapi, url_prefix=version1)
app.register_blueprint(ciuapi, url_prefix=version1)
app.register_blueprint(estacivapi, url_prefix=version1)
app.register_blueprint(ocupapi, url_prefix=version1)
app.register_blueprint(recepapi, url_prefix=version1)
app.register_blueprint(estaserviapi, url_prefix=version1)
app.register_blueprint(veapi, url_prefix=version1)
app.register_blueprint(mecapi, url_prefix=version1)
app.register_blueprint(repuapi, url_prefix=version1)
app.register_blueprint(turapi, url_prefix=version1)
app.register_blueprint(proapi, url_prefix=version1)
app.register_blueprint(kiloapi, url_prefix=version1)
app.register_blueprint(marcapi, url_prefix=version1)
app.register_blueprint(modelapi, url_prefix=version1)
app.register_blueprint(placapi, url_prefix=version1)

# ───── FUNCIONES ADICIONALES (BUSCAR / LOGIN) ─────
@app.route('/buscar', methods=['GET'])
def buscar():
    termino = request.args.get('termino').lower()
    rutas = {
        'ciudad': 'ciudad.ciudadIndex',
        'ciudades': 'ciudad.ciudadIndex',
        'pais': 'pais.paisIndex',
        'paises': 'pais.paisIndex',
        'nacionalidad': 'nacionalidad.nacionalidadIndex',
        'nacionalidades': 'nacionalidad.nacionalidadIndex',
        'ocupacion': 'ocupacion.ocupacionIndex',
        'ocupaciones': 'ocupacion.ocupacionIndex',
        'estado civil': 'estadocivil.estadocivilIndex',
        'estados civiles': 'estadocivil.estadocivilIndex',
        'sexo': 'sexo.sexoIndex',
        'sexos': 'sexo.sexoIndex',
        'persona': 'persona.personaIndex',
        'personas': 'persona.personaIndex',
        'kilometraje': 'kilometraje.kilometrajeIndex',
        'kilometrajes': 'kilometraje.kilometrajeIndex',
        'turno': 'turno.turnoIndex',
        'turnos': 'turno.turnoIndex'
    }
    if termino in rutas:
        return redirect(url_for(rutas[termino]))
    return render_template('no_encontrado.html', termino=termino)

@app.route('/login')
def login():
    return render_template('login.html')

# ───── INICIO DEL SERVIDOR ─────
if __name__ == '__main__':
    app.run(debug=True)
