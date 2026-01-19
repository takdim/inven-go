from flask import Blueprint

bp = Blueprint('merk_aset_tetap', __name__, url_prefix='/merk-aset-tetap')

from app.merk_aset_tetap import routes
