from flask import Blueprint, render_template, jsonify
from app.dao.referenciales.nacionalidad.NacioDao import NacioDao
naciomod = Blueprint('nacionalidad', __name__, template_folder='templates')

@naciomod.route('/nacio-index')
def nacioIndex():
    naciodao = NacioDao()
    return render_template('nacio-index.html',  lista_nacionalidades=naciodao.getNacionalidades())