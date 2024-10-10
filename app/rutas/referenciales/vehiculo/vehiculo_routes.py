from flask import Blueprint, render_template, jsonify
from app.dao.referenciales.vehiculo.VehiculoDao import VehiculoDao

vehimod = Blueprint('vehiculos', __name__, template_folder='templates')

@vehimod.route('/vehiculo-index')
def vehiculoIndex():
    vehiculodao = VehiculoDao()
    return render_template('vehiculo-index.html', lista_personas=vehiculodao.getVehiculos())
