from flask import render_template
from flask_login import login_required, current_user
from app.dashboard import bp
from app.models.barang import Barang, BarangMasuk, BarangKeluar
from app.models.user import User
from app import db
from sqlalchemy import func

@bp.route('/')
@login_required
def index():
    # Statistik dashboard
    total_barang = Barang.query.count()
    total_transaksi_masuk = BarangMasuk.query.count()
    total_transaksi_keluar = BarangKeluar.query.count()
    total_users = User.query.count()
    
    # Barang dengan stok rendah (contoh: < 10)
    barang_stok_rendah = []
    for barang in Barang.query.all():
        stok_akhir = barang.get_stok_akhir()
        if stok_akhir < 10:
            barang_stok_rendah.append({
                'barang': barang,
                'stok_akhir': stok_akhir
            })
    
    # Transaksi terbaru
    transaksi_masuk_terbaru = BarangMasuk.query.order_by(BarangMasuk.created_at.desc()).limit(5).all()
    transaksi_keluar_terbaru = BarangKeluar.query.order_by(BarangKeluar.created_at.desc()).limit(5).all()
    
    return render_template('dashboard/index.html',
                         title='Dashboard',
                         total_barang=total_barang,
                         total_transaksi_masuk=total_transaksi_masuk,
                         total_transaksi_keluar=total_transaksi_keluar,
                         total_users=total_users,
                         barang_stok_rendah=barang_stok_rendah,
                         transaksi_masuk_terbaru=transaksi_masuk_terbaru,
                         transaksi_keluar_terbaru=transaksi_keluar_terbaru)
