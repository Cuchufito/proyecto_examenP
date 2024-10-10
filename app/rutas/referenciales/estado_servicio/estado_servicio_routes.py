from flask import Blueprint, render_template

estaservimod = Blueprint('estadoservicio', __name__, template_folder='templates')

@estaservimod.route('/estadoservicio-index')
def estadoservicioIndex():
    return render_template('estadoservicio-index.html')