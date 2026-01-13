from app import db
from datetime import datetime

class AsetTetap(db.Model):
    __tablename__ = 'aset_tetap'
    
    id = db.Column(db.Integer, primary_key=True)
    kode_aset = db.Column(db.String(50), unique=True, nullable=False, index=True)
    nama_aset = db.Column(db.String(255), nullable=False)
    satuan = db.Column(db.String(50), nullable=False)
    satuan_kecil = db.Column(db.String(50), nullable=True, comment='Contoh: Pack (isi 10 buah)')
    kategori_id = db.Column(db.Integer, db.ForeignKey('kategori_barang.id'), nullable=True)
    merk_id = db.Column(db.Integer, db.ForeignKey('merk_barang.id'), nullable=True)
    spesifikasi = db.Column(db.Text, nullable=True)
    stok_awal = db.Column(db.Integer, default=0)
    stok_minimum = db.Column(db.Integer, default=0, comment='Alert jika stok dibawah ini')
    nomor_kontrak = db.Column(db.String(100), nullable=True)
    tanggal_kontrak = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    kategori = db.relationship('KategoriBarang', backref='aset_tetap_kategori')
    merk = db.relationship('MerkBarang', backref='aset_tetap_merk')
    
    def __repr__(self):
        return f'<AsetTetap {self.kode_aset}: {self.nama_aset}>'
    
    def get_stok_akhir(self):
        """Hitung stok akhir dari transaksi masuk dan keluar"""
        from app.models.barang import BarangMasuk, BarangKeluar
        
        total_masuk = db.session.query(db.func.sum(BarangMasuk.qty_masuk)).filter(
            BarangMasuk.aset_tetap_id == self.id
        ).scalar() or 0
        
        total_keluar = db.session.query(db.func.sum(BarangKeluar.qty_keluar)).filter(
            BarangKeluar.aset_tetap_id == self.id
        ).scalar() or 0
        
        return self.stok_awal + total_masuk - total_keluar
    
    def to_dict(self):
        return {
            'id': self.id,
            'kode_aset': self.kode_aset,
            'nama_aset': self.nama_aset,
            'satuan': self.satuan,
            'satuan_kecil': self.satuan_kecil,
            'kategori_id': self.kategori_id,
            'kategori': self.kategori.nama_kategori if self.kategori else None,
            'merk_id': self.merk_id,
            'merk': self.merk.nama_merk if self.merk else None,
            'spesifikasi': self.spesifikasi,
            'stok_awal': self.stok_awal,
            'stok_akhir': self.get_stok_akhir(),
            'stok_minimum': self.stok_minimum,
            'nomor_kontrak': self.nomor_kontrak,
            'tanggal_kontrak': self.tanggal_kontrak,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }
