#!/usr/bin/env python
"""
Script untuk update tabel merk_aset_tetap dengan kolom tambahan seperti merk_barang
"""
from app import create_app, db

app = create_app()

with app.app_context():
    try:
        # Check if columns exist in merk_aset_tetap table
        inspector = db.inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns('merk_aset_tetap')]
        
        # Add tipe column if it doesn't exist
        if 'tipe' not in columns:
            with db.engine.connect() as conn:
                conn.execute(db.text("""
                    ALTER TABLE merk_aset_tetap 
                    ADD COLUMN tipe VARCHAR(100)
                """))
                conn.commit()
            print("✓ Kolom tipe ditambahkan ke tabel merk_aset_tetap")
        
        # Add tanggal_pengadaan column if it doesn't exist
        if 'tanggal_pengadaan' not in columns:
            with db.engine.connect() as conn:
                conn.execute(db.text("""
                    ALTER TABLE merk_aset_tetap 
                    ADD COLUMN tanggal_pengadaan DATE
                """))
                conn.commit()
            print("✓ Kolom tanggal_pengadaan ditambahkan ke tabel merk_aset_tetap")
        
        # Add nomor_kontrak column if it doesn't exist
        if 'nomor_kontrak' not in columns:
            with db.engine.connect() as conn:
                conn.execute(db.text("""
                    ALTER TABLE merk_aset_tetap 
                    ADD COLUMN nomor_kontrak VARCHAR(100)
                """))
                conn.commit()
            print("✓ Kolom nomor_kontrak ditambahkan ke tabel merk_aset_tetap")
        
        # Add spesifikasi column if it doesn't exist
        if 'spesifikasi' not in columns:
            with db.engine.connect() as conn:
                conn.execute(db.text("""
                    ALTER TABLE merk_aset_tetap 
                    ADD COLUMN spesifikasi TEXT
                """))
                conn.commit()
            print("✓ Kolom spesifikasi ditambahkan ke tabel merk_aset_tetap")
        
        # Drop keterangan column if it exists
        if 'keterangan' in columns:
            with db.engine.connect() as conn:
                conn.execute(db.text("""
                    ALTER TABLE merk_aset_tetap 
                    DROP COLUMN keterangan
                """))
                conn.commit()
            print("✓ Kolom keterangan dihapus dari tabel merk_aset_tetap")
        
        print("\n✓ Update database berhasil!")
        print("✓ Tabel merk_aset_tetap sekarang memiliki struktur sama seperti merk_barang")
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
