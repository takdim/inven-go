from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField, SubmitField, IntegerField, DecimalField, SelectField
from wtforms.validators import DataRequired, Length, Optional, NumberRange, ValidationError
from app.models.kontrak import KontrakBarang

class KontrakForm(FlaskForm):
    nomor_kontrak = StringField('Nomor Kontrak/SPK', validators=[
        DataRequired(message='Nomor kontrak wajib diisi'),
        Length(min=3, max=100, message='Nomor kontrak 3-100 karakter')
    ])
    tanggal_kontrak = DateField('Tanggal Kontrak', format='%Y-%m-%d', validators=[
        DataRequired(message='Tanggal kontrak wajib diisi')
    ])
    deskripsi = TextAreaField('Deskripsi/Keterangan', validators=[Optional()])
    submit = SubmitField('Simpan')
    
    def __init__(self, original_nomor=None, *args, **kwargs):
        super(KontrakForm, self).__init__(*args, **kwargs)
        self.original_nomor = original_nomor
    
    def validate_nomor_kontrak(self, nomor_kontrak):
        if self.original_nomor is None or nomor_kontrak.data != self.original_nomor:
            kontrak = KontrakBarang.query.filter_by(nomor_kontrak=nomor_kontrak.data).first()
            if kontrak is not None:
                raise ValidationError('Nomor kontrak sudah digunakan. Silakan gunakan nomor lain.')


class BarangKontrakForm(FlaskForm):
    barang_id = SelectField('Pilih Barang', coerce=int, validators=[
        DataRequired(message='Barang wajib dipilih')
    ])
    qty_kontrak = IntegerField('Jumlah/Qty', validators=[
        DataRequired(message='Qty wajib diisi'),
        NumberRange(min=1, message='Qty minimal 1')
    ])
    harga_satuan = DecimalField('Harga Satuan (Rp)', validators=[
        Optional(),
        NumberRange(min=0, message='Harga tidak boleh negatif')
    ], places=2)
    submit = SubmitField('Tambah Barang')
