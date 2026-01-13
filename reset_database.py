"""
Script untuk drop semua tabel dan membuat ulang database
Jalankan: python reset_database.py
"""
from app import create_app, db
from app.models import User, Barang, BarangMasuk, BarangKeluar, UserLog, AsetTetap, KategoriBarang, MerkBarang

def reset_database():
    app = create_app()
    
    with app.app_context():
        print("Dropping all tables...")
        db.drop_all()
        print("✅ All tables dropped!")
        
        print("Creating database tables...")
        db.create_all()
        print("✅ Database tables created successfully!")
        
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
            admin.set_password('admin123')  # Ganti password ini!
            db.session.add(admin)
            db.session.commit()
            print("✅ Default admin user created!")
            print("   Username: admin")
            print("   Password: admin123")
            print("   ⚠️  SEGERA GANTI PASSWORD SETELAH LOGIN!")
        else:
            print("ℹ️  Admin user already exists.")
        
        print("\n✅ Database reset completed!")

if __name__ == '__main__':
    reset_database()
