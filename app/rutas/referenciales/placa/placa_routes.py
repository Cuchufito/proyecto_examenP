from flask import Blueprint, render_template

placamod = Blueprint('placa', __name__, template_folder='templates')

@placamod.route('/placa-index')
def placaIndex():
    return render_template('placa-index.html')  