from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.fields import DateField
from wtforms.validators import DataRequired, Length, Optional

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
