#!/usr/bin/env python
"""
Migration script to add nama_pengguna column to aset_tetap table
"""

import sys
sys.path.insert(0, '/root/inven-go')

from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    try:
        # Check if column already exists
        result = db.session.execute(text("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME='aset_tetap' AND COLUMN_NAME='nama_pengguna'
        """))
        
        if result.fetchone():
            print("✓ Column nama_pengguna already exists!")
        else:
            # Add the column
            db.session.execute(text("""
                ALTER TABLE aset_tetap 
                ADD COLUMN nama_pengguna VARCHAR(255) COMMENT 'Nama pengguna/pemakai aset' 
                AFTER tempat_penggunaan
            """))
            db.session.commit()
            print("✓ Column nama_pengguna added successfully!")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        db.session.rollback()
        sys.exit(1)
