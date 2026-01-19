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
    
    def get_total_item(self):
        """Get total jumlah barang dalam kategori ini"""
        return self.barang.count()
    
    def to_dict(self):
        return {
            'id': self.id,
            'nama_kategori': self.nama_kategori,
            'deskripsi': self.deskripsi,
            'jumlah_barang': self.get_total_item()
        }


class MerkBarang(db.Model):
    __tablename__ = 'merk_barang'
    
    id = db.Column(db.Integer, primary_key=True)
    nama_merk = db.Column(db.String(100), unique=True, nullable=False)
    tipe = db.Column(db.String(100))
    tanggal_pengadaan = db.Column(db.Date)
    nomor_kontrak = db.Column(db.String(100))
    spesifikasi = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    barang = db.relationship('Barang', backref='merk', lazy='dynamic')
    
    def __repr__(self):
        return f'<MerkBarang {self.nama_merk}>'
    
    def get_total_item(self):
        """Get total jumlah barang dengan merk ini"""
        return self.barang.count()
    
    def to_dict(self):
        return {
            'id': self.id,
            'nama_merk': self.nama_merk,
            'tipe': self.tipe,
            'tanggal_pengadaan': self.tanggal_pengadaan.isoformat() if self.tanggal_pengadaan else None,
            'nomor_kontrak': self.nomor_kontrak,
            'spesifikasi': self.spesifikasi,
            'jumlah_barang': self.get_total_item()
        }
