from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.kategori import bp
from app.models.kategori import KategoriBarang
from app.kategori.forms import KategoriForm
from app import db

@bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    
    query = KategoriBarang.query
    
    if search:
        query = query.filter(KategoriBarang.nama_kategori.like(f'%{search}%'))
    
    pagination = query.order_by(KategoriBarang.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    kategori_list = pagination.items
    
    return render_template('kategori/index.html',
                         title='Data Kategori Barang',
                         kategori_list=kategori_list,
                         pagination=pagination,
                         search=search)

@bp.route('/tambah', methods=['GET', 'POST'])
@login_required
def tambah():
    form = KategoriForm()
    
    if form.validate_on_submit():
        kategori = KategoriBarang(
            nama_kategori=form.nama_kategori.data,
            deskripsi=form.deskripsi.data
        )
        
        db.session.add(kategori)
        db.session.commit()
        
        flash('Kategori berhasil ditambahkan!', 'success')
        return redirect(url_for('kategori.index'))
    
    return render_template('kategori/form.html',
                         title='Tambah Kategori',
                         form=form)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    kategori = KategoriBarang.query.get_or_404(id)
    form = KategoriForm(obj=kategori)
    
    if form.validate_on_submit():
        kategori.nama_kategori = form.nama_kategori.data
        kategori.deskripsi = form.deskripsi.data
        
        db.session.commit()
        
        flash('Kategori berhasil diupdate!', 'success')
        return redirect(url_for('kategori.index'))
    
    return render_template('kategori/form.html',
                         title='Edit Kategori',
                         form=form,
                         kategori=kategori)

@bp.route('/hapus/<int:id>', methods=['POST'])
@login_required
def hapus(id):
    kategori = KategoriBarang.query.get_or_404(id)
    
    # Cek apakah kategori digunakan oleh barang
    if kategori.barang.count() > 0:
        flash('Kategori tidak dapat dihapus karena masih digunakan oleh barang!', 'danger')
        return redirect(url_for('kategori.index'))
    
    db.session.delete(kategori)
    db.session.commit()
    
    flash('Kategori berhasil dihapus!', 'success')
    return redirect(url_for('kategori.index'))
