from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError, Optional
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
    kategori_id = SelectField('Kategori', coerce=int, validators=[Optional()])
    merk_id = SelectField('Merk', coerce=int, validators=[Optional()])
    spesifikasi = TextAreaField('Spesifikasi', validators=[Optional()])
    satuan = StringField('Satuan', validators=[
        DataRequired(message='Satuan wajib diisi'),
        Length(min=2, max=50, message='Satuan 2-50 karakter')
    ])
    stok_awal = IntegerField('Stok Awal', validators=[
        DataRequired(message='Stok awal wajib diisi')
    ], default=0)
    submit = SubmitField('Simpan')
    
    def __init__(self, original_kode=None, *args, **kwargs):
        super(BarangForm, self).__init__(*args, **kwargs)
        self.original_kode = original_kode
    
    def validate_kode_barang(self, kode_barang):
        if self.original_kode is None or kode_barang.data != self.original_kode:
            barang = Barang.query.filter_by(kode_barang=kode_barang.data).first()
            if barang is not None:
                raise ValidationError('Kode barang sudah digunakan. Silakan gunakan kode lain.')
