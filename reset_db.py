"""
Script untuk reset database - drop dan recreate semua tabel
Jalankan: python reset_db.py
"""
from app import create_app, db
from sqlalchemy import text
from app.models import User, Barang, BarangMasuk, BarangKeluar, UserLog, KategoriBarang, MerkBarang, KontrakBarang, BarangKontrak, AsetTetap

def reset_database():
    app = create_app()
    
    with app.app_context():
        # Disable foreign key checks
        db.session.execute(text('SET FOREIGN_KEY_CHECKS=0'))
        db.session.commit()
        
        # Drop all tables
        print("Dropping all tables...")
        db.drop_all()
        print("[OK] All tables dropped!")
        
        # Enable foreign key checks
        db.session.execute(text('SET FOREIGN_KEY_CHECKS=1'))
        db.session.commit()
        
        # Create all tables
        print("Creating database tables...")
        db.create_all()
        print("[OK] Database tables created successfully!")
        
        # Create default admin user
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("Creating default admin user...")
            admin = User(
                username='admin',
                nama_lengkap='Administrator',
                email='admin@inventaris.com',
                role='admin',
                is_active=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("[OK] Admin user created (username: admin, password: admin123)")
        else:
            print("[INFO] Admin user already exists.")
        
        print("\n[OK] Database reset completed!")

if __name__ == '__main__':
    reset_database()
