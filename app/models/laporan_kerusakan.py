from app import db
from datetime import datetime


class LaporanKerusakan(db.Model):
    __tablename__ = 'laporan_kerusakan'

    id = db.Column(db.Integer, primary_key=True)
    aset_tetap_id = db.Column(db.Integer, db.ForeignKey('aset_tetap.id', ondelete='CASCADE'), nullable=False, index=True)
    pelapor_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), index=True)
    tanggal_diketahui_rusak = db.Column(db.Date, nullable=False)
    nama_pengguna = db.Column(db.String(255), nullable=False)
    lokasi = db.Column(db.String(255), nullable=False)
    jumlah = db.Column(db.Integer, default=1, nullable=False)
    jenis_kerusakan = db.Column(db.Text, nullable=False)
    penyebab = db.Column(db.Text)
    tindakan = db.Column(db.Text)
    kondisi_saat_ini = db.Column(db.Text)
    dampak = db.Column(db.Text)
    status = db.Column(
        db.Enum('draft', 'terkirim', 'selesai', name='laporan_kerusakan_status'),
        default='draft',
        nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    pelapor = db.relationship('User', backref='laporan_kerusakan_list')

    def __repr__(self):
        return f'<LaporanKerusakan {self.id} aset={self.aset_tetap_id}>'
