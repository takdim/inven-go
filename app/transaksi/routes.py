from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.transaksi import bp
from app.transaksi.forms import TransaksiForm
from app.models.barang import Barang, BarangMasuk, BarangKeluar
from app.models.user import UserLog
from app import db

@bp.route('/masuk')
@login_required
def masuk():
    """Halaman daftar transaksi barang masuk"""
    page = request.args.get('page', 1, type=int)
    transaksi_list = BarangMasuk.query.order_by(BarangMasuk.tanggal.desc(), BarangMasuk.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('transaksi/masuk_list.html',
                         title='Barang Masuk',
                         transaksi_list=transaksi_list)

@bp.route('/masuk/tambah', methods=['GET', 'POST'])
@login_required
def masuk_tambah():
    """Halaman tambah transaksi barang masuk"""
    form = TransaksiForm()
    
    # Populate dropdown barang
    barang_list = Barang.query.order_by(Barang.nama_barang).all()
    form.kode_barang.choices = [(b.kode_barang, f'{b.kode_barang} - {b.nama_barang}') for b in barang_list]
    
    if form.validate_on_submit():
        transaksi = BarangMasuk(
            tanggal=form.tanggal.data,
            kode_barang=form.kode_barang.data,
            qty=form.qty.data,
            keterangan=form.keterangan.data
        )
        
        db.session.add(transaksi)
        db.session.commit()
        
        # Log aktivitas
        barang = Barang.query.filter_by(kode_barang=form.kode_barang.data).first()
        UserLog.log_activity(
            user_id=current_user.id,
            activity='Barang Masuk',
            description=f'Barang masuk: {barang.nama_barang} (+{form.qty.data})',
            ip_address=request.remote_addr
        )
        
        flash(f'Transaksi barang masuk berhasil ditambahkan!', 'success')
        return redirect(url_for('transaksi.masuk'))
    
    return render_template('transaksi/masuk_form.html',
                         title='Tambah Barang Masuk',
                         form=form)

@bp.route('/masuk/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def masuk_edit(id):
    """Halaman edit transaksi barang masuk"""
    transaksi = BarangMasuk.query.get_or_404(id)
    form = TransaksiForm(obj=transaksi)
    
    # Populate dropdown barang
    barang_list = Barang.query.order_by(Barang.nama_barang).all()
    form.kode_barang.choices = [(b.kode_barang, f'{b.kode_barang} - {b.nama_barang}') for b in barang_list]
    
    if form.validate_on_submit():
        transaksi.tanggal = form.tanggal.data
        transaksi.kode_barang = form.kode_barang.data
        transaksi.qty = form.qty.data
        transaksi.keterangan = form.keterangan.data
        
        db.session.commit()
        
        # Log aktivitas
        barang = Barang.query.filter_by(kode_barang=form.kode_barang.data).first()
        UserLog.log_activity(
            user_id=current_user.id,
            activity='Edit Barang Masuk',
            description=f'Edit barang masuk: {barang.nama_barang}',
            ip_address=request.remote_addr
        )
        
        flash(f'Transaksi barang masuk berhasil diupdate!', 'success')
        return redirect(url_for('transaksi.masuk'))
    
    return render_template('transaksi/masuk_form.html',
                         title='Edit Barang Masuk',
                         form=form,
                         transaksi=transaksi)

@bp.route('/masuk/hapus/<int:id>', methods=['POST'])
@login_required
def masuk_hapus(id):
    """Hapus transaksi barang masuk"""
    transaksi = BarangMasuk.query.get_or_404(id)
    
    barang = transaksi.barang
    qty = transaksi.qty
    
    db.session.delete(transaksi)
    db.session.commit()
    
    # Log aktivitas
    UserLog.log_activity(
        user_id=current_user.id,
        activity='Hapus Barang Masuk',
        description=f'Hapus barang masuk: {barang.nama_barang} ({qty})',
        ip_address=request.remote_addr
    )
    
    flash(f'Transaksi barang masuk berhasil dihapus!', 'success')
    return redirect(url_for('transaksi.masuk'))

# === BARANG KELUAR ===

@bp.route('/keluar')
@login_required
def keluar():
    """Halaman daftar transaksi barang keluar"""
    page = request.args.get('page', 1, type=int)
    transaksi_list = BarangKeluar.query.order_by(BarangKeluar.tanggal.desc(), BarangKeluar.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('transaksi/keluar_list.html',
                         title='Barang Keluar',
                         transaksi_list=transaksi_list)

@bp.route('/keluar/tambah', methods=['GET', 'POST'])
@login_required
def keluar_tambah():
    """Halaman tambah transaksi barang keluar"""
    form = TransaksiForm()
    
    # Populate dropdown barang
    barang_list = Barang.query.order_by(Barang.nama_barang).all()
    form.kode_barang.choices = [(b.kode_barang, f'{b.kode_barang} - {b.nama_barang}') for b in barang_list]
    
    if form.validate_on_submit():
        # Cek stok
        barang = Barang.query.filter_by(kode_barang=form.kode_barang.data).first()
        stok_akhir = barang.get_stok_akhir()
        
        if form.qty.data > stok_akhir:
            flash(f'Stok tidak cukup! Stok tersedia: {stok_akhir}', 'danger')
            return render_template('transaksi/keluar_form.html',
                                 title='Tambah Barang Keluar',
                                 form=form)
        
        transaksi = BarangKeluar(
            tanggal=form.tanggal.data,
            kode_barang=form.kode_barang.data,
            qty=form.qty.data,
            keterangan=form.keterangan.data
        )
        
        db.session.add(transaksi)
        db.session.commit()
        
        # Log aktivitas
        UserLog.log_activity(
            user_id=current_user.id,
            activity='Barang Keluar',
            description=f'Barang keluar: {barang.nama_barang} (-{form.qty.data})',
            ip_address=request.remote_addr
        )
        
        flash(f'Transaksi barang keluar berhasil ditambahkan!', 'success')
        return redirect(url_for('transaksi.keluar'))
    
    return render_template('transaksi/keluar_form.html',
                         title='Tambah Barang Keluar',
                         form=form)

@bp.route('/keluar/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def keluar_edit(id):
    """Halaman edit transaksi barang keluar"""
    transaksi = BarangKeluar.query.get_or_404(id)
    form = TransaksiForm(obj=transaksi)
    
    # Populate dropdown barang
    barang_list = Barang.query.order_by(Barang.nama_barang).all()
    form.kode_barang.choices = [(b.kode_barang, f'{b.kode_barang} - {b.nama_barang}') for b in barang_list]
    
    if form.validate_on_submit():
        transaksi.tanggal = form.tanggal.data
        transaksi.kode_barang = form.kode_barang.data
        transaksi.qty = form.qty.data
        transaksi.keterangan = form.keterangan.data
        
        db.session.commit()
        
        # Log aktivitas
        barang = Barang.query.filter_by(kode_barang=form.kode_barang.data).first()
        UserLog.log_activity(
            user_id=current_user.id,
            activity='Edit Barang Keluar',
            description=f'Edit barang keluar: {barang.nama_barang}',
            ip_address=request.remote_addr
        )
        
        flash(f'Transaksi barang keluar berhasil diupdate!', 'success')
        return redirect(url_for('transaksi.keluar'))
    
    return render_template('transaksi/keluar_form.html',
                         title='Edit Barang Keluar',
                         form=form,
                         transaksi=transaksi)

@bp.route('/keluar/hapus/<int:id>', methods=['POST'])
@login_required
def keluar_hapus(id):
    """Hapus transaksi barang keluar"""
    transaksi = BarangKeluar.query.get_or_404(id)
    
    barang = transaksi.barang
    qty = transaksi.qty
    
    db.session.delete(transaksi)
    db.session.commit()
    
    # Log aktivitas
    UserLog.log_activity(
        user_id=current_user.id,
        activity='Hapus Barang Keluar',
        description=f'Hapus barang keluar: {barang.nama_barang} ({qty})',
        ip_address=request.remote_addr
    )
    
    flash(f'Transaksi barang keluar berhasil dihapus!', 'success')
    return redirect(url_for('transaksi.keluar'))
