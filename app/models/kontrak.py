from app import db
from datetime import datetime

class KontrakBarang(db.Model):
    __tablename__ = 'kontrak_barang'
    
    id = db.Column(db.Integer, primary_key=True)
    nomor_kontrak = db.Column(db.String(100), unique=True, nullable=False, index=True)
    tanggal_kontrak = db.Column(db.Date, nullable=False)
    deskripsi = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    barang_kontrak = db.relationship('BarangKontrak', backref='kontrak', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<KontrakBarang {self.nomor_kontrak}>'
    
    def get_total_nilai(self):
        """Hitung total nilai kontrak"""
        total = 0
        for bk in self.barang_kontrak:
            if bk.harga_satuan:
                total += bk.qty_kontrak * float(bk.harga_satuan)
        return total
    
    def get_total_qty(self):
        """Hitung total qty barang dalam kontrak"""
        return sum(bk.qty_kontrak for bk in self.barang_kontrak)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nomor_kontrak': self.nomor_kontrak,
            'tanggal_kontrak': self.tanggal_kontrak.isoformat() if self.tanggal_kontrak else None,
            'deskripsi': self.deskripsi,
            'jumlah_barang': self.barang_kontrak.count(),
            'total_qty': self.get_total_qty(),
            'total_nilai': self.get_total_nilai(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class BarangKontrak(db.Model):
    __tablename__ = 'barang_kontrak'
    
    id = db.Column(db.Integer, primary_key=True)
    barang_id = db.Column(db.Integer, db.ForeignKey('barang.id', ondelete='CASCADE'), nullable=False, index=True)
    kontrak_id = db.Column(db.Integer, db.ForeignKey('kontrak_barang.id', ondelete='CASCADE'), nullable=False, index=True)
    qty_kontrak = db.Column(db.Integer, nullable=False)
    harga_satuan = db.Column(db.Numeric(15, 2), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint
    __table_args__ = (
        db.UniqueConstraint('barang_id', 'kontrak_id', name='unique_barang_kontrak'),
    )
    
    def __repr__(self):
        return f'<BarangKontrak B:{self.barang_id} K:{self.kontrak_id}>'
    
    def get_total_nilai(self):
        """Hitung total nilai (qty * harga)"""
        if self.harga_satuan:
            return self.qty_kontrak * float(self.harga_satuan)
        return 0
    
    def to_dict(self):
        return {
            'id': self.id,
            'barang_id': self.barang_id,
            'barang_kode': self.barang.kode_barang if self.barang else None,
            'barang_nama': self.barang.nama_barang if self.barang else None,
            'kontrak_id': self.kontrak_id,
            'nomor_kontrak': self.kontrak.nomor_kontrak if self.kontrak else None,
            'qty_kontrak': self.qty_kontrak,
            'harga_satuan': float(self.harga_satuan) if self.harga_satuan else None,
            'total_nilai': self.get_total_nilai(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
