from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.aset_tetap import bp
from app.aset_tetap.forms import AsetTetapForm
from app.models.aset_tetap import AsetTetap
from app.models.kategori import KategoriBarang, MerkBarang
from app.models.merk_aset_tetap import MerkAsetTetap
from app import db

@bp.route('/')
@login_required
def index():
    """Halaman daftar aset tetap"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    
    query = AsetTetap.query
    
    if search:
        query = query.filter(
            (AsetTetap.kode_aset.like(f'%{search}%')) |
            (AsetTetap.nama_aset.like(f'%{search}%'))
        )
    
    pagination = query.order_by(AsetTetap.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    aset_list = pagination.items
    
    return render_template('aset_tetap/index.html',
                         title='Daftar Aset Tetap',
                         aset_list=aset_list,
                         pagination=pagination,
                         search=search)

@bp.route('/tambah', methods=['GET', 'POST'])
@login_required
def tambah():
    """Tambah aset tetap baru"""
    form = AsetTetapForm()
    
    # Populate kategori choices
    form.kategori_id.choices = [(0, '-- Pilih Kategori --')] + [(k.id, k.nama_kategori) for k in KategoriBarang.query.order_by(KategoriBarang.nama_kategori).all()]
    
    # Populate merk_aset_tetap choices
    form.merk_aset_tetap_id.choices = [(0, '-- Pilih Merk --')] + [(m.id, f'{m.nama_merk} ({m.tipe})') for m in MerkAsetTetap.query.order_by(MerkAsetTetap.nama_merk).all()]
    
    # Populate kontrak_spk choices from MerkAsetTetap
    form.kontrak_spk.choices = [('', '-- Pilih Kontrak/SPK --')] + [(m.nomor_kontrak, f'{m.nomor_kontrak} ({m.nama_merk} - {m.tipe})') for m in MerkAsetTetap.query.filter(MerkAsetTetap.nomor_kontrak.isnot(None)).order_by(MerkAsetTetap.nomor_kontrak).all()]
    
    if form.validate_on_submit():
        # Check if kode_aset already exists
        if AsetTetap.query.filter_by(kode_aset=form.kode_aset.data).first():
            flash('Kode aset sudah digunakan!', 'danger')
            return redirect(url_for('aset_tetap.tambah'))
        
        aset = AsetTetap(
            kode_aset=form.kode_aset.data,
            nama_aset=form.nama_aset.data,
            kategori_id=form.kategori_id.data if form.kategori_id.data != 0 else None,
            merk_aset_tetap_id=form.merk_aset_tetap_id.data if form.merk_aset_tetap_id.data != 0 else None,
            tanggal_kontrak=form.tanggal_kontrak.data,
            kontrak_spk=form.kontrak_spk.data,
            tempat_penggunaan=form.tempat_penggunaan.data,
            nama_pengguna=form.nama_pengguna.data
        )
        
        db.session.add(aset)
        db.session.commit()
        
        flash('Aset tetap berhasil ditambahkan!', 'success')
        return redirect(url_for('aset_tetap.index'))
    
    return render_template('aset_tetap/form.html',
                         title='Tambah Aset Tetap',
                         form=form)

@bp.route('/<int:id>')
@login_required
def detail(id):
    """Detail aset tetap"""
    aset = AsetTetap.query.get_or_404(id)
    return render_template('aset_tetap/detail.html',
                         title='Detail Aset Tetap',
                         aset=aset)

@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    """Edit aset tetap"""
    aset = AsetTetap.query.get_or_404(id)
    form = AsetTetapForm(obj=aset, original_kode=aset.kode_aset)
    
    # Populate kategori choices
    form.kategori_id.choices = [(0, '-- Pilih Kategori --')] + [(k.id, k.nama_kategori) for k in KategoriBarang.query.order_by(KategoriBarang.nama_kategori).all()]
    
    # Populate merk_aset_tetap choices
    form.merk_aset_tetap_id.choices = [(0, '-- Pilih Merk --')] + [(m.id, f'{m.nama_merk} ({m.tipe})') for m in MerkAsetTetap.query.order_by(MerkAsetTetap.nama_merk).all()]
    
    # Populate kontrak_spk choices from MerkAsetTetap
    form.kontrak_spk.choices = [('', '-- Pilih Kontrak/SPK --')] + [(m.nomor_kontrak, f'{m.nomor_kontrak} ({m.nama_merk} - {m.tipe})') for m in MerkAsetTetap.query.filter(MerkAsetTetap.nomor_kontrak.isnot(None)).order_by(MerkAsetTetap.nomor_kontrak).all()]
    
    if form.validate_on_submit():
        aset.kode_aset = form.kode_aset.data
        aset.nama_aset = form.nama_aset.data
        aset.kategori_id = form.kategori_id.data if form.kategori_id.data != 0 else None
        aset.merk_aset_tetap_id = form.merk_aset_tetap_id.data if form.merk_aset_tetap_id.data != 0 else None
        aset.tanggal_kontrak = form.tanggal_kontrak.data
        aset.kontrak_spk = form.kontrak_spk.data
        aset.tempat_penggunaan = form.tempat_penggunaan.data
        aset.nama_pengguna = form.nama_pengguna.data
        
        db.session.commit()
        
        flash('Aset tetap berhasil diperbarui!', 'success')
        return redirect(url_for('aset_tetap.index'))
    
    return render_template('aset_tetap/form.html',
                         title='Edit Aset Tetap',
                         form=form,
                         aset=aset)

@bp.route('/<int:id>/hapus', methods=['POST'])
@login_required
def hapus(id):
    """Hapus aset tetap"""
    aset = AsetTetap.query.get_or_404(id)
    
    db.session.delete(aset)
    db.session.commit()
    
    flash('Aset tetap berhasil dihapus!', 'success')
    return redirect(url_for('aset_tetap.index'))
