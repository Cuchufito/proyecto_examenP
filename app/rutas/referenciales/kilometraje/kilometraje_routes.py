from flask import Blueprint, render_template, jsonify
from app.dao.referenciales.kilometraje.KilometrajeDao import KilometrajeDao

kilomod = Blueprint('kilometraje', __name__, template_folder='templates')

@kilomod.route('/kilometraje-index')
def kilometrajeIndex():
    kilodao = KilometrajeDao()
    return render_template('kilometraje-index.html', lista_kilometraje=kilodao.getKilometrajes())
