from flask import Blueprint, render_template, request, flash, redirect, url_for
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


@bp.route('/lapor-kerusakan', methods=['GET', 'POST'])
def lapor_kerusakan_public():
    form = LaporanKerusakanPublicForm()
    form.aset_tetap_id.choices = [(0, '-- Pilih Aset --')] + [
        (a.id, f'{a.kode_aset} - {a.nama_aset}')
        for a in AsetTetap.query.order_by(AsetTetap.kode_aset).all()
    ]

    if request.method == 'GET' and not form.jumlah.data:
        form.jumlah.data = 1

    if form.validate_on_submit():
        if form.aset_tetap_id.data == 0:
            flash('Pilih aset terlebih dahulu.', 'danger')
            return render_template('laporan_kerusakan_public.html', form=form, title='Lapor Kerusakan')

        laporan = LaporanKerusakan(
            aset_tetap_id=form.aset_tetap_id.data,
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

    return render_template('laporan_kerusakan_public.html', form=form, title='Lapor Kerusakan')
