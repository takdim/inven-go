from app import db
from datetime import datetime

class PermintaanBarang(db.Model):
    __tablename__ = 'permintaan_barang'

    id = db.Column(db.Integer, primary_key=True)
    nama_pengguna = db.Column(db.String(255), nullable=False)
    barang1_id = db.Column(db.Integer, db.ForeignKey('barang.id'), nullable=False)
    banyaknya1 = db.Column(db.Integer, nullable=False, default=1)
    barang2_id = db.Column(db.Integer, db.ForeignKey('barang.id'), nullable=True)
    banyaknya2 = db.Column(db.Integer, nullable=True)
    barang3_id = db.Column(db.Integer, db.ForeignKey('barang.id'), nullable=True)
    banyaknya3 = db.Column(db.Integer, nullable=True)
    tempat_penggunaan = db.Column(db.String(255), nullable=False)
    tanggal = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), default='terkirim', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    barang1 = db.relationship('Barang', foreign_keys=[barang1_id])
    barang2 = db.relationship('Barang', foreign_keys=[barang2_id])
    barang3 = db.relationship('Barang', foreign_keys=[barang3_id])

    def __repr__(self):
        return f'<PermintaanBarang {self.id}: {self.nama_pengguna}>'