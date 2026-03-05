# 🚀 Quick Start: Email Notification & Monitoring System

## Yang Telah Diimplementasikan

### 1. ✅ Email Notification System
- **Admin Notification**: Notifikasi otomatis ke admin saat ada laporan kerusakan baru
- **Pelapor Update**: Notifikasi ke pelapor saat status laporan berubah
- **Async Sending**: Email dikirim secara asynchronous agar tidak blocking aplikasi
- **HTML Templates**: Email dengan format HTML yang profesional

### 2. ✅ Dashboard Real-time Notifications
- **Laporan Pending Counter**: Badge menunjukkan jumlah laporan menunggu penanganan
- **Alert Box**: Alert merah otomatis muncul di dashboard jika ada laporan pending
- **Tabel Terbaru**: Menampilkan 10 laporan kerusakan terbaru
- **Weekly Stats**: Statistik laporan kerusakan dalam 7 hari terakhir

### 3. ✅ Admin Monitoring Page
- **URL**: `/dashboard/laporan_kerusakan_monitor`
- **Stats Cards**: Statistik lengkap (Total, Pending, Selesai, Ditolak)
- **Filter & Search**: Filter berdasarkan status laporan
- **Daftar Lengkap**: Tabel dengan pagination (20 item/halaman)
- **Quick Actions**: Tombol untuk Detail, Edit, dan Cetak PDF
- **One-Click Access**: Hanya untuk user dengan role admin

---

## 📋 Setup Instructions

### Step 1: Setup Email Configuration

1. **Edit file `.env` di root project:**

```env
# Email Configuration untuk Gmail
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your_app_password_here
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

2. **Untuk Gmail:**
   - Aktifkan 2-Factor Authentication di https://myaccount.google.com
   - Generate App Password (di Security settings)
   - Copy password dan paste ke `.env`

3. **Untuk Email Provider Lain:** Lihat `EMAIL_SETUP.md`

### Step 2: Update Admin Users dengan Email

1. Login ke aplikasi dengan akun admin
2. Edit profile admin untuk menambahkan email
3. Email diperlukan agar admin bisa menerima notifikasi

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Test Configuration

```bash
python test_email_setup.py
```

Output akan menunjukkan:
- ✓ Email configuration
- ✓ SMTP connection
- ✓ Admin users & emails

---

## 🎯 Fitur-Fitur Utama

### A. Dashboard Notifikasi (`/dashboard`)

**Alert Laporan Kerusakan:**
- Muncul otomatis jika ada laporan dengan status "terkirim"
- Menampilkan jumlah laporan pending
- Tombol link ke halaman monitoring

**Tabel Laporan Terbaru:**
- Menampilkan 10 laporan kerusakan terbaru
- Filter berdasarkan status
- Quick link untuk lihat detail

### B. Admin Monitoring (`/dashboard/laporan_kerusakan_monitor`)

**Statistik Cards:**
- Total Laporan: Semua laporan
- Menunggu Ditangani: Status "terkirim"
- Selesai Ditangani: Status "selesai"
- Ditolak: Status "ditolak"

**Filter & Search:**
```
Status Filter: Semua / Draft / Terkirim / Selesai / Ditolak
```

**Tabel Laporan:**
| ID | Pelapor | Lokasi | Jenis Kerusakan | Tanggal | Status | Aksi |
|---|---|---|---|---|---|---|
| #1 | Nama | Ruang A | Rusak... | 01 Jan | Terkirim | Edit, Detail, PDF |

**Aksi:**
- 👁️ Detail: Lihat laporan lengkap
- ✏️ Edit: Update status laporan
- 📄 PDF: Cetak laporan ke PDF

### C. Email Notification

**Email Admin - Laporan Baru:**
- Subject: `[PENTING] Laporan Kerusakan Aset Baru - {Nama Pelapor}`
- Penerima: Semua admin dengan email
- Konten: Detail lengkap laporan
- Action: Link ke sistem untuk penanganan

**Email Pelapor - Update Status:**
- Subject: `Update: Laporan Kerusakan Sudah Ditangani` (atau Ditolak)
- Penerima: User yang membuat laporan
- Konten: Status update dan detail laporan

---

## 📁 File-File yang Dibuat/Diubah

### File Baru:
```
✓ app/utils/email_utils.py           # Email utility functions
✓ app/templates/dashboard/laporan_kerusakan_monitor.html  # Monitoring page
✓ EMAIL_SETUP.md                      # Dokumentasi setup email
✓ test_email_setup.py                 # Testing script
✓ QUICK_START.md                      # File ini
```

### File yang Diupdate:
```
✓ requirements.txt                    # +Flask-Mail==0.9.1
✓ config/config.py                    # +Email configuration
✓ app/__init__.py                     # +Flask-Mail initialization
✓ app/dashboard/routes.py            # +Notifikasi & monitoring routes
✓ app/aset_tetap/routes.py           # +Email sending di laporan routes
✓ app/templates/dashboard/index.html  # +Notifikasi section
```

---

## 🧪 Testing

### Test 1: Verifikasi Konfigurasi
```bash
python test_email_setup.py
```

### Test 2: Manual Testing via Python Shell
```python
from app import create_app, db
from app.models.laporan_kerusakan import LaporanKerusakan
from app.utils.email_utils import send_laporan_kerusakan_notification

app = create_app()
with app.app_context():
    laporan = LaporanKerusakan.query.first()
    if laporan:
        send_laporan_kerusakan_notification(laporan, app)
        print("✓ Email sent!")
```

### Test 3: Test di Aplikasi
1. Buat laporan kerusakan baru dengan status "terkirim"
2. Email akan dikirim ke admin secara otomatis
3. Cek email admin untuk memverifikasi

---

## 🔧 Troubleshooting

### Email tidak terkirim
- [ ] Cek `.env` file - pastikan credentials benar
- [ ] Jalankan `test_email_setup.py` untuk diagnosa
- [ ] Cek log aplikasi untuk error messages
- [ ] Pastikan admin user punya email

### SMTP Connection Error
- [ ] Verify `MAIL_SERVER` dan `MAIL_PORT` sesuai provider
- [ ] Gmail: 587 (TLS), Outlook: 587
- [ ] Cek firewall/proxy settings
- [ ] Pastikan password benar

### Email masuk ke Spam
- [ ] Gunakan domain email resmi
- [ ] Jangan gunakan free email account untuk production
- [ ] Gunakan SendGrid atau service provider untuk reliabilitas

---

## 🎓 API Usage

### Mengirim Notifikasi Laporan Baru
```python
from app.utils.email_utils import send_laporan_kerusakan_notification
from flask import current_app

laporan = LaporanKerusakan(...)
db.session.add(laporan)
db.session.commit()

# Kirim notifikasi ke admin
if laporan.status == 'terkirim':
    send_laporan_kerusakan_notification(laporan, current_app)
```

### Mengirim Notifikasi Update Status
```python
from app.utils.email_utils import send_laporan_kerusakan_update

# Ketika status berubah
status_lama = 'draft'
status_baru = 'selesai'

if status_baru in ('selesai', 'ditolak'):
    send_laporan_kerusakan_update(laporan, status_baru, current_app)
```

---

## 📊 Monitoring Dashboard Flow

```
┌─────────────────────────────┐
│   Dashboard Utama           │
│  /dashboard                 │
└────────────┬────────────────┘
             │
             ├─ Alert Notifikasi
             │  (jika laporan_pending > 0)
             │
             ├─ Statistik Cards
             │  (Total, Barang, Transaksi, Aset)
             │
             ├─ Tabel Laporan Terbaru
             │  (10 laporan terakhir)
             │
             ↓
┌─────────────────────────────┐
│   Admin Monitoring          │
│  /dashboard/laporan_kerusakan
│  _monitor (Admin Only)      │
│                             │
│  - Stats Cards (4 metric)   │
│  - Filter by Status         │
│  - Table dengan Pagination  │
│  - Quick Actions            │
└─────────────────────────────┘
```

---

## 📞 Production Checklist

- [ ] Email credentials di `.env` (jangan di-commit)
- [ ] Admin users memiliki email
- [ ] Test email dikirim dengan benar
- [ ] Email tidak masuk spam
- [ ] Monitoring page bisa diakses admin
- [ ] Dashboard alerts muncul
- [ ] Backup email configuration
- [ ] Setup monitoring untuk delivery rate
- [ ] Document email sender address

---

## 📚 Dokumentasi Lengkap

Lihat file `EMAIL_SETUP.md` untuk dokumentasi lebih detail tentang:
- Setup untuk berbagai email provider
- Troubleshooting guide
- Production recommendations
- API documentation

---

## ✨ Next Steps (Optional)

Fitur tambahan yang bisa ditambahkan:

1. **SMS Notification**
   - Notifikasi via SMS untuk laporan sangat urgent
   - Gunakan Twilio API

2. **Push Notification**
   - Real-time push ke admin device
   - Gunakan Firebase

3. **Email Template Builder**
   - Custom email templates
   - Drag & drop editor

4. **Delivery Report**
   - Track email delivery status
   - Bounce handling
   - Analytics

5. **Scheduled Reports**
   - Daily/Weekly summary reports
   - Statistics and trends

---

**Created:** February 2025
**Version:** 1.0
**Status:** Ready for Production

Untuk bantuan lebih lanjut, silakan baca `EMAIL_SETUP.md`
