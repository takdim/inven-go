from app import db
from datetime import datetime

class Barang(db.Model):
    __tablename__ = 'barang'
    
    id = db.Column(db.Integer, primary_key=True)
    kode_barang = db.Column(db.String(50), unique=True, nullable=False, index=True)
    nama_barang = db.Column(db.String(255), nullable=False)
    satuan = db.Column(db.String(50), nullable=False)
    kategori_id = db.Column(db.Integer, db.ForeignKey('kategori_barang.id'), nullable=True)
    merk_id = db.Column(db.Integer, db.ForeignKey('merk_barang.id'), nullable=True)
    spesifikasi = db.Column(db.Text, nullable=True)
    stok_awal = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    barang_masuk = db.relationship('BarangMasuk', backref='barang', lazy='dynamic', cascade='all, delete-orphan')
    barang_keluar = db.relationship('BarangKeluar', backref='barang', lazy='dynamic', cascade='all, delete-orphan')
    barang_kontrak = db.relationship('BarangKontrak', backref='barang', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Barang {self.kode_barang}: {self.nama_barang}>'
    
    def get_kontrak_list(self):
        """Dapatkan list kontrak yang terkait dengan barang ini"""
        return [bk.kontrak for bk in self.barang_kontrak]
    
    def get_total_qty_kontrak(self):
        """Total qty dari semua kontrak"""
        return sum(bk.qty_kontrak for bk in self.barang_kontrak)
    
    def to_dict(self):
        return {
            'id': self.id,
            'kode_barang': self.kode_barang,
            'nama_barang': self.nama_barang,
            'satuan': self.satuan,
            'kategori_id': self.kategori_id,
            'kategori': self.kategori.nama_kategori if self.kategori else None,
            'merk_id': self.merk_id,
            'merk': self.merk.nama_merk if self.merk else None,
            'spesifikasi': self.spesifikasi,
            'stok_awal': self.stok_awal,
            'stok_akhir': self.get_stok_akhir(),
            'jumlah_kontrak': self.barang_kontrak.count(),
            'total_qty_kontrak': self.get_total_qty_kontrak(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def get_stok_akhir(self):
        """Menghitung stok akhir berdasarkan transaksi"""
        total_masuk = db.session.query(db.func.sum(BarangMasuk.qty)).filter_by(kode_barang=self.kode_barang).scalar() or 0
        total_keluar = db.session.query(db.func.sum(BarangKeluar.qty)).filter_by(kode_barang=self.kode_barang).scalar() or 0
        return self.stok_awal + total_masuk - total_keluar


class BarangMasuk(db.Model):
    __tablename__ = 'barang_masuk'
    
    id = db.Column(db.Integer, primary_key=True)
    tanggal = db.Column(db.Date, nullable=False, index=True)
    kode_barang = db.Column(db.String(50), db.ForeignKey('barang.kode_barang', onupdate='CASCADE'), nullable=False, index=True)
    qty = db.Column(db.Integer, nullable=False)
    keterangan = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<BarangMasuk {self.kode_barang}: {self.qty}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'tanggal': self.tanggal.isoformat() if self.tanggal else None,
            'kode_barang': self.kode_barang,
            'nama_barang': self.barang.nama_barang if self.barang else None,
            'qty': self.qty,
            'keterangan': self.keterangan,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class BarangKeluar(db.Model):
    __tablename__ = 'barang_keluar'
    
    id = db.Column(db.Integer, primary_key=True)
    tanggal = db.Column(db.Date, nullable=False, index=True)
    kode_barang = db.Column(db.String(50), db.ForeignKey('barang.kode_barang', onupdate='CASCADE'), nullable=False, index=True)
    qty = db.Column(db.Integer, nullable=False)
    keterangan = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<BarangKeluar {self.kode_barang}: {self.qty}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'tanggal': self.tanggal.isoformat() if self.tanggal else None,
            'kode_barang': self.kode_barang,
            'nama_barang': self.barang.nama_barang if self.barang else None,
            'qty': self.qty,
            'keterangan': self.keterangan,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
