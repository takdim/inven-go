from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.kontrak import bp
from app.kontrak.forms import KontrakForm, BarangKontrakForm
from app.models.kontrak import KontrakBarang, BarangKontrak
from app.models.barang import Barang
from app.models.user import UserLog
from app import db

@bp.route('/')
@login_required
def index():
    """Halaman daftar semua kontrak"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    
    query = KontrakBarang.query
    
    if search:
        query = query.filter(
            (KontrakBarang.nomor_kontrak.like(f'%{search}%')) |
            (KontrakBarang.deskripsi.like(f'%{search}%'))
        )
    
    kontrak_list = query.order_by(KontrakBarang.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('kontrak/index.html',
                         title='Daftar Kontrak/SPK',
                         kontrak_list=kontrak_list,
                         search=search)

@bp.route('/tambah', methods=['GET', 'POST'])
@login_required
def tambah():
    """Halaman tambah kontrak baru"""
    form = KontrakForm()
    
    if form.validate_on_submit():
        kontrak = KontrakBarang(
            nomor_kontrak=form.nomor_kontrak.data,
            tanggal_kontrak=form.tanggal_kontrak.data,
            deskripsi=form.deskripsi.data
        )
        
        db.session.add(kontrak)
        db.session.commit()
        
        # Log aktivitas
        UserLog.log_activity(
            user_id=current_user.id,
            activity='Tambah Kontrak',
            description=f'Menambahkan kontrak: {kontrak.nomor_kontrak}',
            ip_address=request.remote_addr
        )
        
        flash(f'Kontrak {kontrak.nomor_kontrak} berhasil ditambahkan!', 'success')
        return redirect(url_for('kontrak.detail', id=kontrak.id))
    
    return render_template('kontrak/form.html',
                         title='Tambah Kontrak',
                         form=form,
                         action='Tambah')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    """Halaman edit kontrak"""
    kontrak = KontrakBarang.query.get_or_404(id)
    form = KontrakForm(original_nomor=kontrak.nomor_kontrak, obj=kontrak)
    
    if form.validate_on_submit():
        kontrak.nomor_kontrak = form.nomor_kontrak.data
        kontrak.tanggal_kontrak = form.tanggal_kontrak.data
        kontrak.deskripsi = form.deskripsi.data
        
        db.session.commit()
        
        # Log aktivitas
        UserLog.log_activity(
            user_id=current_user.id,
            activity='Edit Kontrak',
            description=f'Mengedit kontrak: {kontrak.nomor_kontrak}',
            ip_address=request.remote_addr
        )
        
        flash(f'Kontrak {kontrak.nomor_kontrak} berhasil diupdate!', 'success')
        return redirect(url_for('kontrak.detail', id=kontrak.id))
    
    return render_template('kontrak/form.html',
                         title='Edit Kontrak',
                         form=form,
                         action='Edit',
                         kontrak=kontrak)

@bp.route('/hapus/<int:id>', methods=['POST'])
@login_required
def hapus(id):
    """Hapus kontrak"""
    kontrak = KontrakBarang.query.get_or_404(id)
    
    nomor_kontrak = kontrak.nomor_kontrak
    
    db.session.delete(kontrak)
    db.session.commit()
    
    # Log aktivitas
    UserLog.log_activity(
        user_id=current_user.id,
        activity='Hapus Kontrak',
        description=f'Menghapus kontrak: {nomor_kontrak}',
        ip_address=request.remote_addr
    )
    
    flash(f'Kontrak {nomor_kontrak} berhasil dihapus!', 'success')
    return redirect(url_for('kontrak.index'))

@bp.route('/detail/<int:id>')
@login_required
def detail(id):
    """Halaman detail kontrak"""
    kontrak = KontrakBarang.query.get_or_404(id)
    
    # Form untuk tambah barang ke kontrak
    form = BarangKontrakForm()
    form.barang_id.choices = [(0, '-- Pilih Barang --')] + [
        (b.id, f'{b.kode_barang} - {b.nama_barang}') 
        for b in Barang.query.order_by(Barang.nama_barang).all()
    ]
    
    return render_template('kontrak/detail.html',
                         title=f'Detail Kontrak {kontrak.nomor_kontrak}',
                         kontrak=kontrak,
                         form=form)

@bp.route('/detail/<int:id>/tambah-barang', methods=['POST'])
@login_required
def tambah_barang(id):
    """Tambah barang ke kontrak"""
    kontrak = KontrakBarang.query.get_or_404(id)
    form = BarangKontrakForm()
    
    # Populate choices
    form.barang_id.choices = [(0, '-- Pilih Barang --')] + [
        (b.id, f'{b.kode_barang} - {b.nama_barang}') 
        for b in Barang.query.order_by(Barang.nama_barang).all()
    ]
    
    if form.validate_on_submit():
        if form.barang_id.data == 0:
            flash('Silakan pilih barang terlebih dahulu!', 'warning')
            return redirect(url_for('kontrak.detail', id=id))
        
        # Cek apakah barang sudah ada di kontrak ini
        existing = BarangKontrak.query.filter_by(
            barang_id=form.barang_id.data,
            kontrak_id=kontrak.id
        ).first()
        
        if existing:
            flash('Barang sudah ada dalam kontrak ini!', 'warning')
            return redirect(url_for('kontrak.detail', id=id))
        
        barang_kontrak = BarangKontrak(
            barang_id=form.barang_id.data,
            kontrak_id=kontrak.id,
            qty_kontrak=form.qty_kontrak.data,
            harga_satuan=form.harga_satuan.data
        )
        
        db.session.add(barang_kontrak)
        db.session.commit()
        
        barang = Barang.query.get(form.barang_id.data)
        
        # Log aktivitas
        UserLog.log_activity(
            user_id=current_user.id,
            activity='Tambah Barang ke Kontrak',
            description=f'Menambah barang {barang.nama_barang} ke kontrak {kontrak.nomor_kontrak}',
            ip_address=request.remote_addr
        )
        
        flash(f'Barang {barang.nama_barang} berhasil ditambahkan ke kontrak!', 'success')
    
    return redirect(url_for('kontrak.detail', id=id))

@bp.route('/detail/<int:kontrak_id>/hapus-barang/<int:barang_kontrak_id>', methods=['POST'])
@login_required
def hapus_barang(kontrak_id, barang_kontrak_id):
    """Hapus barang dari kontrak"""
    barang_kontrak = BarangKontrak.query.get_or_404(barang_kontrak_id)
    
    if barang_kontrak.kontrak_id != kontrak_id:
        flash('Data tidak valid!', 'danger')
        return redirect(url_for('kontrak.index'))
    
    barang_nama = barang_kontrak.barang.nama_barang
    kontrak_nomor = barang_kontrak.kontrak.nomor_kontrak
    
    db.session.delete(barang_kontrak)
    db.session.commit()
    
    # Log aktivitas
    UserLog.log_activity(
        user_id=current_user.id,
        activity='Hapus Barang dari Kontrak',
        description=f'Menghapus barang {barang_nama} dari kontrak {kontrak_nomor}',
        ip_address=request.remote_addr
    )
    
    flash(f'Barang {barang_nama} berhasil dihapus dari kontrak!', 'success')
    return redirect(url_for('kontrak.detail', id=kontrak_id))
