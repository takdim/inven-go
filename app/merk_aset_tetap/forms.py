from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError, Optional
from app.models.merk_aset_tetap import MerkAsetTetap

class MerkAsetTetapForm(FlaskForm):
    nama_merk = StringField('Jenis Aset', validators=[
        DataRequired(message='Jenis aset tidak boleh kosong'),
        Length(min=2, max=100, message='Jenis aset harus antara 2-100 karakter')
    ])
    
    tipe = StringField('Tipe', validators=[
        Optional(),
        Length(max=100, message='Tipe maksimal 100 karakter')
    ])
    
    tanggal_pengadaan = DateField('Tanggal Pengadaan', validators=[Optional()])
    
    nomor_kontrak = StringField('Nomor Kontrak', validators=[
        Optional(),
        Length(max=100, message='Nomor kontrak maksimal 100 karakter')
    ])
    
    spesifikasi = TextAreaField('Spesifikasi', validators=[
        Optional(),
        Length(max=2000, message='Spesifikasi maksimal 2000 karakter')
    ])
    
    submit = SubmitField('Simpan')
    
    def validate_nama_merk(self, field):
        # Check jika sedang edit, jangan validasi dengan diri sendiri
        if hasattr(self, 'edit_id') and self.edit_id:
            existing = MerkAsetTetap.query.filter(
                MerkAsetTetap.nama_merk == field.data,
                MerkAsetTetap.id != self.edit_id
            ).first()
        else:
            existing = MerkAsetTetap.query.filter_by(nama_merk=field.data).first()
        
        if existing:
            raise ValidationError('Jenis aset sudah digunakan.')
