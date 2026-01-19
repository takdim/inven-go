from app import db
from datetime import datetime

class MerkAsetTetap(db.Model):
    __tablename__ = 'merk_aset_tetap'
    
    id = db.Column(db.Integer, primary_key=True)
    nama_merk = db.Column(db.String(100), unique=True, nullable=False, index=True)
    tipe = db.Column(db.String(100), nullable=True)
    tanggal_pengadaan = db.Column(db.Date, nullable=True)
    nomor_kontrak = db.Column(db.String(100), nullable=True)
    spesifikasi = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<MerkAsetTetap {self.nama_merk}>'
    
    def get_total_aset(self):
        """Get total jumlah aset dengan merk ini"""
        from app.models.aset_tetap import AsetTetap
        return AsetTetap.query.filter_by(merk_aset_tetap_id=self.id).count()
    
    def get_total_aset_by_criteria(self):
        """Get total jumlah aset berdasarkan nama_merk, tipe, dan kontrak_spk"""
        from app.models.aset_tetap import AsetTetap
        count = AsetTetap.query.filter(
            AsetTetap.merk_aset_tetap_id == self.id,
            AsetTetap.kontrak_spk == self.nomor_kontrak
        ).count()
        return count if count > 0 else AsetTetap.query.filter_by(merk_aset_tetap_id=self.id).count()
    
    def to_dict(self):
        return {
            'id': self.id,
            'nama_merk': self.nama_merk,
            'tipe': self.tipe,
            'tanggal_pengadaan': self.tanggal_pengadaan.isoformat() if self.tanggal_pengadaan else None,
            'nomor_kontrak': self.nomor_kontrak,
            'spesifikasi': self.spesifikasi,
            'jumlah_aset': self.get_total_aset(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

