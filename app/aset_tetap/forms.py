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
    merk_id = SelectField('Merk', coerce=int, validators=[Optional()])
    spesifikasi = TextAreaField('Spesifikasi', validators=[Optional()])
    satuan = StringField('Jumlah Aset', validators=[
        DataRequired(message='Jumlah aset wajib diisi'),
        Length(min=1, max=50, message='Jumlah aset 1-50 karakter')
    ])
    satuan_kecil = StringField('Satuan Kecil (Opsional)', validators=[
        Length(max=50, message='Satuan kecil maksimal 50 karakter'),
        Optional()
    ])
    nomor_kontrak = StringField('Nomor Kontrak/SPK', validators=[
        Optional(),
        Length(max=100, message='Nomor kontrak maksimal 100 karakter')
    ])
    tanggal_kontrak = DateField('Tanggal Kontrak/SPK', validators=[Optional()])
    submit = SubmitField('Simpan')
    
    def __init__(self, original_kode=None, *args, **kwargs):
        super(AsetTetapForm, self).__init__(*args, **kwargs)
        self.original_kode = original_kode
    
    def validate_kode_aset(self, kode_aset):
        if kode_aset.data != self.original_kode:
            aset = AsetTetap.query.filter_by(kode_aset=kode_aset.data).first()
            if aset:
                raise ValidationError('Kode aset ini sudah digunakan!')
