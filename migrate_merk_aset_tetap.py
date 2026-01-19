#!/usr/bin/env python
"""
Script untuk menambah tabel merk_aset_tetap dan kolom merk_aset_tetap_id ke tabel aset_tetap
"""
from app import create_app, db
from app.models.merk_aset_tetap import MerkAsetTetap

app = create_app()

with app.app_context():
    # Create the new table
    try:
        # Create merk_aset_tetap table
        db.create_all()
        
        # Check if column exists in aset_tetap table
        inspector = db.inspect(db.engine)
        aset_tetap_columns = [col['name'] for col in inspector.get_columns('aset_tetap')]
        
        if 'merk_aset_tetap_id' not in aset_tetap_columns:
            # Add the column if it doesn't exist
            with db.engine.connect() as conn:
                conn.execute(db.text("""
                    ALTER TABLE aset_tetap 
                    ADD COLUMN merk_aset_tetap_id INT,
                    ADD FOREIGN KEY (merk_aset_tetap_id) REFERENCES merk_aset_tetap(id)
                """))
                conn.commit()
            print("✓ Kolom merk_aset_tetap_id ditambahkan ke tabel aset_tetap")
        else:
            print("✓ Kolom merk_aset_tetap_id sudah ada")
        
        # Check if kontrak_spk and tempat_penggunaan columns exist
        if 'kontrak_spk' not in aset_tetap_columns:
            with db.engine.connect() as conn:
                conn.execute(db.text("""
                    ALTER TABLE aset_tetap 
                    ADD COLUMN kontrak_spk VARCHAR(200)
                """))
                conn.commit()
            print("✓ Kolom kontrak_spk ditambahkan ke tabel aset_tetap")
        
        if 'tempat_penggunaan' not in aset_tetap_columns:
            with db.engine.connect() as conn:
                conn.execute(db.text("""
                    ALTER TABLE aset_tetap 
                    ADD COLUMN tempat_penggunaan VARCHAR(255)
                """))
                conn.commit()
            print("✓ Kolom tempat_penggunaan ditambahkan ke tabel aset_tetap")
        
        print("\n✓ Migrasi database berhasil!")
        print("✓ Tabel merk_aset_tetap sudah siap digunakan")
        print("✓ Anda dapat mengakses 'Data Merk Aset Tetap' di Master Data menu")
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        print("Silakan jalankan manual migration atau lihat DATABASE_SETUP.md")
