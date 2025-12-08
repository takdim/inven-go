from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, StringField, SubmitField
from wtforms.validators import Optional
from datetime import datetime, timedelta


class LaporanBarangForm(FlaskForm):
    """Form filter laporan barang"""
    kategori_id = SelectField('Kategori', coerce=int, validators=[Optional()])
    merk_id = SelectField('Merk', coerce=int, validators=[Optional()])
    status = SelectField('Status Stok', choices=[
        ('', 'Semua'),
        ('rendah', 'Stok Rendah'),
        ('sedang', 'Stok Sedang'),
        ('aman', 'Stok Aman')
    ], validators=[Optional()])
    submit = SubmitField('Tampilkan')


class LaporanTransaksiForm(FlaskForm):
    """Form filter laporan transaksi"""
    tanggal_awal = DateField('Tanggal Awal', format='%Y-%m-%d', 
                             default=lambda: datetime.now() - timedelta(days=30),
                             validators=[Optional()])
    tanggal_akhir = DateField('Tanggal Akhir', format='%Y-%m-%d', 
                              default=datetime.now,
                              validators=[Optional()])
    kode_barang = StringField('Kode Barang', validators=[Optional()])
    submit = SubmitField('Tampilkan')


class LaporanKontrakForm(FlaskForm):
    """Form filter laporan kontrak"""
    tahun = SelectField('Tahun', coerce=int, validators=[Optional()])
    bulan = SelectField('Bulan', choices=[
        ('', 'Semua'),
        ('1', 'Januari'), ('2', 'Februari'), ('3', 'Maret'),
        ('4', 'April'), ('5', 'Mei'), ('6', 'Juni'),
        ('7', 'Juli'), ('8', 'Agustus'), ('9', 'September'),
        ('10', 'Oktober'), ('11', 'November'), ('12', 'Desember')
    ], validators=[Optional()])
    submit = SubmitField('Tampilkan')
