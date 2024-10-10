from flask import Blueprint, render_template, jsonify
from app.dao.referenciales.paises.PaisDao import PaisDao
paimod = Blueprint('pais', __name__, template_folder='templates')

@paimod.route('/pais-index')
def paisIndex():
    paidao = PaisDao()
    return render_template('pais-index.html',  lista_paises=paidao.getPaises())