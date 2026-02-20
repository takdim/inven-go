from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from datetime import date
from app import db
from app.aset_tetap.forms import LaporanKerusakanPublicForm
from app.models.aset_tetap import AsetTetap
from app.models.laporan_kerusakan import LaporanKerusakan

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/about')
def about():
    return render_template('about.html')


def _build_aset_choices():
    return [(0, '-- Pilih Aset --')] + [
        (a.id, f'{a.kode_aset} - {a.nama_aset}')
        for a in AsetTetap.query.order_by(AsetTetap.kode_aset).all()
    ]


def _build_nama_pengguna_choices():
    """Ambil nama pengguna yang unik dari aset_tetap yang tidak kosong"""
    aset_list = AsetTetap.query.filter(
        AsetTetap.nama_pengguna.isnot(None),
        AsetTetap.nama_pengguna != ''
    ).distinct(AsetTetap.nama_pengguna).all()
    
    nama_list = sorted(list(set([a.nama_pengguna for a in aset_list])))
    return [('', '-- Pilih Nama Pengguna --')] + [(name, name) for name in nama_list]


@bp.route('/api/aset-by-pengguna/<nama_pengguna>')
def get_aset_by_pengguna(nama_pengguna):
    """API endpoint untuk mendapatkan list aset berdasarkan nama pengguna"""
    aset_list = AsetTetap.query.filter_by(nama_pengguna=nama_pengguna).all()
    
    result = []
    for aset in aset_list:
        result.append({
            'id': aset.id,
            'kode_aset': aset.kode_aset,
            'nama_aset': aset.nama_aset,
            'tempat_penggunaan': aset.tempat_penggunaan or '',
        })
    
    return jsonify(result)


@bp.route('/lapor-kerusakan', methods=['GET', 'POST'])
@bp.route('/user/lapor-kerusakan', methods=['GET', 'POST'])
def lapor_kerusakan_public():
    form = LaporanKerusakanPublicForm()
    form.aset_tetap_id.choices = _build_aset_choices()
    form.nama_pengguna.choices = _build_nama_pengguna_choices()

    if request.method == 'GET':
        aset_id = request.args.get('aset_id', type=int)
        if aset_id and any(choice_id == aset_id for choice_id, _ in form.aset_tetap_id.choices):
            form.aset_tetap_id.data = aset_id

        if not form.jumlah.data:
            form.jumlah.data = 1
        if not form.tanggal_diketahui_rusak.data:
            form.tanggal_diketahui_rusak.data = date.today()

    if len(form.aset_tetap_id.choices) <= 1:
        flash('Belum ada data aset. Hubungi admin untuk menambahkan aset terlebih dahulu.', 'warning')
        return render_template('laporan_kerusakan_public.html', form=form, title='Lapor Kerusakan Aset')

    if form.validate_on_submit():
        if form.aset_tetap_id.data == 0:
            flash('Pilih aset terlebih dahulu.', 'danger')
            return render_template('laporan_kerusakan_public.html', form=form, title='Lapor Kerusakan Aset')

        aset = AsetTetap.query.get(form.aset_tetap_id.data)
        if aset is None:
            flash('Aset tidak ditemukan. Silakan pilih aset lain.', 'danger')
            return render_template('laporan_kerusakan_public.html', form=form, title='Lapor Kerusakan Aset')

        laporan = LaporanKerusakan(
            aset_tetap_id=aset.id,
            pelapor_id=None,
            tanggal_diketahui_rusak=form.tanggal_diketahui_rusak.data,
            nama_pengguna=form.nama_pengguna.data,
            lokasi=form.lokasi.data,
            jumlah=form.jumlah.data,
            jenis_kerusakan=form.jenis_kerusakan.data,
            penyebab=form.penyebab.data,
            tindakan=form.tindakan.data,
            kondisi_saat_ini=form.kondisi_saat_ini.data,
            dampak=form.dampak.data,
            status='terkirim'
        )
        db.session.add(laporan)
        db.session.commit()

        flash('Laporan kerusakan berhasil dikirim.', 'success')
        return redirect(url_for('main.lapor_kerusakan_public'))

    return render_template('laporan_kerusakan_public.html', form=form, title='Lapor Kerusakan Aset')
