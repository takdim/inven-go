from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, TextAreaField, RadioField, DateField
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


class PermintaanBarangPublicForm(FlaskForm):
    nama_pengguna = SelectField('Nama', choices=[
        ('Rasman, S.Sos.', 'Rasman, S.Sos.'),
        ('Dr. Iskandar, S.Sos.MM', 'Dr. Iskandar, S.Sos.MM'),
        ('Darmiati, S.Sos.,MM.', 'Darmiati, S.Sos.,MM.'),
        ('A. Milu Marguna, S.Sos.MM', 'A. Milu Marguna, S.Sos.MM'),
        ('Asmawati Mile, S.Sos.', 'Asmawati Mile, S.Sos.'),
        ('Sangiasseri Abubakar, S.Hum', 'Sangiasseri Abubakar, S.Hum'),
        ('Hasmaliati, S.Sos', 'Hasmaliati, S.Sos'),
        ('Masnah, S. Sos', 'Masnah, S. Sos'),
        ('Hasyim, S.Sos. M.Si', 'Hasyim, S.Sos. M.Si'),
        ('Trimurtiati, S.Sos', 'Trimurtiati, S.Sos'),
        ('Nur Hasnah, S.H., M.IP', 'Nur Hasnah, S.H., M.IP'),
        ('Zohrah Djohan,S.I.P', 'Zohrah Djohan,S.I.P'),
        ('Rosmini', 'Rosmini'),
        ('Darmawati, S.Sos', 'Darmawati, S.Sos'),
        ('Darmawati Nembo, A.Md', 'Darmawati Nembo, A.Md'),
        ('Hatijah, A.Md', 'Hatijah, A.Md'),
        ('Nasyir Nompo, S.Sos', 'Nasyir Nompo, S.Sos'),
        ('Andi Nasri Abduh, S.Sos., M.Hum', 'Andi Nasri Abduh, S.Sos., M.Hum'),
        ('Wahyuni Aras, S.AP., M.Ikom', 'Wahyuni Aras, S.AP., M.Ikom'),
        ('Tadius Tangnga', 'Tadius Tangnga'),
        ('Kamaluddin M., S.IP., M.Hum.', 'Kamaluddin M., S.IP., M.Hum.'),
        ('Nuraeda, S.Sos', 'Nuraeda, S.Sos'),
        ('Erwiyanti, S.IP.', 'Erwiyanti, S.IP.'),
        ('A. Nurjannah, S.Kom', 'A. Nurjannah, S.Kom'),
        ('Nurul Fitrihasari Ramadhani', 'Nurul Fitrihasari Ramadhani'),
        ('A. Nur Fadillah, S.IP', 'A. Nur Fadillah, S.IP'),
        ('Siti Fathirah Suciaty, ST', 'Siti Fathirah Suciaty, ST'),
        ('Chandra Risma Adri, S.Kom', 'Chandra Risma Adri, S.Kom'),
        ('Muh Takdim', 'Muh Takdim')
    ], validators=[
        DataRequired(message='Nama wajib dipilih')
    ])
    nama_barang1 = SelectField('Nama Barang 1', coerce=int, validators=[
        DataRequired(message='Barang 1 wajib dipilih')
    ])
    banyaknya1 = IntegerField('Banyaknya', validators=[
        DataRequired(message='Banyaknya wajib diisi'),
        NumberRange(min=1, message='Banyaknya minimal 1')
    ])
    nama_barang2 = SelectField('Nama Barang 2', coerce=int, validators=[
        Optional()
    ])
    banyaknya2 = IntegerField('Banyaknya', validators=[
        Optional(),
        NumberRange(min=1, message='Banyaknya minimal 1')
    ])
    nama_barang3 = SelectField('Nama Barang 3', coerce=int, validators=[
        Optional()
    ])
    banyaknya3 = IntegerField('Banyaknya', validators=[
        Optional(),
        NumberRange(min=1, message='Banyaknya minimal 1')
    ])
    tempat_penggunaan = StringField('Tempat Penggunaan', validators=[
        DataRequired(message='Tempat penggunaan wajib diisi'),
        Length(max=255, message='Tempat penggunaan maksimal 255 karakter')
    ])
    tanggal = DateField('Tanggal', validators=[
        DataRequired(message='Tanggal wajib diisi')
    ])
    submit = SubmitField('Kirim Permintaan')
