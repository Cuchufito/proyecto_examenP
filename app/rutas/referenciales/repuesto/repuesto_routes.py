from flask import Blueprint, render_template, jsonify
from app.dao.referenciales.repuesto.RepuestoDao import RepuestoDao

repumod = Blueprint('repuesto', __name__, template_folder='templates')

@repumod.route('/persona-index')
def repuestoIndex():
    repuestodao = RepuestoDao()
    return render_template('repuesto-index.html', lista_personas=repuestodao.getRepuesto())
