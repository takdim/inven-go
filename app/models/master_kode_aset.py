from app import db
from datetime import datetime

class MasterKodeAset(db.Model):
    __tablename__ = 'master_kode_aset'
    
    id = db.Column(db.Integer, primary_key=True)
    kode_aset = db.Column(db.String(50), unique=True, nullable=False, index=True)
    deskripsi = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    aset_tetap = db.relationship('AsetTetap', backref='master_kode', lazy='dynamic')
    
    def __repr__(self):
        return f'<MasterKodeAset {self.kode_aset}>'
    
    def get_total_aset(self):
        """Get total jumlah aset dengan kode ini"""
        return self.aset_tetap.count()
    
    def to_dict(self):
        return {
            'id': self.id,
            'kode_aset': self.kode_aset,
            'deskripsi': self.deskripsi,
            'jumlah_aset': self.get_total_aset()
        }
