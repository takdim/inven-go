from flask import Blueprint

bp = Blueprint('kategori', __name__, url_prefix='/kategori')

from app.kategori import routes
