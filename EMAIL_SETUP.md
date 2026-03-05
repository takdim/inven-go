# Panduan Setup Email Notification Sistem Inven-Go

## Overview
Sistem ini dilengkapi dengan fitur Email Notification untuk:
1. **Notifikasi Admin**: Ketika ada laporan kerusakan aset baru
2. **Notifikasi Pelapor**: Ketika status laporan kerusakan berubah
3. **Dashboard Monitoring**: Tampilan real-time laporan kerusakan untuk admin

## Setup Email Configuration

### 1. Konfigurasi Environment Variables

Edit file `.env` di root project dan tambahkan konfigurasi email:

```env
# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your_app_password_here
MAIL_DEFAULT_SENDER=inven-go@example.com
```

### 2. Menggunakan Gmail

Jika menggunakan Gmail, ikuti langkah berikut:

1. **Enable 2-Factor Authentication**
   - Buka https://myaccount.google.com
   - Pilih "Security" di menu sebelah kiri
   - Aktifkan "2-Step Verification"

2. **Generate App Password**
   - Kembali ke halaman Security
   - Cari "App passwords" (hanya muncul jika 2FA sudah aktif)
   - Pilih "Mail" dan "Windows Computer" (atau device yang digunakan)
   - Salin password yang dihasilkan
   - Gunakan password ini untuk `MAIL_PASSWORD`

3. **Contoh Konfigurasi Gmail**
   ```env
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=xxxx xxxx xxxx xxxx  # App password yang di-generate
   MAIL_DEFAULT_SENDER=your-email@gmail.com
   ```

### 3. Menggunakan Email Provider Lain

#### Outlook/Hotmail
```env
MAIL_SERVER=smtp-mail.outlook.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@outlook.com
MAIL_PASSWORD=your_password
MAIL_DEFAULT_SENDER=your-email@outlook.com
```

#### SendGrid
```env
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=apikey
MAIL_PASSWORD=your_sendgrid_api_key
MAIL_DEFAULT_SENDER=your-email@example.com
```

## Fitur Email Notification

### 1. Notifikasi Admin - Laporan Kerusakan Baru
- Dikirim ketika laporan kerusakan berstatus "terkirim"
- Penerima: Semua user dengan role "admin"
- Email berisi:
  - Detail pelapor dan lokasi
  - Jenis dan penyebab kerusakan
  - Link ke sistem untuk aksi lebih lanjut

### 2. Notifikasi Pelapor - Update Status
- Dikirim ketika status berubah ke "selesai" atau "ditolak"
- Penerima: User yang membuat laporan (jika punya email)
- Email berisi:
  - Status terbaru laporan
  - Detail lokasi dan jenis kerusakan

## Dashboard & Monitoring

### Dashboard Utama (`/dashboard`)
- **Notifikasi Alert**: Badge menunjukkan jumlah laporan pending
- **Tabel Laporan Terbaru**: 10 laporan kerusakan terbaru
- **Statistik Minggu Ini**: Jumlah laporan dalam 7 hari terakhir

### Halaman Monitoring (`/dashboard/laporan_kerusakan_monitor`)
**Hanya untuk Admin**

Fitur:
- Statistik laporan (Total, Pending, Selesai, Ditolak)
- Filter berdasarkan status
- Tabel lengkap dengan:
  - ID Laporan
  - Nama Pelapor
  - Lokasi
  - Jenis Kerusakan
  - Tanggal
  - Status
  - Aksi (Lihat Detail, Edit, Cetak PDF)
- Pagination (20 item per halaman)
- Real-time update statistik

## Struktur Email

### Email Notifikasi Admin

**Subject**: `[PENTING] Laporan Kerusakan Aset Baru - {Nama Pelapor}`

**Konten:**
- Alert visual dengan latar kuning
- Informasi detail laporan
- Link langsung ke sistem
- Status awal: "Menunggu Penanganan"

### Email Update Status

**Subject**: `Update: Laporan Kerusakan Sudah Ditangani` (atau "Ditolak")

**Konten:**
- Greeting personal dengan nama pelapor
- Status update message
- Detail lokasi dan jenis kerusakan
- Status baru dengan styling warna

## Testing

### 1. Test Email Sending
Jalankan command berikut di terminal dalam project:

```bash
python
>>> from app import create_app, db
>>> from app.models.laporan_kerusakan import LaporanKerusakan
>>> from app.utils.email_utils import send_laporan_kerusakan_notification
>>> app = create_app()
>>> 
>>> # Get a sample laporan
>>> with app.app_context():
...     laporan = LaporanKerusakan.query.first()
...     if laporan:
...         send_laporan_kerusakan_notification(laporan, app)
...         print("Email sent successfully!")
...     else:
...         print("No laporan found")
```

### 2. Test Email Configuration
```bash
python
>>> import os
>>> from app import create_app
>>> app = create_app()
>>> print(f"Mail Server: {app.config['MAIL_SERVER']}")
>>> print(f"Mail Port: {app.config['MAIL_PORT']}")
>>> print(f"Mail Username: {app.config['MAIL_USERNAME']}")
```

## Troubleshooting

### Email tidak terkirim
1. Cek konfigurasi di `.env`
2. Pastikan email dan password benar
3. Cek koneksi internet
4. Lihat log aplikasi untuk error messages

### SMTP Connection Error
- Pastikan MAIL_PORT sesuai dengan email provider
- Gmail: 587 (TLS) atau 465 (SSL)
- Outlook: 587
- Cek firewall/security settings

### Email masuk ke Spam
- Gunakan email dari domain resmi (bukan free account)
- Setup SPF, DKIM, DMARC records
- Gunakan service seperti SendGrid untuk reliabilitas lebih tinggi

### Admin tidak menerima email
- Pastikan user dengan role "admin" memiliki email di database
- Cek tabel users dan pastikan email field terisi
- Pastikan `is_active` status adalah True

## Production Recommendations

1. **Gunakan SendGrid atau Email Service Provider**
   - Lebih reliable dan tidak blocked
   - Built-in tracking dan analytics
   - Support dari provider

2. **Setup Background Job Queue**
   - Gunakan Celery untuk async email sending
   - Hindari blocking request
   - Retry mechanism untuk failed emails

3. **Monitor Email Delivery**
   - Setup bounce handling
   - Track unsubscribe
   - Monitor delivery rates

4. **Security**
   - Jangan hardcode credentials
   - Gunakan environment variables
   - Encrypt sensitive data

## File-File Terkait

- `app/utils/email_utils.py` - Email utility functions
- `config/config.py` - Email configuration
- `app/__init__.py` - Flask-Mail initialization
- `app/dashboard/routes.py` - Dashboard routes
- `app/aset_tetap/routes.py` - Laporan kerusakan routes
- `app/templates/dashboard/index.html` - Dashboard template
- `app/templates/dashboard/laporan_kerusakan_monitor.html` - Monitoring template

## API Functions

### send_laporan_kerusakan_notification(laporan, app=None)
Mengirim notifikasi ke admin saat laporan kerusakan baru dibuat

**Parameters:**
- `laporan`: Instance LaporanKerusakan
- `app`: Flask app instance (optional, menggunakan current_app jika None)

**Usage:**
```python
from app.utils.email_utils import send_laporan_kerusakan_notification
from flask import current_app

laporan = LaporanKerusakan(...)
send_laporan_kerusakan_notification(laporan, current_app)
```

### send_laporan_kerusakan_update(laporan, status_baru, app=None)
Mengirim notifikasi update status ke pelapor

**Parameters:**
- `laporan`: Instance LaporanKerusakan
- `status_baru`: Status baru ('selesai', 'ditolak', dll)
- `app`: Flask app instance (optional)

**Usage:**
```python
from app.utils.email_utils import send_laporan_kerusakan_update

send_laporan_kerusakan_update(laporan, 'selesai', current_app)
```
