from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.barang import bp
from app.barang.forms import BarangForm
from app.models.barang import Barang
from app.models.kategori import KategoriBarang, MerkBarang
from app.models.user import UserLog
from app import db

@bp.route('/')
@login_required
def index():
    """Halaman daftar semua barang"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    
    query = Barang.query
    
    if search:
        query = query.filter(
            (Barang.kode_barang.like(f'%{search}%')) |
            (Barang.nama_barang.like(f'%{search}%'))
        )
    
    barang_list = query.order_by(Barang.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    # Hitung stok akhir untuk setiap barang
    barang_dengan_stok = []
    for barang in barang_list.items:
        barang_dengan_stok.append({
            'barang': barang,
            'stok_akhir': barang.get_stok_akhir()
        })
    
    return render_template('barang/index.html',
                         title='Daftar Barang',
                         barang_list=barang_dengan_stok,
                         pagination=barang_list,
                         search=search)

@bp.route('/tambah', methods=['GET', 'POST'])
@login_required
def tambah():
    """Halaman tambah barang baru"""
    form = BarangForm()
    
    # Populate kategori dan merk choices
    form.kategori_id.choices = [(0, '-- Pilih Kategori --')] + [(k.id, k.nama_kategori) for k in KategoriBarang.query.order_by(KategoriBarang.nama_kategori).all()]
    form.merk_id.choices = [(0, '-- Pilih Merk --')] + [(m.id, m.nama_merk) for m in MerkBarang.query.order_by(MerkBarang.nama_merk).all()]
    
    if form.validate_on_submit():
        barang = Barang(
            kode_barang=form.kode_barang.data,
            nama_barang=form.nama_barang.data,
            jenis_barang=form.jenis_barang.data,
            kategori_id=form.kategori_id.data if form.kategori_id.data != 0 else None,
            merk_id=form.merk_id.data if form.merk_id.data != 0 else None,
            spesifikasi=form.spesifikasi.data,
            satuan=form.satuan.data,
            satuan_kecil=form.satuan_kecil.data if form.satuan_kecil.data else None,
            stok_awal=form.stok_awal.data,
            stok_minimum=form.stok_minimum.data if form.stok_minimum.data else 0
        )
        
        db.session.add(barang)
        db.session.commit()
        
        # Log aktivitas
        UserLog.log_activity(
            user_id=current_user.id,
            activity='Tambah Barang',
            description=f'Menambahkan barang: {barang.kode_barang} - {barang.nama_barang}',
            ip_address=request.remote_addr
        )
        
        flash(f'Barang {barang.nama_barang} berhasil ditambahkan!', 'success')
        return redirect(url_for('barang.index'))
    
    return render_template('barang/form.html',
                         title='Tambah Barang',
                         form=form,
                         action='Tambah')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    """Halaman edit barang"""
    barang = Barang.query.get_or_404(id)
    form = BarangForm(original_kode=barang.kode_barang, obj=barang)
    
    # Populate kategori dan merk choices
    form.kategori_id.choices = [(0, '-- Pilih Kategori --')] + [(k.id, k.nama_kategori) for k in KategoriBarang.query.order_by(KategoriBarang.nama_kategori).all()]
    form.merk_id.choices = [(0, '-- Pilih Merk --')] + [(m.id, m.nama_merk) for m in MerkBarang.query.order_by(MerkBarang.nama_merk).all()]
    
    if form.validate_on_submit():
        barang.kode_barang = form.kode_barang.data
        barang.nama_barang = form.nama_barang.data
        barang.jenis_barang = form.jenis_barang.data
        barang.kategori_id = form.kategori_id.data if form.kategori_id.data != 0 else None
        barang.merk_id = form.merk_id.data if form.merk_id.data != 0 else None
        barang.spesifikasi = form.spesifikasi.data
        barang.satuan = form.satuan.data
        barang.satuan_kecil = form.satuan_kecil.data if form.satuan_kecil.data else None
        barang.stok_awal = form.stok_awal.data
        barang.stok_minimum = form.stok_minimum.data if form.stok_minimum.data else 0
        
        db.session.commit()
        
        # Log aktivitas
        UserLog.log_activity(
            user_id=current_user.id,
            activity='Edit Barang',
            description=f'Mengedit barang: {barang.kode_barang} - {barang.nama_barang}',
            ip_address=request.remote_addr
        )
        
        flash(f'Barang {barang.nama_barang} berhasil diupdate!', 'success')
        return redirect(url_for('barang.index'))
    
    return render_template('barang/form.html',
                         title='Edit Barang',
                         form=form,
                         action='Edit',
                         barang=barang)

@bp.route('/hapus/<int:id>', methods=['POST'])
@login_required
def hapus(id):
    """Hapus barang"""
    barang = Barang.query.get_or_404(id)
    
    nama_barang = barang.nama_barang
    kode_barang = barang.kode_barang
    
    db.session.delete(barang)
    db.session.commit()
    
    # Log aktivitas
    UserLog.log_activity(
        user_id=current_user.id,
        activity='Hapus Barang',
        description=f'Menghapus barang: {kode_barang} - {nama_barang}',
        ip_address=request.remote_addr
    )
    
    flash(f'Barang {nama_barang} berhasil dihapus!', 'success')
    return redirect(url_for('barang.index'))

@bp.route('/detail/<int:id>')
@login_required
def detail(id):
    """Halaman detail barang"""
    from app.models.barang import BarangMasuk, BarangKeluar
    
    barang = Barang.query.get_or_404(id)
    stok_akhir = barang.get_stok_akhir()
    
    # Ambil transaksi terkait
    transaksi_masuk = barang.barang_masuk.order_by(BarangMasuk.created_at.desc()).limit(10).all()
    transaksi_keluar = barang.barang_keluar.order_by(BarangKeluar.created_at.desc()).limit(10).all()
    
    return render_template('barang/detail.html',
                         title=f'Detail {barang.nama_barang}',
                         barang=barang,
                         stok_akhir=stok_akhir,
                         transaksi_masuk=transaksi_masuk,
                         transaksi_keluar=transaksi_keluar)
