from flask import render_template, redirect, url_for, flash, request, send_file
from flask_login import login_required
from app.merk_aset_tetap import bp
from app.models.merk_aset_tetap import MerkAsetTetap
from app.merk_aset_tetap.forms import MerkAsetTetapForm
from app.utils.pdf_export import export_merk_aset_tetap_to_pdf
from app import db
from datetime import datetime
from sqlalchemy import func

@bp.route('/')
@login_required
def index():
    """Halaman daftar merk aset tetap"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    
    query = MerkAsetTetap.query
    
    if search:
        query = query.filter(
            MerkAsetTetap.nama_merk.like(f'%{search}%')
        )
    
    pagination = query.order_by(MerkAsetTetap.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    merk_list = pagination.items
    
    return render_template('merk_aset_tetap/index.html',
                         title='Data Merk Aset Tetap',
                         merk_list=merk_list,
                         pagination=pagination,
                         search=search)

@bp.route('/tambah', methods=['GET', 'POST'])
@login_required
def tambah():
    """Tambah merk aset tetap baru"""
    form = MerkAsetTetapForm()
    
    if form.validate_on_submit():
        merk = MerkAsetTetap(
            nama_merk=form.nama_merk.data,
            tipe=form.tipe.data,
            tanggal_pengadaan=form.tanggal_pengadaan.data,
            nomor_kontrak=form.nomor_kontrak.data,
            spesifikasi=form.spesifikasi.data
        )
        
        db.session.add(merk)
        db.session.commit()
        
        flash('Merk Aset Tetap berhasil ditambahkan!', 'success')
        return redirect(url_for('merk_aset_tetap.index'))
    
    return render_template('merk_aset_tetap/form.html',
                         title='Tambah Merk Aset Tetap',
                         form=form)

@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    """Edit merk aset tetap"""
    merk = MerkAsetTetap.query.get_or_404(id)
    form = MerkAsetTetapForm()
    form.edit_id = id
    
    if form.validate_on_submit():
        merk.nama_merk = form.nama_merk.data
        merk.tipe = form.tipe.data
        merk.tanggal_pengadaan = form.tanggal_pengadaan.data
        merk.nomor_kontrak = form.nomor_kontrak.data
        merk.spesifikasi = form.spesifikasi.data
        
        db.session.commit()
        
        flash('Merk Aset Tetap berhasil diupdate!', 'success')
        return redirect(url_for('merk_aset_tetap.index'))
    
    elif request.method == 'GET':
        form.nama_merk.data = merk.nama_merk
        form.tipe.data = merk.tipe
        form.tanggal_pengadaan.data = merk.tanggal_pengadaan
        form.nomor_kontrak.data = merk.nomor_kontrak
        form.spesifikasi.data = merk.spesifikasi
    
    return render_template('merk_aset_tetap/form.html',
                         title='Edit Merk Aset Tetap',
                         form=form,
                         merk=merk)

@bp.route('/<int:id>/hapus', methods=['POST'])
@login_required
def hapus(id):
    """Hapus merk aset tetap"""
    merk = MerkAsetTetap.query.get_or_404(id)
    
    # Cek apakah merk digunakan oleh aset
    if merk.get_total_aset() > 0:
        flash(f'Merk Aset Tetap tidak dapat dihapus karena masih digunakan oleh {merk.get_total_aset()} aset!', 'danger')
        return redirect(url_for('merk_aset_tetap.index'))
    
    db.session.delete(merk)
    db.session.commit()
    
    flash('Merk Aset Tetap berhasil dihapus!', 'success')
    return redirect(url_for('merk_aset_tetap.index'))


@bp.route('/detail/<int:id>')
@login_required
def detail(id):
    merk = MerkAsetTetap.query.get_or_404(id)

    from app.models.aset_tetap import AsetTetap

    aset_query = AsetTetap.query.filter_by(merk_aset_tetap_id=merk.id)
    aset_total = aset_query.count()

    total_barang_all = (
        db.session.query(func.sum(AsetTetap.total_barang))
        .filter_by(merk_aset_tetap_id=merk.id)
        .scalar()
        or 0
    )

    total_barang_by_criteria = merk.get_total_aset_by_criteria()

    aset_list = (
        aset_query.order_by(AsetTetap.created_at.desc()).limit(20).all()
        if aset_total > 0
        else []
    )

    return render_template(
        'merk_aset_tetap/detail.html',
        title=f'Detail Merk Aset Tetap {merk.nama_merk}',
        merk=merk,
        aset_total=aset_total,
        total_barang_all=total_barang_all,
        total_barang_by_criteria=total_barang_by_criteria,
        aset_list=aset_list,
    )


@bp.route('/cetak-laporan')
@login_required
def cetak_laporan():
    """Cetak laporan daftar merk aset tetap ke PDF"""
    search = request.args.get('search', '', type=str)
    
    query = MerkAsetTetap.query
    
    if search:
        query = query.filter(
            MerkAsetTetap.nama_merk.like(f'%{search}%')
        )
    
    merk_list = query.order_by(MerkAsetTetap.created_at.desc()).all()
    
    # Generate PDF
    pdf_data = export_merk_aset_tetap_to_pdf(merk_list)
    
    return send_file(
        pdf_data,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'Laporan_Merk_Aset_Tetap_{datetime.now().strftime("%d%m%Y_%H%M%S")}.pdf'
    )
