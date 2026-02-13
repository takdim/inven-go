from flask import render_template, request, redirect, url_for, flash, send_file, current_app
from flask_login import login_required, current_user
from app.aset_tetap import bp
from app.aset_tetap.forms import AsetTetapForm, LaporanKerusakanForm
from app.models.aset_tetap import AsetTetap
from app.models.laporan_kerusakan import LaporanKerusakan
from app.models.kategori import KategoriBarang, MerkBarang
from app.models.merk_aset_tetap import MerkAsetTetap
from app.models.barang import Barang
from app.utils.pdf_export import export_laporan_kerusakan_to_pdf
from app import db
from datetime import datetime
import os


def _resolve_unhas_logo_path():
    """Resolve logo path for PDF letterhead with flexible fallback candidates."""
    configured_path = current_app.config.get('UNHAS_LOGO_PATH')
    candidates = []

    if configured_path:
        if os.path.isabs(configured_path):
            candidates.append(configured_path)
        else:
            candidates.append(os.path.join(current_app.root_path, configured_path))

    images_dir = os.path.join(current_app.root_path, 'static', 'images')
    candidates.extend([
        os.path.join(images_dir, 'logo_unhas.png'),
        os.path.join(images_dir, 'logo_unhas.jpg'),
        os.path.join(images_dir, 'logo_unhas.jpeg'),
        os.path.join(images_dir, 'logo_institusi.png'),
        os.path.join(images_dir, 'logo_institusi.jpg'),
        os.path.join(images_dir, 'logo_institusi.jpeg'),
    ])

    for path in candidates:
        if path and os.path.exists(path):
            return path

    return None


@bp.route('/')
@login_required
def index():
    """Halaman daftar aset tetap"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    
    # Hitung total barang
    total_barang = Barang.query.count()
    
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
                         search=search,
                         total_barang=total_barang)

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
            nama_pengguna=form.nama_pengguna.data,
            total_barang=form.total_barang.data if form.total_barang.data else 0
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
        aset.total_barang = form.total_barang.data if form.total_barang.data else 0
        
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


@bp.route('/<int:aset_id>/laporan-kerusakan')
@login_required
def laporan_kerusakan_list(aset_id):
    """Daftar laporan kerusakan per aset"""
    aset = AsetTetap.query.get_or_404(aset_id)
    laporan_list = LaporanKerusakan.query.filter_by(
        aset_tetap_id=aset.id
    ).order_by(LaporanKerusakan.created_at.desc()).all()

    return render_template(
        'aset_tetap/laporan_kerusakan_list.html',
        title='Laporan Kerusakan',
        aset=aset,
        laporan_list=laporan_list
    )


@bp.route('/<int:aset_id>/laporan-kerusakan/tambah', methods=['GET', 'POST'])
@login_required
def laporan_kerusakan_tambah(aset_id):
    """Tambah laporan kerusakan untuk aset"""
    aset = AsetTetap.query.get_or_404(aset_id)
    form = LaporanKerusakanForm()

    if request.method == 'GET':
        form.nama_pengguna.data = aset.nama_pengguna or ''
        form.lokasi.data = aset.tempat_penggunaan or ''
        if not form.jumlah.data:
            form.jumlah.data = 1

    if form.validate_on_submit():
        laporan = LaporanKerusakan(
            aset_tetap_id=aset.id,
            pelapor_id=current_user.id if current_user.is_authenticated else None,
            tanggal_diketahui_rusak=form.tanggal_diketahui_rusak.data,
            nama_pengguna=form.nama_pengguna.data,
            lokasi=form.lokasi.data,
            jumlah=form.jumlah.data,
            jenis_kerusakan=form.jenis_kerusakan.data,
            penyebab=form.penyebab.data,
            tindakan=form.tindakan.data,
            kondisi_saat_ini=form.kondisi_saat_ini.data,
            dampak=form.dampak.data,
            status=form.status.data
        )
        db.session.add(laporan)
        db.session.commit()

        flash('Laporan kerusakan berhasil disimpan!', 'success')
        return redirect(url_for('aset_tetap.laporan_kerusakan_list', aset_id=aset.id))

    return render_template(
        'aset_tetap/laporan_kerusakan_form.html',
        title='Tambah Laporan Kerusakan',
        aset=aset,
        form=form
    )


@bp.route('/laporan-kerusakan/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def laporan_kerusakan_edit(id):
    """Edit laporan kerusakan"""
    laporan = LaporanKerusakan.query.get_or_404(id)
    aset = laporan.aset_tetap
    form = LaporanKerusakanForm(obj=laporan)

    if form.validate_on_submit():
        laporan.tanggal_diketahui_rusak = form.tanggal_diketahui_rusak.data
        laporan.nama_pengguna = form.nama_pengguna.data
        laporan.lokasi = form.lokasi.data
        laporan.jumlah = form.jumlah.data
        laporan.jenis_kerusakan = form.jenis_kerusakan.data
        laporan.penyebab = form.penyebab.data
        laporan.tindakan = form.tindakan.data
        laporan.kondisi_saat_ini = form.kondisi_saat_ini.data
        laporan.dampak = form.dampak.data
        laporan.status = form.status.data
        db.session.commit()

        flash('Laporan kerusakan berhasil diperbarui!', 'success')
        return redirect(url_for('aset_tetap.laporan_kerusakan_list', aset_id=aset.id))

    return render_template(
        'aset_tetap/laporan_kerusakan_form.html',
        title='Edit Laporan Kerusakan',
        aset=aset,
        form=form,
        laporan=laporan
    )


@bp.route('/laporan-kerusakan/<int:id>/cetak-pdf')
@login_required
def laporan_kerusakan_cetak_pdf(id):
    """Cetak laporan kerusakan ke PDF"""
    laporan = LaporanKerusakan.query.get_or_404(id)
    logo_path = _resolve_unhas_logo_path()
    if not logo_path:
        current_app.logger.warning(
            'Logo UNHAS tidak ditemukan. PDF dicetak tanpa logo. '
            'Atur UNHAS_LOGO_PATH atau simpan file di app/static/images/logo_unhas.png'
        )

    buffer = export_laporan_kerusakan_to_pdf(laporan, logo_path=logo_path)
    filename = (
        f"Surat_Laporan_Kerusakan_v2_{laporan.aset_tetap.kode_aset}_"
        f"{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.pdf"
    )

    response = send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=filename
    )
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response
