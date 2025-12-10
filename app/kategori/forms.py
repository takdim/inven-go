from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class KategoriForm(FlaskForm):
    nama_kategori = StringField('Nama Kategori', 
                               validators=[DataRequired(), Length(min=2, max=100)],
                               render_kw={"placeholder": "Contoh: Elektronik, Furniture, ATK"})
    
    deskripsi = TextAreaField('Deskripsi',
                             validators=[Length(max=500)],
                             render_kw={"placeholder": "Deskripsi kategori (opsional)", "rows": 4})
    
    submit = SubmitField('Simpan')
