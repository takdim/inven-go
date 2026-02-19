from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.fields import DateField
from wtforms.validators import DataRequired, Length, Optional, ValidationError
from app.models.kategori import MerkBarang

class MerkForm(FlaskForm):
    nama_merk = StringField('Nama Merk', 
                           validators=[DataRequired(), Length(min=2, max=100)],
                           render_kw={"placeholder": "Contoh: HP, Dell, Canon, Epson"})
    
    tanggal_pengadaan = DateField('Tanggal Pengadaan', 
                                 validators=[Optional()],
                                 format='%Y-%m-%d')
    
    spesifikasi = TextAreaField('Spesifikasi',
                               validators=[Length(max=500)],
                               render_kw={"placeholder": "Spesifikasi merk dan tipe (opsional)", "rows": 4})
    
    submit = SubmitField('Simpan')
    
    def __init__(self, original_nama_merk=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_nama_merk = original_nama_merk
    
    def validate_nama_merk(self, field):
        """Check if merk with this nama already exists (excluding current record during edit)"""
        # If editing and nama_merk hasn't changed, allow it
        if self.original_nama_merk and field.data == self.original_nama_merk:
            return
        
        existing = MerkBarang.query.filter_by(nama_merk=field.data).first()
        if existing:
            raise ValidationError('Merk dengan nama ini sudah ada di database!')
