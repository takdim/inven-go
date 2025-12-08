"""
Script untuk reset password admin atau membuat user baru
Jalankan: python reset_admin.py
"""
from app import create_app, db
from app.models.user import User

def reset_admin_password():
    app = create_app()
    
    with app.app_context():
        # Cari user admin
        admin = User.query.filter_by(username='admin').first()
        
        if admin:
            print("✅ User admin ditemukan!")
            print(f"   Username: {admin.username}")
            print(f"   Email: {admin.email}")
            print(f"   Nama: {admin.nama_lengkap}")
            
            # Reset password
            new_password = 'admin123'
            admin.set_password(new_password)
            admin.is_active = True
            db.session.commit()
            
            print(f"\n✅ Password admin berhasil direset!")
            print(f"   Username: admin")
            print(f"   Password: {new_password}")
            print(f"   ⚠️  SEGERA GANTI PASSWORD SETELAH LOGIN!")
        else:
            print("❌ User admin tidak ditemukan. Membuat user admin baru...")
            
            # Buat user admin baru
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
            
            print("✅ User admin berhasil dibuat!")
            print("   Username: admin")
            print("   Password: admin123")
            print("   ⚠️  SEGERA GANTI PASSWORD SETELAH LOGIN!")

if __name__ == '__main__':
    reset_admin_password()
