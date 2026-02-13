#!/usr/bin/env python
"""
Create laporan_kerusakan table if it does not exist.
Run: python migrate_laporan_kerusakan.py
"""

import sys

from sqlalchemy import inspect, text

from app import create_app, db


def migrate():
    app = create_app()

    with app.app_context():
        try:
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()

            if 'laporan_kerusakan' in tables:
                print("[OK] Table laporan_kerusakan already exists.")
                return

            if 'aset_tetap' not in tables or 'users' not in tables:
                print("[ERROR] Required tables not found: aset_tetap and users must exist first.")
                sys.exit(1)

            db.session.execute(text("""
                CREATE TABLE laporan_kerusakan (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    aset_tetap_id INT NOT NULL,
                    pelapor_id INT NULL,
                    tanggal_diketahui_rusak DATE NOT NULL,
                    nama_pengguna VARCHAR(255) NOT NULL,
                    lokasi VARCHAR(255) NOT NULL,
                    jumlah INT NOT NULL DEFAULT 1,
                    jenis_kerusakan TEXT NOT NULL,
                    penyebab TEXT,
                    tindakan TEXT,
                    kondisi_saat_ini TEXT,
                    dampak TEXT,
                    status ENUM('draft', 'terkirim', 'selesai') NOT NULL DEFAULT 'draft',
                    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (aset_tetap_id) REFERENCES aset_tetap(id) ON DELETE CASCADE,
                    FOREIGN KEY (pelapor_id) REFERENCES users(id) ON DELETE SET NULL,
                    INDEX idx_laporan_kerusakan_aset_tetap_id (aset_tetap_id),
                    INDEX idx_laporan_kerusakan_pelapor_id (pelapor_id),
                    INDEX idx_laporan_kerusakan_status (status),
                    INDEX idx_laporan_kerusakan_created_at (created_at)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """))
            db.session.commit()

            print("[OK] Table laporan_kerusakan created successfully.")
        except Exception as exc:
            db.session.rollback()
            print(f"[ERROR] Migration failed: {exc}")
            sys.exit(1)


if __name__ == '__main__':
    migrate()
