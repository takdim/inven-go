#!/usr/bin/env python
"""
Direct SQL migration to add nama_pengguna column
"""
import pymysql

try:
    conn = pymysql.connect(
        host='127.0.0.1',
        user='aim',
        password='',
        database='inventaris_gudang'
    )
    
    cursor = conn.cursor()
    
    # Check if column exists
    cursor.execute("""
        SELECT COLUMN_NAME 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME='aset_tetap' AND COLUMN_NAME='nama_pengguna'
    """)
    
    if cursor.fetchone():
        print("✓ Column nama_pengguna already exists!")
    else:
        # Add the column
        cursor.execute("""
            ALTER TABLE aset_tetap 
            ADD COLUMN nama_pengguna VARCHAR(255) COMMENT 'Nama pengguna/pemakai aset' 
            AFTER tempat_penggunaan
        """)
        conn.commit()
        print("✓ Column nama_pengguna added successfully!")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"✗ Error: {e}")
