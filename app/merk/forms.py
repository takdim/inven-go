from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class MerkForm(FlaskForm):
    nama_merk = StringField('Nama Merk', 
                           validators=[DataRequired(), Length(min=2, max=100)],
                           render_kw={"placeholder": "Contoh: HP, Dell, Canon, Epson"})
    
    deskripsi = TextAreaField('Deskripsi',
                             validators=[Length(max=500)],
                             render_kw={"placeholder": "Deskripsi merk (opsional)", "rows": 4})
    
    submit = SubmitField('Simpan')
