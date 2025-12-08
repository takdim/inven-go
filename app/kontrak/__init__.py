from flask import Blueprint

bp = Blueprint('kontrak', __name__, url_prefix='/kontrak')

from app.kontrak import routes
