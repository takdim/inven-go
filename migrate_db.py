#!/usr/bin/env python
"""
Database migration script to add nama_pengguna column to aset_tetap table
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db

def migrate():
    """Add nama_pengguna column to aset_tetap table if it doesn't exist"""
    app = create_app()
    
    with app.app_context():
        try:
            # Check if column exists
            from sqlalchemy import inspect, text
            inspector = inspect(db.engine)
            columns = [c['name'] for c in inspector.get_columns('aset_tetap')]
            
            if 'nama_pengguna' not in columns:
                print("Adding nama_pengguna column to aset_tetap table...")
                sql = """
                ALTER TABLE aset_tetap 
                ADD COLUMN nama_pengguna VARCHAR(255) 
                COMMENT 'Nama pengguna/pemakai aset' 
                AFTER tempat_penggunaan
                """
                db.session.execute(text(sql))
                db.session.commit()
                print("✓ Successfully added nama_pengguna column")
            else:
                print("✓ Column nama_pengguna already exists")
                
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            db.session.rollback()
            sys.exit(1)

if __name__ == '__main__':
    migrate()
