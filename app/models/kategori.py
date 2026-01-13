from app import db
from datetime import datetime

class KategoriBarang(db.Model):
    __tablename__ = 'kategori_barang'
    
    id = db.Column(db.Integer, primary_key=True)
    nama_kategori = db.Column(db.String(100), unique=True, nullable=False)
    deskripsi = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    barang = db.relationship('Barang', backref='kategori', lazy='dynamic')
    
    def __repr__(self):
        return f'<KategoriBarang {self.nama_kategori}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nama_kategori': self.nama_kategori,
            'deskripsi': self.deskripsi,
            'jumlah_barang': self.barang.count()
        }


class MerkBarang(db.Model):
    __tablename__ = 'merk_barang'
    
    id = db.Column(db.Integer, primary_key=True)
    nama_merk = db.Column(db.String(100), unique=True, nullable=False)
    deskripsi = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    barang = db.relationship('Barang', backref='merk', lazy='dynamic')
    aset_tetap = db.relationship('AsetTetap', foreign_keys='AsetTetap.merk_id', lazy='dynamic')
    
    def get_total_item(self):
        """Hitung total barang + aset tetap"""
        return self.barang.count() + self.aset_tetap.count()
    
    def __repr__(self):
        return f'<MerkBarang {self.nama_merk}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nama_merk': self.nama_merk,
            'deskripsi': self.deskripsi,
            'jumlah_barang': self.barang.count()
        }
