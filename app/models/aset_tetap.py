from app import db
from datetime import datetime

class AsetTetap(db.Model):
    __tablename__ = 'aset_tetap'
    
    id = db.Column(db.Integer, primary_key=True)
    kode_aset = db.Column(db.String(50), unique=True, nullable=False, index=True)
    nama_aset = db.Column(db.String(255), nullable=False)
    kategori_id = db.Column(db.Integer, db.ForeignKey('kategori_barang.id'))
    merk_id = db.Column(db.Integer, db.ForeignKey('merk_barang.id'))
    merk_aset_tetap_id = db.Column(db.Integer, db.ForeignKey('merk_aset_tetap.id'))
    spesifikasi = db.Column(db.Text)
    satuan = db.Column(db.String(50))
    satuan_kecil = db.Column(db.String(50), comment='Contoh: Pack (isi 10 unit)')
    nomor_kontrak = db.Column(db.String(100))
    tanggal_kontrak = db.Column(db.Date)
    kontrak_spk = db.Column(db.String(200), comment='Nomor kontrak/SPK')
    tempat_penggunaan = db.Column(db.String(255), comment='Lokasi penggunaan aset')
    nama_pengguna = db.Column(db.String(255), comment='Nama pengguna/pemakai aset')
    total_barang = db.Column(db.Integer, default=0, comment='Total jumlah barang')
    stok_awal = db.Column(db.Integer, default=0)
    stok_minimum = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    kategori = db.relationship('KategoriBarang', foreign_keys=[kategori_id], backref='aset_tetap_list')
    merk = db.relationship('MerkBarang', foreign_keys=[merk_id], backref='aset_tetap_list')
    merk_aset_tetap = db.relationship('MerkAsetTetap', foreign_keys=[merk_aset_tetap_id], backref='aset_tetap_list')
    laporan_kerusakan = db.relationship(
        'LaporanKerusakan',
        backref='aset_tetap',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    def __repr__(self):
        return f'<AsetTetap {self.kode_aset}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'kode_aset': self.kode_aset,
            'nama_aset': self.nama_aset,
            'kategori_id': self.kategori_id,
            'merk_id': self.merk_id,
            'spesifikasi': self.spesifikasi,
            'satuan': self.satuan,
            'satuan_kecil': self.satuan_kecil,
            'nomor_kontrak': self.nomor_kontrak,
            'tanggal_kontrak': self.tanggal_kontrak.isoformat() if self.tanggal_kontrak else None,
            'kontrak_spk': self.kontrak_spk,
            'tempat_penggunaan': self.tempat_penggunaan,
            'stok_awal': self.stok_awal,
            'stok_minimum': self.stok_minimum
        }
