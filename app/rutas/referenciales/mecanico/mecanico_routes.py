from flask import Blueprint, render_template, jsonify
from app.dao.referenciales.mecanico.MecanicoDao import MecanicoDao

mecamod = Blueprint('mecanicos', __name__, template_folder='templates')

@mecamod.route('/mecanicos-index')
def mecanicoIndex():
    mecanicodao = MecanicoDao()
    return render_template('mecanico-index.html', lista_mecanicos=mecanicodao.getMecanicos())
