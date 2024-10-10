from flask import Blueprint, render_template

servimod = Blueprint('servicios', __name__, template_folder='templates')

@servimod.route('/servicio-index')
def servicioIndex():
    return render_template('servicio-index.html')