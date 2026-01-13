from flask import Blueprint

bp = Blueprint('aset_tetap', __name__, url_prefix='/aset-tetap', template_folder='templates')

from app.aset_tetap import routes
