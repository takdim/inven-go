from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.aset_tetap import bp
from app.aset_tetap.forms import AsetTetapForm
from app.models.aset_tetap import AsetTetap
from app.models.kategori import KategoriBarang, MerkBarang
from app.models.user import UserLog
from app import db

@bp.route('/')
@login_required
def index():
    """Halaman daftar semua aset tetap"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    
    query = AsetTetap.query
    
    if search:
        query = query.filter(
            (AsetTetap.kode_aset.like(f'%{search}%')) |
            (AsetTetap.nama_aset.like(f'%{search}%'))
        )
    
    aset_list = query.order_by(AsetTetap.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    # Hitung stok akhir untuk setiap aset
    aset_dengan_stok = []
    for aset in aset_list.items:
        aset_dengan_stok.append({
            'aset': aset,
            'stok_akhir': aset.get_stok_akhir()
        })
    
    return render_template('aset_tetap/index.html',
                         title='Daftar Aset Tetap',
                         aset_list=aset_dengan_stok,
                         pagination=aset_list,
                         search=search)

@bp.route('/tambah', methods=['GET', 'POST'])
@login_required
def tambah():
    """Halaman tambah aset tetap baru"""
    form = AsetTetapForm()
    
    # Populate kategori dan merk choices
    form.kategori_id.choices = [(0, '-- Pilih Kategori --')] + [(k.id, k.nama_kategori) for k in KategoriBarang.query.order_by(KategoriBarang.nama_kategori).all()]
    form.merk_id.choices = [(0, '-- Pilih Merk --')] + [(m.id, m.nama_merk) for m in MerkBarang.query.order_by(MerkBarang.nama_merk).all()]
    
    if form.validate_on_submit():
        aset = AsetTetap(
            kode_aset=form.kode_aset.data,
            nama_aset=form.nama_aset.data,
            kategori_id=form.kategori_id.data if form.kategori_id.data != 0 else None,
            merk_id=form.merk_id.data if form.merk_id.data != 0 else None,
            spesifikasi=form.spesifikasi.data,
            satuan=form.satuan.data,
            satuan_kecil=form.satuan_kecil.data if form.satuan_kecil.data else None,
            stok_awal=0,
            stok_minimum=0,
            nomor_kontrak=form.nomor_kontrak.data if form.nomor_kontrak.data else None,
            tanggal_kontrak=form.tanggal_kontrak.data if form.tanggal_kontrak.data else None
        )
        
        db.session.add(aset)
        db.session.commit()
        
        # Log aktivitas
        UserLog.log_activity(
            user_id=current_user.id,
            activity='Tambah Aset Tetap',
            description=f'Menambahkan aset tetap: {aset.kode_aset} - {aset.nama_aset}',
            ip_address=request.remote_addr
        )
        
        flash(f'Aset Tetap {aset.nama_aset} berhasil ditambahkan!', 'success')
        return redirect(url_for('aset_tetap.index'))
    
    return render_template('aset_tetap/form.html',
                         title='Tambah Aset Tetap',
                         form=form,
                         action='Tambah')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    """Halaman edit aset tetap"""
    aset = AsetTetap.query.get_or_404(id)
    form = AsetTetapForm(original_kode=aset.kode_aset, obj=aset)
    
    # Populate kategori dan merk choices
    form.kategori_id.choices = [(0, '-- Pilih Kategori --')] + [(k.id, k.nama_kategori) for k in KategoriBarang.query.order_by(KategoriBarang.nama_kategori).all()]
    form.merk_id.choices = [(0, '-- Pilih Merk --')] + [(m.id, m.nama_merk) for m in MerkBarang.query.order_by(MerkBarang.nama_merk).all()]
    
    if form.validate_on_submit():
        aset.kode_aset = form.kode_aset.data
        aset.nama_aset = form.nama_aset.data
        aset.kategori_id = form.kategori_id.data if form.kategori_id.data != 0 else None
        aset.merk_id = form.merk_id.data if form.merk_id.data != 0 else None
        aset.spesifikasi = form.spesifikasi.data
        aset.satuan = form.satuan.data
        aset.satuan_kecil = form.satuan_kecil.data if form.satuan_kecil.data else None
        aset.nomor_kontrak = form.nomor_kontrak.data if form.nomor_kontrak.data else None
        aset.tanggal_kontrak = form.tanggal_kontrak.data if form.tanggal_kontrak.data else None
        
        db.session.commit()
        
        # Log aktivitas
        UserLog.log_activity(
            user_id=current_user.id,
            activity='Edit Aset Tetap',
            description=f'Mengedit aset tetap: {aset.kode_aset} - {aset.nama_aset}',
            ip_address=request.remote_addr
        )
        
        flash(f'Aset Tetap {aset.nama_aset} berhasil diupdate!', 'success')
        return redirect(url_for('aset_tetap.index'))
    
    return render_template('aset_tetap/form.html',
                         title='Edit Aset Tetap',
                         form=form,
                         action='Edit',
                         aset=aset)

@bp.route('/detail/<int:id>')
@login_required
def detail(id):
    """Halaman detail aset tetap"""
    aset = AsetTetap.query.get_or_404(id)
    
    return render_template('aset_tetap/detail.html',
                         title='Detail Aset Tetap',
                         aset=aset,
                         stok_akhir=aset.get_stok_akhir())

@bp.route('/hapus/<int:id>', methods=['POST'])
@login_required
def hapus(id):
    """Hapus aset tetap"""
    aset = AsetTetap.query.get_or_404(id)
    
    nama_aset = aset.nama_aset
    kode_aset = aset.kode_aset
    
    db.session.delete(aset)
    db.session.commit()
    
    # Log aktivitas
    UserLog.log_activity(
        user_id=current_user.id,
        activity='Hapus Aset Tetap',
        description=f'Menghapus aset tetap: {kode_aset} - {nama_aset}',
        ip_address=request.remote_addr
    )
    
    flash(f'Aset Tetap {nama_aset} berhasil dihapus!', 'success')
    return redirect(url_for('aset_tetap.index'))
