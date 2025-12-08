from flask import Blueprint

bp = Blueprint('transaksi', __name__, url_prefix='/transaksi')

from app.transaksi import routes
