from flask import Blueprint, render_template, jsonify
from app.dao.referenciales.persona.PersonaDao import PersonaDao

permod = Blueprint('persona', __name__, template_folder='templates')

@permod.route('/persona-index')
def personaIndex():
    personadao = PersonaDao()
    return render_template('persona-index.html', lista_personas=personadao.getPersonas())
