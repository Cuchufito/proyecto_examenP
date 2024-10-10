from flask import Blueprint, render_template, jsonify
from app.dao.referenciales.proveedor.ProveedorDao import ProveedorDao

provemod = Blueprint('proveedor', __name__, template_folder='templates')

@provemod.route('/proveedor-index')
def proveedorIndex():
    proveedordao = ProveedorDao()
    return render_template('proveedor-index.html', lista_proveedores=proveedordao.getProveedores())
