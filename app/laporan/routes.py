from flask import render_template, request, send_file, flash, redirect, url_for
from flask_login import login_required
from app.laporan import laporan_bp
from app.laporan.forms import LaporanBarangForm, LaporanTransaksiForm, LaporanKontrakForm
from app.models import Barang, BarangMasuk, BarangKeluar, KontrakBarang, KategoriBarang, MerkBarang
from app.utils.excel_export import export_barang_to_excel, export_kontrak_to_excel, export_transaksi_to_excel
from app.utils.pdf_export import export_barang_to_pdf, export_kontrak_to_pdf, export_transaksi_to_pdf
from datetime import datetime


@laporan_bp.route('/')
@login_required
def index():
    """Halaman dashboard laporan"""
    return render_template('laporan/index.html', title='Laporan')


@laporan_bp.route('/barang')
@login_required
def laporan_barang():
    """Laporan daftar barang"""
    form = LaporanBarangForm()
    
    # Populate choices
    form.kategori_id.choices = [(0, 'Semua')] + [(k.id, k.nama_kategori) for k in KategoriBarang.query.all()]
    form.merk_id.choices = [(0, 'Semua')] + [(m.id, m.nama_merk) for m in MerkBarang.query.all()]
    
    # Query barang
    query = Barang.query
    
    # Apply filters
    if request.args.get('kategori_id') and int(request.args.get('kategori_id')) > 0:
        query = query.filter_by(kategori_id=int(request.args.get('kategori_id')))
        form.kategori_id.data = int(request.args.get('kategori_id'))
    
    if request.args.get('merk_id') and int(request.args.get('merk_id')) > 0:
        query = query.filter_by(merk_id=int(request.args.get('merk_id')))
        form.merk_id.data = int(request.args.get('merk_id'))
    
    barang_list = query.all()
    
    # Calculate stok akhir
    data = []
    for barang in barang_list:
        stok_akhir = barang.get_stok_akhir()
        
        # Filter by status
        if request.args.get('status'):
            status = request.args.get('status')
            if status == 'rendah' and stok_akhir >= 10:
                continue
            elif status == 'sedang' and (stok_akhir < 10 or stok_akhir >= 50):
                continue
            elif status == 'aman' and stok_akhir < 50:
                continue
        
        data.append({
            'barang': barang,
            'stok_akhir': stok_akhir
        })
    
    if request.args.get('status'):
        form.status.data = request.args.get('status')
    
    return render_template('laporan/barang.html', 
                          title='Laporan Barang',
                          form=form,
                          data=data)


@laporan_bp.route('/barang/export-excel')
@login_required
def export_barang_excel():
    """Export laporan barang ke Excel"""
    # Get filters from request
    query = Barang.query
    
    if request.args.get('kategori_id') and int(request.args.get('kategori_id')) > 0:
        query = query.filter_by(kategori_id=int(request.args.get('kategori_id')))
    
    if request.args.get('merk_id') and int(request.args.get('merk_id')) > 0:
        query = query.filter_by(merk_id=int(request.args.get('merk_id')))
    
    barang_list = query.all()
    
    # Calculate stok akhir
    data = []
    for barang in barang_list:
        stok_akhir = barang.get_stok_akhir()
        
        # Filter by status
        if request.args.get('status'):
            status = request.args.get('status')
            if status == 'rendah' and stok_akhir >= 10:
                continue
            elif status == 'sedang' and (stok_akhir < 10 or stok_akhir >= 50):
                continue
            elif status == 'aman' and stok_akhir < 50:
                continue
        
        data.append({
            'barang': barang,
            'stok_akhir': stok_akhir
        })
    
    # Generate Excel
    buffer = export_barang_to_excel(data)
    
    # Generate filename
    filename = f'Laporan_Barang_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    
    return send_file(buffer, 
                    mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    as_attachment=True,
                    download_name=filename)


@laporan_bp.route('/barang/export-pdf')
@login_required
def export_barang_pdf():
    """Export laporan barang ke PDF"""
    # Get filters from request
    query = Barang.query
    
    if request.args.get('kategori_id') and int(request.args.get('kategori_id')) > 0:
        query = query.filter_by(kategori_id=int(request.args.get('kategori_id')))
    
    if request.args.get('merk_id') and int(request.args.get('merk_id')) > 0:
        query = query.filter_by(merk_id=int(request.args.get('merk_id')))
    
    barang_list = query.all()
    
    # Calculate stok akhir
    data = []
    for barang in barang_list:
        stok_akhir = barang.get_stok_akhir()
        
        # Filter by status
        if request.args.get('status'):
            status = request.args.get('status')
            if status == 'rendah' and stok_akhir >= 10:
                continue
            elif status == 'sedang' and (stok_akhir < 10 or stok_akhir >= 50):
                continue
            elif status == 'aman' and stok_akhir < 50:
                continue
        
        data.append({
            'barang': barang,
            'stok_akhir': stok_akhir
        })
    
    # Generate PDF
    buffer = export_barang_to_pdf(data)
    
    # Generate filename
    filename = f'Laporan_Barang_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    
    return send_file(buffer, 
                    mimetype='application/pdf',
                    as_attachment=True,
                    download_name=filename)


@laporan_bp.route('/kontrak')
@login_required
def laporan_kontrak():
    """Laporan daftar kontrak"""
    form = LaporanKontrakForm()
    
    # Populate tahun choices
    current_year = datetime.now().year
    form.tahun.choices = [(0, 'Semua')] + [(y, str(y)) for y in range(current_year - 5, current_year + 2)]
    
    # Query kontrak
    query = KontrakBarang.query
    
    # Apply filters
    if request.args.get('tahun') and int(request.args.get('tahun')) > 0:
        tahun = int(request.args.get('tahun'))
        query = query.filter(KontrakBarang.tanggal_kontrak.between(
            datetime(tahun, 1, 1),
            datetime(tahun, 12, 31)
        ))
        form.tahun.data = tahun
    
    if request.args.get('bulan'):
        bulan = int(request.args.get('bulan'))
        tahun = int(request.args.get('tahun', current_year))
        query = query.filter(KontrakBarang.tanggal_kontrak.between(
            datetime(tahun, bulan, 1),
            datetime(tahun, bulan, 28 if bulan == 2 else 30 if bulan in [4, 6, 9, 11] else 31)
        ))
        form.bulan.data = str(bulan)
    
    kontrak_list = query.order_by(KontrakBarang.tanggal_kontrak.desc()).all()
    
    return render_template('laporan/kontrak.html', 
                          title='Laporan Kontrak',
                          form=form,
                          kontrak_list=kontrak_list)


@laporan_bp.route('/kontrak/export-excel')
@login_required
def export_kontrak_excel():
    """Export laporan kontrak ke Excel"""
    # Get filters from request
    query = KontrakBarang.query
    
    if request.args.get('tahun') and int(request.args.get('tahun')) > 0:
        tahun = int(request.args.get('tahun'))
        query = query.filter(KontrakBarang.tanggal_kontrak.between(
            datetime(tahun, 1, 1),
            datetime(tahun, 12, 31)
        ))
    
    if request.args.get('bulan'):
        bulan = int(request.args.get('bulan'))
        tahun = int(request.args.get('tahun', datetime.now().year))
        query = query.filter(KontrakBarang.tanggal_kontrak.between(
            datetime(tahun, bulan, 1),
            datetime(tahun, bulan, 28 if bulan == 2 else 30 if bulan in [4, 6, 9, 11] else 31)
        ))
    
    kontrak_list = query.order_by(KontrakBarang.tanggal_kontrak.desc()).all()
    
    # Generate Excel
    buffer = export_kontrak_to_excel(kontrak_list)
    
    # Generate filename
    filename = f'Laporan_Kontrak_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    
    return send_file(buffer, 
                    mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    as_attachment=True,
                    download_name=filename)


@laporan_bp.route('/kontrak/export-pdf')
@login_required
def export_kontrak_pdf():
    """Export laporan kontrak ke PDF"""
    # Get filters from request
    query = KontrakBarang.query
    
    if request.args.get('tahun') and int(request.args.get('tahun')) > 0:
        tahun = int(request.args.get('tahun'))
        query = query.filter(KontrakBarang.tanggal_kontrak.between(
            datetime(tahun, 1, 1),
            datetime(tahun, 12, 31)
        ))
    
    if request.args.get('bulan'):
        bulan = int(request.args.get('bulan'))
        tahun = int(request.args.get('tahun', datetime.now().year))
        query = query.filter(KontrakBarang.tanggal_kontrak.between(
            datetime(tahun, bulan, 1),
            datetime(tahun, bulan, 28 if bulan == 2 else 30 if bulan in [4, 6, 9, 11] else 31)
        ))
    
    kontrak_list = query.order_by(KontrakBarang.tanggal_kontrak.desc()).all()
    
    # Generate PDF
    buffer = export_kontrak_to_pdf(kontrak_list)
    
    # Generate filename
    filename = f'Laporan_Kontrak_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    
    return send_file(buffer, 
                    mimetype='application/pdf',
                    as_attachment=True,
                    download_name=filename)


@laporan_bp.route('/transaksi-masuk')
@login_required
def laporan_transaksi_masuk():
    """Laporan barang masuk"""
    form = LaporanTransaksiForm()
    
    # Query transaksi
    query = BarangMasuk.query
    
    # Apply filters
    if request.args.get('tanggal_awal'):
        tanggal_awal = datetime.strptime(request.args.get('tanggal_awal'), '%Y-%m-%d')
        query = query.filter(BarangMasuk.tanggal >= tanggal_awal)
        form.tanggal_awal.data = tanggal_awal
    
    if request.args.get('tanggal_akhir'):
        tanggal_akhir = datetime.strptime(request.args.get('tanggal_akhir'), '%Y-%m-%d')
        query = query.filter(BarangMasuk.tanggal <= tanggal_akhir)
        form.tanggal_akhir.data = tanggal_akhir
    
    if request.args.get('kode_barang'):
        query = query.filter(BarangMasuk.kode_barang.like(f"%{request.args.get('kode_barang')}%"))
        form.kode_barang.data = request.args.get('kode_barang')
    
    transaksi_list = query.order_by(BarangMasuk.tanggal.desc()).all()
    
    return render_template('laporan/transaksi_masuk.html', 
                          title='Laporan Barang Masuk',
                          form=form,
                          transaksi_list=transaksi_list)


@laporan_bp.route('/transaksi-masuk/export-excel')
@login_required
def export_transaksi_masuk_excel():
    """Export laporan barang masuk ke Excel"""
    # Get filters from request
    query = BarangMasuk.query
    
    tanggal_awal = None
    tanggal_akhir = None
    
    if request.args.get('tanggal_awal'):
        tanggal_awal = datetime.strptime(request.args.get('tanggal_awal'), '%Y-%m-%d')
        query = query.filter(BarangMasuk.tanggal >= tanggal_awal)
    
    if request.args.get('tanggal_akhir'):
        tanggal_akhir = datetime.strptime(request.args.get('tanggal_akhir'), '%Y-%m-%d')
        query = query.filter(BarangMasuk.tanggal <= tanggal_akhir)
    
    if request.args.get('kode_barang'):
        query = query.filter(BarangMasuk.kode_barang.like(f"%{request.args.get('kode_barang')}%"))
    
    transaksi_list = query.order_by(BarangMasuk.tanggal.desc()).all()
    
    # Generate Excel
    buffer = export_transaksi_to_excel(transaksi_list, 'masuk', tanggal_awal, tanggal_akhir)
    
    # Generate filename
    filename = f'Laporan_Barang_Masuk_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    
    return send_file(buffer, 
                    mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    as_attachment=True,
                    download_name=filename)


@laporan_bp.route('/transaksi-masuk/export-pdf')
@login_required
def export_transaksi_masuk_pdf():
    """Export laporan barang masuk ke PDF"""
    # Get filters from request
    query = BarangMasuk.query
    
    tanggal_awal = None
    tanggal_akhir = None
    
    if request.args.get('tanggal_awal'):
        tanggal_awal = datetime.strptime(request.args.get('tanggal_awal'), '%Y-%m-%d')
        query = query.filter(BarangMasuk.tanggal >= tanggal_awal)
    
    if request.args.get('tanggal_akhir'):
        tanggal_akhir = datetime.strptime(request.args.get('tanggal_akhir'), '%Y-%m-%d')
        query = query.filter(BarangMasuk.tanggal <= tanggal_akhir)
    
    if request.args.get('kode_barang'):
        query = query.filter(BarangMasuk.kode_barang.like(f"%{request.args.get('kode_barang')}%"))
    
    transaksi_list = query.order_by(BarangMasuk.tanggal.desc()).all()
    
    # Generate PDF
    buffer = export_transaksi_to_pdf(transaksi_list, 'masuk', tanggal_awal, tanggal_akhir)
    
    # Generate filename
    filename = f'Laporan_Barang_Masuk_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    
    return send_file(buffer, 
                    mimetype='application/pdf',
                    as_attachment=True,
                    download_name=filename)


@laporan_bp.route('/transaksi-keluar')
@login_required
def laporan_transaksi_keluar():
    """Laporan barang keluar"""
    form = LaporanTransaksiForm()
    
    # Query transaksi
    query = BarangKeluar.query
    
    # Apply filters
    if request.args.get('tanggal_awal'):
        tanggal_awal = datetime.strptime(request.args.get('tanggal_awal'), '%Y-%m-%d')
        query = query.filter(BarangKeluar.tanggal >= tanggal_awal)
        form.tanggal_awal.data = tanggal_awal
    
    if request.args.get('tanggal_akhir'):
        tanggal_akhir = datetime.strptime(request.args.get('tanggal_akhir'), '%Y-%m-%d')
        query = query.filter(BarangKeluar.tanggal <= tanggal_akhir)
        form.tanggal_akhir.data = tanggal_akhir
    
    if request.args.get('kode_barang'):
        query = query.filter(BarangKeluar.kode_barang.like(f"%{request.args.get('kode_barang')}%"))
        form.kode_barang.data = request.args.get('kode_barang')
    
    transaksi_list = query.order_by(BarangKeluar.tanggal.desc()).all()
    
    return render_template('laporan/transaksi_keluar.html', 
                          title='Laporan Barang Keluar',
                          form=form,
                          transaksi_list=transaksi_list)


@laporan_bp.route('/transaksi-keluar/export-excel')
@login_required
def export_transaksi_keluar_excel():
    """Export laporan barang keluar ke Excel"""
    # Get filters from request
    query = BarangKeluar.query
    
    tanggal_awal = None
    tanggal_akhir = None
    
    if request.args.get('tanggal_awal'):
        tanggal_awal = datetime.strptime(request.args.get('tanggal_awal'), '%Y-%m-%d')
        query = query.filter(BarangKeluar.tanggal >= tanggal_awal)
    
    if request.args.get('tanggal_akhir'):
        tanggal_akhir = datetime.strptime(request.args.get('tanggal_akhir'), '%Y-%m-%d')
        query = query.filter(BarangKeluar.tanggal <= tanggal_akhir)
    
    if request.args.get('kode_barang'):
        query = query.filter(BarangKeluar.kode_barang.like(f"%{request.args.get('kode_barang')}%"))
    
    transaksi_list = query.order_by(BarangKeluar.tanggal.desc()).all()
    
    # Generate Excel
    buffer = export_transaksi_to_excel(transaksi_list, 'keluar', tanggal_awal, tanggal_akhir)
    
    # Generate filename
    filename = f'Laporan_Barang_Keluar_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    
    return send_file(buffer, 
                    mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    as_attachment=True,
                    download_name=filename)


@laporan_bp.route('/transaksi-keluar/export-pdf')
@login_required
def export_transaksi_keluar_pdf():
    """Export laporan barang keluar ke PDF"""
    # Get filters from request
    query = BarangKeluar.query
    
    tanggal_awal = None
    tanggal_akhir = None
    
    if request.args.get('tanggal_awal'):
        tanggal_awal = datetime.strptime(request.args.get('tanggal_awal'), '%Y-%m-%d')
        query = query.filter(BarangKeluar.tanggal >= tanggal_awal)
    
    if request.args.get('tanggal_akhir'):
        tanggal_akhir = datetime.strptime(request.args.get('tanggal_akhir'), '%Y-%m-%d')
        query = query.filter(BarangKeluar.tanggal <= tanggal_akhir)
    
    if request.args.get('kode_barang'):
        query = query.filter(BarangKeluar.kode_barang.like(f"%{request.args.get('kode_barang')}%"))
    
    transaksi_list = query.order_by(BarangKeluar.tanggal.desc()).all()
    
    # Generate PDF
    buffer = export_transaksi_to_pdf(transaksi_list, 'keluar', tanggal_awal, tanggal_akhir)
    
    # Generate filename
    filename = f'Laporan_Barang_Keluar_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    
    return send_file(buffer, 
                    mimetype='application/pdf',
                    as_attachment=True,
                    download_name=filename)
