from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, TextAreaField, RadioField
from wtforms.validators import DataRequired, Length, ValidationError, Optional, NumberRange
from app.models.barang import Barang

class BarangForm(FlaskForm):
    kode_barang = StringField('Kode Barang', validators=[
        DataRequired(message='Kode barang wajib diisi'),
        Length(min=2, max=50, message='Kode barang 2-50 karakter')
    ])
    nama_barang = StringField('Nama Barang', validators=[
        DataRequired(message='Nama barang wajib diisi'),
        Length(min=3, max=255, message='Nama barang 3-255 karakter')
    ])
    
    # Jenis barang
    jenis_barang = RadioField('Jenis Barang', 
        choices=[
            ('inventaris', 'Barang Inventaris (Laptop, Printer, Meja, dll)'),
            ('habis_pakai', 'Barang Habis Pakai (ATK, Tinta, Kertas, dll)')
        ],
        default='inventaris',
        validators=[DataRequired()]
    )
    
    kategori_id = SelectField('Kategori', coerce=int, validators=[Optional()])
    merk_id = SelectField('Merk', coerce=int, validators=[Optional()])
    spesifikasi = TextAreaField('Spesifikasi', validators=[Optional()])
    satuan = StringField('Satuan', validators=[
        DataRequired(message='Satuan wajib diisi'),
        Length(min=2, max=50, message='Satuan 2-50 karakter')
    ], description='Contoh: Unit, Pcs, Box, Buah')
    
    # Untuk barang habis pakai
    satuan_kecil = StringField('Satuan Kecil/Kemasan', validators=[
        Optional(),
        Length(max=50)
    ], description='Contoh: Pack (isi 10 pcs), Box (isi 100 lembar), Rim (500 lembar)')
    
    stok_awal = IntegerField('Stok Awal', validators=[
        DataRequired(message='Stok awal wajib diisi')
    ], default=0)
    
    # Stok minimum untuk alert
    stok_minimum = IntegerField('Stok Minimum', validators=[
        Optional(),
        NumberRange(min=0, message='Stok minimum tidak boleh negatif')
    ], default=0, description='Alert akan muncul jika stok dibawah jumlah ini')
    
    submit = SubmitField('Simpan')
    
    def __init__(self, original_kode=None, *args, **kwargs):
        super(BarangForm, self).__init__(*args, **kwargs)
        self.original_kode = original_kode
    
    def validate_kode_barang(self, kode_barang):
        if self.original_kode is None or kode_barang.data != self.original_kode:
            barang = Barang.query.filter_by(kode_barang=kode_barang.data).first()
            if barang is not None:
                raise ValidationError('Kode barang sudah digunakan. Silakan gunakan kode lain.')
