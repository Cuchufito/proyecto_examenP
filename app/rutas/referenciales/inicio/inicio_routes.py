from flask import Blueprint, render_template

inimod = Blueprint('inicio', __name__, template_folder='templates')

@inimod.route('/inicio-index')
def inicioIndex():
    return render_template('inicio-index.html')



