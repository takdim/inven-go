from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.merk import bp
from app.models.kategori import MerkBarang
from app.merk.forms import MerkForm
from app import db

@bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    
    query = MerkBarang.query
    
    if search:
        query = query.filter(
            MerkBarang.nama_merk.like(f'%{search}%')
        )
    
    pagination = query.order_by(MerkBarang.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    merk_list = pagination.items
    
    return render_template('merk/index.html',
                         title='Data Merk dan Tipe Barang',
                         merk_list=merk_list,
                         pagination=pagination,
                         search=search)

@bp.route('/tambah', methods=['GET', 'POST'])
@login_required
def tambah():
    form = MerkForm()
    
    if form.validate_on_submit():
        merk = MerkBarang(
            nama_merk=form.nama_merk.data,
            tanggal_pengadaan=form.tanggal_pengadaan.data,
            spesifikasi=form.spesifikasi.data
        )
        
        db.session.add(merk)
        db.session.commit()
        
        flash('Merk dan Tipe berhasil ditambahkan!', 'success')
        return redirect(url_for('merk.index'))
    
    return render_template('merk/form.html',
                         title='Tambah Merk dan Tipe',
                         form=form)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    merk = MerkBarang.query.get_or_404(id)
    form = MerkForm(obj=merk)
    
    if form.validate_on_submit():
        merk.nama_merk = form.nama_merk.data
        merk.tanggal_pengadaan = form.tanggal_pengadaan.data
        merk.spesifikasi = form.spesifikasi.data
        
        db.session.commit()
        
        flash('Merk dan Tipe berhasil diupdate!', 'success')
        return redirect(url_for('merk.index'))
    
    return render_template('merk/form.html',
                         title='Edit Merk dan Tipe',
                         form=form,
                         merk=merk)

@bp.route('/hapus/<int:id>', methods=['POST'])
@login_required
def hapus(id):
    merk = MerkBarang.query.get_or_404(id)
    
    # Cek apakah merk digunakan oleh barang
    if merk.barang.count() > 0:
        flash('Merk dan Tipe tidak dapat dihapus karena masih digunakan oleh barang!', 'danger')
        return redirect(url_for('merk.index'))
    
    db.session.delete(merk)
    db.session.commit()
    
    flash('Merk dan Tipe berhasil dihapus!', 'success')
    return redirect(url_for('merk.index'))


@bp.route('/detail/<int:id>')
@login_required
def detail(id):
    merk = MerkBarang.query.get_or_404(id)

    from app.models.barang import Barang

    barang_total = merk.barang.count()
    barang_list = (
        merk.barang.order_by(Barang.created_at.desc()).limit(20).all()
        if barang_total > 0
        else []
    )

    return render_template(
        'merk/detail.html',
        title=f'Detail Merk {merk.nama_merk}',
        merk=merk,
        barang_total=barang_total,
        barang_list=barang_list,
    )
