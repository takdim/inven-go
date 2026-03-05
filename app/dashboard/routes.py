from flask import render_template
from flask_login import login_required, current_user
from app.dashboard import bp
from app.models.barang import Barang, BarangMasuk, BarangKeluar
from app.models.user import User
from app.models.aset_tetap import AsetTetap
from app.models.laporan_kerusakan import LaporanKerusakan
from app.models.permintaan_barang import PermintaanBarang
from app.barang.forms import PermintaanBarangPublicForm
from app import db
from sqlalchemy import func

@bp.route('/')
@login_required
def index():
    # Statistik dashboard
    total_barang = Barang.query.count()
    total_transaksi_masuk = BarangMasuk.query.count()
    total_transaksi_keluar = BarangKeluar.query.count()
    total_aset = AsetTetap.query.count()
    
    # Barang dengan stok rendah (contoh: < 10)
    barang_stok_rendah = []
    for barang in Barang.query.all():
        stok_akhir = barang.get_stok_akhir()
        if stok_akhir < 10:
            barang_stok_rendah.append({
                'barang': barang,
                'stok_akhir': stok_akhir
            })
    
    # Barang habis pakai dengan stok rendah (untuk alert khusus)
    barang_habis_pakai_rendah = []
    for barang in Barang.query.filter_by(jenis_barang='habis_pakai').all():
        stok_akhir = barang.get_stok_akhir()
        if barang.is_stok_rendah(stok_akhir):
            prediksi = barang.prediksi_habis(30)
            barang_habis_pakai_rendah.append({
                'barang': barang,
                'stok_akhir': stok_akhir,
                'status': barang.get_status_stok(stok_akhir),
                'prediksi': prediksi
            })
    
    # Transaksi terbaru
    transaksi_masuk_terbaru = BarangMasuk.query.order_by(BarangMasuk.created_at.desc()).limit(5).all()
    transaksi_keluar_terbaru = BarangKeluar.query.order_by(BarangKeluar.created_at.desc()).limit(5).all()
    
    # Notifikasi Laporan Kerusakan
    laporan_pending = LaporanKerusakan.query.filter_by(status='terkirim').count()
    laporan_terbaru = LaporanKerusakan.query.order_by(LaporanKerusakan.created_at.desc()).limit(10).all()
    
    # Notifikasi Permintaan Barang
    permintaan_pending = PermintaanBarang.query.filter_by(status='terkirim').count()
    permintaan_terbaru = PermintaanBarang.query.order_by(PermintaanBarang.created_at.desc()).limit(10).all()
    
    # Total laporan dalam 7 hari terakhir
    from datetime import datetime, timedelta
    seminggu_lalu = datetime.utcnow() - timedelta(days=7)
    laporan_minggu_ini = LaporanKerusakan.query.filter(
        LaporanKerusakan.created_at >= seminggu_lalu
    ).count()
    
    return render_template('dashboard/index.html',
                         title='Dashboard',
                         total_barang=total_barang,
                         total_transaksi_masuk=total_transaksi_masuk,
                         total_transaksi_keluar=total_transaksi_keluar,
                         total_aset=total_aset,
                         barang_stok_rendah=barang_stok_rendah,
                         barang_habis_pakai_rendah=barang_habis_pakai_rendah,
                         transaksi_masuk_terbaru=transaksi_masuk_terbaru,
                         transaksi_keluar_terbaru=transaksi_keluar_terbaru,
                         laporan_pending=laporan_pending,
                         laporan_terbaru=laporan_terbaru,
                         laporan_minggu_ini=laporan_minggu_ini,
                         permintaan_pending=permintaan_pending,
                         permintaan_terbaru=permintaan_terbaru)

@bp.route('/laporan_kerusakan_monitor')
@login_required
def laporan_kerusakan_monitor():
    """Halaman monitoring laporan kerusakan untuk admin"""
    from flask import abort
    
    # Hanya admin yang bisa akses
    if current_user.role != 'admin':
        abort(403)
    
    # Pagination
    page = 1
    status_filter = 'semua'
    
    try:
        from flask import request
        page = request.args.get('page', 1, type=int)
        status_filter = request.args.get('status', 'semua')
    except:
        pass
    
    # Query dengan filter
    query = LaporanKerusakan.query
    
    if status_filter != 'semua':
        query = query.filter_by(status=status_filter)
    
    # Urutkan berdasarkan tanggal terbaru
    laporan_kerusakan = query.order_by(
        LaporanKerusakan.created_at.desc()
    ).paginate(page=page, per_page=20)
    
    # Statistik
    total_laporan = LaporanKerusakan.query.count()
    laporan_pending = LaporanKerusakan.query.filter_by(status='terkirim').count()
    laporan_selesai = LaporanKerusakan.query.filter_by(status='selesai').count()
    laporan_ditolak = LaporanKerusakan.query.filter_by(status='ditolak').count()
    
    return render_template('dashboard/laporan_kerusakan_monitor.html',
                         title='Monitor Laporan Kerusakan',
                         laporan_kerusakan=laporan_kerusakan,
                         status_filter=status_filter,
                         total_laporan=total_laporan,
                         laporan_pending=laporan_pending,
                         laporan_selesai=laporan_selesai,
                         laporan_ditolak=laporan_ditolak)


@bp.route('/permintaan_barang_monitor')
@login_required
def permintaan_barang_monitor():
    """Halaman monitoring permintaan barang untuk admin"""
    from flask import abort
    
    # Hanya admin yang bisa akses
    if current_user.role != 'admin':
        abort(403)
    
    # Pagination
    page = 1
    status_filter = 'semua'
    
    try:
        from flask import request
        page = request.args.get('page', 1, type=int)
        status_filter = request.args.get('status', 'semua')
    except:
        pass
    
    # Query dengan filter
    query = PermintaanBarang.query
    
    if status_filter != 'semua':
        query = query.filter_by(status=status_filter)
    
    # Urutkan berdasarkan tanggal terbaru
    permintaan_barang = query.order_by(
        PermintaanBarang.created_at.desc()
    ).paginate(page=page, per_page=20)
    
    # Statistik
    total_permintaan = PermintaanBarang.query.count()
    permintaan_pending = PermintaanBarang.query.filter_by(status='terkirim').count()
    permintaan_selesai = PermintaanBarang.query.filter_by(status='selesai').count()
    permintaan_ditolak = PermintaanBarang.query.filter_by(status='ditolak').count()
    
    return render_template('dashboard/permintaan_barang_monitor.html',
                         title='Monitor Permintaan Barang',
                         permintaan_barang=permintaan_barang,
                         status_filter=status_filter,
                         total_permintaan=total_permintaan,
                         permintaan_pending=permintaan_pending,
                         permintaan_selesai=permintaan_selesai,
                         permintaan_ditolak=permintaan_ditolak)


@bp.route('/permintaan_barang_monitor/edit/<int:id>', methods=['GET','POST'])
@login_required
def permintaan_barang_edit(id):
    """Edit permintaan barang ATK"""
    from flask import request, redirect, url_for, flash, abort

    # hanya admin boleh edit
    if current_user.role != 'admin':
        abort(403)

    permintaan = PermintaanBarang.query.get_or_404(id)
    form = PermintaanBarangPublicForm(obj=permintaan)

    # rebuild choice lists
    barang_choices = [(0, '-- Pilih Barang --')] + [
        (b.id, f'{b.kode_barang} - {b.nama_barang} (Stok: {b.get_stok_akhir()})')
        for b in Barang.query.filter_by(kategori_id=3).order_by(Barang.kode_barang).all()
    ]
    form.nama_barang1.choices = barang_choices
    form.nama_barang2.choices = barang_choices
    form.nama_barang3.choices = barang_choices

    if form.validate_on_submit():
        permintaan.nama_pengguna = form.nama_pengguna.data
        permintaan.barang1_id = form.nama_barang1.data
        permintaan.banyaknya1 = form.banyaknya1.data
        permintaan.barang2_id = form.nama_barang2.data or None
        permintaan.banyaknya2 = form.banyaknya2.data or None
        permintaan.barang3_id = form.nama_barang3.data or None
        permintaan.banyaknya3 = form.banyaknya3.data or None
        permintaan.tempat_penggunaan = form.tempat_penggunaan.data
        permintaan.tanggal = form.tanggal.data
        db.session.commit()
        flash('Permintaan barang berhasil diperbarui.', 'success')
        return redirect(url_for('dashboard.permintaan_barang_monitor'))

    return render_template('dashboard/permintaan_barang_edit.html',
                         title='Edit Permintaan Barang',
                         form=form,
                         permintaan=permintaan)


@bp.route('/permintaan_barang_monitor/hapus/<int:id>', methods=['POST'])
@login_required
def permintaan_barang_hapus(id):
    """Hapus permintaan barang dari dashboard monitoring"""
    from flask import request, redirect, url_for, flash, abort

    # hanya admin boleh hapus
    if current_user.role != 'admin':
        abort(403)

    permintaan = PermintaanBarang.query.get_or_404(id)
    db.session.delete(permintaan)
    db.session.commit()

    flash('Permintaan barang berhasil dihapus.', 'success')
    # kembali ke halaman monitor, pertahankan filter/page jika ada
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'semua')
    return redirect(url_for('dashboard.permintaan_barang_monitor', page=page, status=status))


@bp.route('/permintaan_barang_monitor/selesai/<int:id>', methods=['POST'])
@login_required
def permintaan_barang_selesai(id):
    """Tandai permintaan barang selesai"""
    from flask import request, redirect, url_for, flash, abort

    if current_user.role != 'admin':
        abort(403)

    permintaan = PermintaanBarang.query.get_or_404(id)
    permintaan.status = 'selesai'
    db.session.commit()

    flash('Permintaan barang ditandai selesai.', 'success')
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'semua')
    return redirect(url_for('dashboard.permintaan_barang_monitor', page=page, status=status))


@bp.route('/laporan_kerusakan_monitor/hapus/<int:id>', methods=['POST'])
@login_required
def laporan_kerusakan_hapus(id):
    """Hapus laporan kerusakan dari dashboard monitoring"""
    from flask import request, redirect, url_for, flash, abort

    # hanya admin boleh hapus
    if current_user.role != 'admin':
        abort(403)

    laporan = LaporanKerusakan.query.get_or_404(id)
    db.session.delete(laporan)
    db.session.commit()

    flash('Laporan kerusakan berhasil dihapus.', 'success')
    # kembali ke halaman monitor, pertahankan filter/page jika ada
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'semua')
    return redirect(url_for('dashboard.laporan_kerusakan_monitor', page=page, status=status))

