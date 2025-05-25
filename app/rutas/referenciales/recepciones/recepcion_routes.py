from flask import Blueprint, render_template

recemod = Blueprint('recepciones', __name__, template_folder='templates')

@recemod.route('/recepcion-index')
def recepcionIndex():
    return render_template('recepcion-index.html')