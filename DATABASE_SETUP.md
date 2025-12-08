"""
Panduan Setup Database MySQL
=============================

## Cara 1: Menggunakan MySQL Command Line

1. Login ke MySQL sebagai root:

   ```bash
   mysql -u root -p
   ```

2. Buat database dan user:

   ```sql
   CREATE DATABASE IF NOT EXISTS inventaris_gudang;

   CREATE USER IF NOT EXISTS 'aim'@'localhost' IDENTIFIED BY 'P@pua123';
   GRANT ALL PRIVILEGES ON inventaris_gudang.* TO 'aim'@'localhost';
   FLUSH PRIVILEGES;

   USE inventaris_gudang;
   SOURCE schema.sql;
   ```

3. Exit MySQL:
   ```sql
   EXIT;
   ```

## Cara 2: Menggunakan Python Script (Recommended)

Jalankan script init_db.py:

```bash
source venv/bin/activate
python init_db.py
```

## Cara 3: Menggunakan phpMyAdmin atau MySQL Workbench

1. Buka phpMyAdmin/MySQL Workbench
2. Import file `schema.sql`
3. Atau buat database manual dengan nama: `inventaris_gudang`

## Verifikasi Koneksi

Test koneksi database:

```bash
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); print('✅ Database connected!')"
```

## Troubleshooting

Jika error "Access denied":

- Pastikan MySQL server sudah running
- Cek username dan password di config/config.py
- Buat user MySQL baru jika perlu
