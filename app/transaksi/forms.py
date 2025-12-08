from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, DateField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from datetime import date

class TransaksiForm(FlaskForm):
    tanggal = DateField('Tanggal', validators=[DataRequired(message='Tanggal wajib diisi')], default=date.today)
    kode_barang = SelectField('Barang', validators=[DataRequired(message='Barang wajib dipilih')], coerce=str)
    qty = IntegerField('Jumlah', validators=[
        DataRequired(message='Jumlah wajib diisi'),
        NumberRange(min=1, message='Jumlah minimal 1')
    ])
    keterangan = TextAreaField('Keterangan')
    submit = SubmitField('Simpan')
