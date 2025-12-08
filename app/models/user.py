from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    nama_lengkap = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, index=True)
    role = db.Column(db.Enum('admin', 'staff', 'viewer', name='user_roles'), default='staff')
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    logs = db.relationship('UserLog', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash password sebelum disimpan"""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifikasi password"""
        return check_password_hash(self.password, password)
    
    def update_last_login(self):
        """Update waktu login terakhir"""
        self.last_login = datetime.utcnow()
        db.session.commit()
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'nama_lengkap': self.nama_lengkap,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def has_role(self, role):
        """Check apakah user memiliki role tertentu"""
        return self.role == role
    
    def is_admin(self):
        """Check apakah user adalah admin"""
        return self.role == 'admin'


class UserLog(db.Model):
    __tablename__ = 'user_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    activity = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    ip_address = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<UserLog {self.user_id}: {self.activity}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.user.username if self.user else None,
            'activity': self.activity,
            'description': self.description,
            'ip_address': self.ip_address,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @staticmethod
    def log_activity(user_id, activity, description=None, ip_address=None):
        """Helper method untuk membuat log aktivitas"""
        log = UserLog(
            user_id=user_id,
            activity=activity,
            description=description,
            ip_address=ip_address
        )
        db.session.add(log)
        db.session.commit()
        return log
