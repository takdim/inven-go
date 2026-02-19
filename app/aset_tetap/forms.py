from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length, ValidationError, Optional, NumberRange
from app.models.aset_tetap import AsetTetap

class AsetTetapForm(FlaskForm):
    kode_aset = StringField('Kode Aset', validators=[
        DataRequired(message='Kode aset wajib diisi'),
        Length(min=2, max=50, message='Kode aset 2-50 karakter')
    ])
    nama_aset = StringField('Nama Aset', validators=[
        DataRequired(message='Nama aset wajib diisi'),
        Length(min=3, max=255, message='Nama aset 3-255 karakter')
    ])
    
    kategori_id = SelectField('Kategori', coerce=int, validators=[Optional()])
    merk_aset_tetap_id = SelectField('Jenis Aset', coerce=int, validators=[Optional()])
    tanggal_kontrak = DateField('Tanggal Kontrak/SPK', validators=[Optional()])
    kontrak_spk = StringField('Kontrak/SPK', validators=[
        Optional(),
        Length(max=200, message='Kontrak/SPK maksimal 200 karakter')
    ])
    tempat_penggunaan = StringField('Tempat Penggunaan', validators=[
        Optional(),
        Length(max=255, message='Tempat penggunaan maksimal 255 karakter')
    ])
    nama_pengguna = StringField('Nama Pengguna', validators=[
        Optional(),
        Length(max=255, message='Nama pengguna maksimal 255 karakter')
    ])
    total_barang = IntegerField('Total Barang', validators=[
        Optional(),
        NumberRange(min=0, message='Total barang minimal 0')
    ])
    spesifikasi = TextAreaField('Spesifikasi', validators=[
        Optional(),
        Length(max=2000, message='Spesifikasi maksimal 2000 karakter')
    ])
    submit = SubmitField('Simpan')
    
    def __init__(self, original_kode=None, *args, **kwargs):
        super(AsetTetapForm, self).__init__(*args, **kwargs)
        self.original_kode = original_kode
    
    def validate_kode_aset(self, kode_aset):
        if kode_aset.data != self.original_kode:
            aset = AsetTetap.query.filter_by(kode_aset=kode_aset.data).first()
            if aset:
                raise ValidationError('Kode aset ini sudah digunakan!')


class LaporanKerusakanForm(FlaskForm):
    tanggal_diketahui_rusak = DateField('Tanggal Diketahui Rusak', validators=[
        DataRequired(message='Tanggal diketahui rusak wajib diisi')
    ])
    nama_pengguna = StringField('Nama Pengguna', validators=[
        DataRequired(message='Nama pengguna wajib diisi'),
        Length(max=255, message='Nama pengguna maksimal 255 karakter')
    ])
    lokasi = StringField('Lokasi', validators=[
        DataRequired(message='Lokasi wajib diisi'),
        Length(max=255, message='Lokasi maksimal 255 karakter')
    ])
    jumlah = IntegerField('Jumlah', validators=[
        DataRequired(message='Jumlah wajib diisi'),
        NumberRange(min=1, message='Jumlah minimal 1')
    ])
    jenis_kerusakan = TextAreaField('Jenis Kerusakan', validators=[
        DataRequired(message='Jenis kerusakan wajib diisi')
    ])
    penyebab = TextAreaField('Penyebab (Jika Diketahui)', validators=[Optional()])
    tindakan = TextAreaField('Tindakan yang Sudah Dilakukan', validators=[Optional()])
    kondisi_saat_ini = TextAreaField('Kondisi Saat Ini', validators=[Optional()])
    dampak = TextAreaField('Dampak', validators=[Optional()])
    status = SelectField('Status', choices=[
        ('draft', 'Draft'),
        ('terkirim', 'Terkirim'),
        ('selesai', 'Selesai')
    ], validators=[DataRequired()])
    submit = SubmitField('Simpan')


class LaporanKerusakanPublicForm(FlaskForm):
    aset_tetap_id = SelectField('Aset', coerce=int, validators=[DataRequired()])
    tanggal_diketahui_rusak = DateField('Tanggal Diketahui Rusak', validators=[
        DataRequired(message='Tanggal diketahui rusak wajib diisi')
    ])
    nama_pengguna = StringField('Nama Pengguna', validators=[
        DataRequired(message='Nama pengguna wajib diisi'),
        Length(max=255, message='Nama pengguna maksimal 255 karakter')
    ])
    lokasi = StringField('Lokasi', validators=[
        DataRequired(message='Lokasi wajib diisi'),
        Length(max=255, message='Lokasi maksimal 255 karakter')
    ])
    jumlah = IntegerField('Jumlah', validators=[
        DataRequired(message='Jumlah wajib diisi'),
        NumberRange(min=1, message='Jumlah minimal 1')
    ])
    jenis_kerusakan = TextAreaField('Jenis Kerusakan', validators=[
        DataRequired(message='Jenis kerusakan wajib diisi')
    ])
    penyebab = TextAreaField('Penyebab (Jika Diketahui)', validators=[Optional()])
    tindakan = TextAreaField('Tindakan yang Sudah Dilakukan', validators=[Optional()])
    kondisi_saat_ini = TextAreaField('Kondisi Saat Ini', validators=[Optional()])
    dampak = TextAreaField('Dampak', validators=[Optional()])
    submit = SubmitField('Kirim Laporan')
