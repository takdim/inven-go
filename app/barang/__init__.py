from flask import Blueprint

bp = Blueprint('barang', __name__, url_prefix='/barang')

from app.barang import routes
