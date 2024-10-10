from flask import Blueprint, render_template
from app.dao.referenciales.modelo.ModeloDao import ModeloDao

modemod = Blueprint('modelo', __name__, template_folder='templates')

@modemod.route('/modelo-index')
def modeloIndex():
    modelodao=ModeloDao()
    return render_template('modelo-index.html' ,lista_modelos=modelodao.getModelos())