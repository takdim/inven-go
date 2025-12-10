from flask import Blueprint

bp = Blueprint('merk', __name__, url_prefix='/merk')

from app.merk import routes
