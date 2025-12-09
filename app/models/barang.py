from app import db
from datetime import datetime

class Barang(db.Model):
    __tablename__ = 'barang'
    
    id = db.Column(db.Integer, primary_key=True)
    kode_barang = db.Column(db.String(50), unique=True, nullable=False, index=True)
    nama_barang = db.Column(db.String(255), nullable=False)
    satuan = db.Column(db.String(50), nullable=False)
    satuan_kecil = db.Column(db.String(50), nullable=True, comment='Contoh: Pack (isi 10 buah)')
    kategori_id = db.Column(db.Integer, db.ForeignKey('kategori_barang.id'), nullable=True)
    merk_id = db.Column(db.Integer, db.ForeignKey('merk_barang.id'), nullable=True)
    jenis_barang = db.Column(db.Enum('inventaris', 'habis_pakai', name='jenis_barang_enum'), default='inventaris', nullable=False)
    spesifikasi = db.Column(db.Text, nullable=True)
    stok_awal = db.Column(db.Integer, default=0)
    stok_minimum = db.Column(db.Integer, default=0, comment='Alert jika stok dibawah ini')
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
            'satuan_kecil': self.satuan_kecil,
            'kategori_id': self.kategori_id,
            'kategori': self.kategori.nama_kategori if self.kategori else None,
            'merk_id': self.merk_id,
            'merk': self.merk.nama_merk if self.merk else None,
            'jenis_barang': self.jenis_barang,
            'spesifikasi': self.spesifikasi,
            'stok_awal': self.stok_awal,
            'stok_akhir': self.get_stok_akhir(),
            'stok_minimum': self.stok_minimum,
            'status_stok': self.get_status_stok(),
            'is_stok_rendah': self.is_stok_rendah(),
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
    
    def is_stok_rendah(self):
        """Cek apakah stok dibawah minimum (untuk barang habis pakai)"""
        if self.jenis_barang == 'habis_pakai' and self.stok_minimum > 0:
            return self.get_stok_akhir() <= self.stok_minimum
        return False
    
    def get_status_stok(self, stok_akhir=None):
        """Get status stok untuk display"""
        if self.jenis_barang == 'inventaris':
            return 'inventaris'
        
        # Gunakan parameter stok_akhir jika ada, kalau tidak hitung ulang
        stok = stok_akhir if stok_akhir is not None else self.get_stok_akhir()
        if stok == 0:
            return 'habis'
        elif self.stok_minimum > 0 and stok <= self.stok_minimum:
            return 'rendah'
        elif self.stok_minimum > 0 and stok <= self.stok_minimum * 2:
            return 'perlu_order'
        else:
            return 'aman'
    
    def prediksi_habis(self, periode_hari=30):
        """Prediksi kapan barang akan habis berdasarkan konsumsi rata-rata"""
        if self.jenis_barang != 'habis_pakai':
            return None
        
        from datetime import timedelta
        from sqlalchemy import func
        
        # Hitung rata-rata keluar per hari dalam periode tertentu
        end_date = datetime.now()
        start_date = end_date - timedelta(days=periode_hari)
        
        total_keluar = db.session.query(
            func.sum(BarangKeluar.qty)
        ).filter(
            BarangKeluar.kode_barang == self.kode_barang,
            BarangKeluar.tanggal >= start_date.date()
        ).scalar() or 0
        
        if total_keluar == 0:
            return None  # Tidak ada data konsumsi
        
        rata_rata_per_hari = total_keluar / periode_hari
        stok_sekarang = self.get_stok_akhir()
        
        if rata_rata_per_hari > 0:
            hari_tersisa = int(stok_sekarang / rata_rata_per_hari)
            tanggal_habis = datetime.now() + timedelta(days=hari_tersisa)
            return {
                'hari_tersisa': hari_tersisa,
                'tanggal_habis': tanggal_habis,
                'rata_rata_konsumsi': round(rata_rata_per_hari, 2)
            }
        
        return None


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
