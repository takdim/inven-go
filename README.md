# Inven-Go

Sistem Manajemen Inventaris Gudang berbasis Flask dengan fitur lengkap untuk tracking barang, kontrak/SPK, dan transaksi masuk/keluar.

## 🚀 Fitur Utama

- **Manajemen Barang**: CRUD lengkap untuk data barang dengan kategori dan merk
- **Kontrak/SPK**: Kelola kontrak dengan relasi many-to-many ke barang
- **Transaksi**: Catat barang masuk dan keluar dengan tracking stok real-time
- **Laporan & Export**: Export data ke Excel dan PDF dengan filter yang fleksibel
- **Authentication**: Login/logout dengan user management
- **Dashboard**: Visualisasi data dengan chart dan statistik

## 📋 Teknologi yang Digunakan

- **Backend**: Flask 3.0.0, SQLAlchemy
- **Database**: MySQL 8.0
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF, WTForms
- **Export**: openpyxl, reportlab, weasyprint
- **Frontend**: Bootstrap 5.3.0, Font Awesome 6.4.0

## 🛠️ Instalasi

### 1. Clone Repository

```bash
git clone https://github.com/takdim/inven-go.git
cd inven-go
```

### 2. Buat Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate  # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Database

Buat database MySQL:

```sql
CREATE DATABASE inventaris_gudang;
```

Copy file .env.example menjadi .env dan sesuaikan konfigurasi:

```bash
cp .env.example .env
```

Edit file `.env`:

```
SECRET_KEY=your-secret-key-here
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=inventaris_gudang
```

### 5. Inisialisasi Database

```bash
python init_db.py
```

### 6. Reset Admin (Opsional)

```bash
python reset_admin.py
```

Default admin:

- Username: `admin`
- Password: `admin123`

### 7. Jalankan Aplikasi

```bash
python run.py
```

Akses aplikasi di: http://localhost:8000

## 📁 Struktur Project

```
inven-go/
├── app/
│   ├── auth/           # Authentication module
│   ├── barang/         # Barang/Item management
│   ├── dashboard/      # Dashboard & statistics
│   ├── kontrak/        # Kontrak/SPK management
│   ├── laporan/        # Reports & exports
│   ├── models/         # Database models
│   ├── routes/         # Main routes
│   ├── transaksi/      # Transaction management
│   ├── utils/          # Utilities (Excel, PDF export)
│   ├── static/         # CSS, JS, images
│   └── templates/      # HTML templates
├── config/
│   └── config.py       # Configuration
├── migrations/         # Database migrations (SQL)
├── tests/             # Unit tests
├── init_db.py         # Database initialization
├── reset_admin.py     # Reset admin user
├── requirements.txt   # Python dependencies
└── run.py            # Application entry point
```

## 📊 Database Schema

### Tabel Utama:

- `users` - User authentication
- `user_log` - User activity logs
- `barang` - Master data barang
- `kategori_barang` - Kategori barang
- `merk_barang` - Merk barang
- `kontrak_barang` - Kontrak/SPK
- `barang_kontrak` - Junction table (barang ↔ kontrak)
- `barang_masuk` - Transaksi barang masuk
- `barang_keluar` - Transaksi barang keluar

Lihat file `schema.sql` atau `DATABASE_SETUP.md` untuk detail lengkap.

## 🔧 Konfigurasi

### Development

Edit `config/config.py` atau gunakan environment variables di `.env`

### Production

⚠️ **Penting untuk Production:**

1. Set `SECRET_KEY` yang kuat
2. Set `SQLALCHEMY_ECHO = False`
3. Gunakan HTTPS
4. Gunakan strong password untuk database
5. Backup database secara berkala
6. Setup proper logging

## 📝 API Endpoints

### Authentication

- `GET/POST /login` - Login page
- `GET /logout` - Logout

### Dashboard

- `GET /dashboard` - Main dashboard

### Barang

- `GET /barang` - List barang
- `GET/POST /barang/tambah` - Add barang
- `GET/POST /barang/edit/<id>` - Edit barang
- `POST /barang/hapus/<id>` - Delete barang
- `GET /barang/<id>` - Detail barang

### Kontrak

- `GET /kontrak` - List kontrak
- `GET/POST /kontrak/tambah` - Add kontrak
- `GET/POST /kontrak/edit/<id>` - Edit kontrak
- `GET /kontrak/<id>` - Detail kontrak
- `POST /kontrak/<id>/tambah-barang` - Add item to kontrak
- `POST /kontrak/<kontrak_id>/hapus-barang/<id>` - Remove item

### Transaksi

- `GET/POST /transaksi/masuk` - Barang masuk
- `GET/POST /transaksi/keluar` - Barang keluar

### Laporan

- `GET /laporan` - Report dashboard
- `GET /laporan/barang` - Laporan barang
- `GET /laporan/barang/export-excel` - Export barang to Excel
- `GET /laporan/barang/export-pdf` - Export barang to PDF
- `GET /laporan/kontrak` - Laporan kontrak
- `GET /laporan/transaksi-masuk` - Laporan barang masuk
- `GET /laporan/transaksi-keluar` - Laporan barang keluar

## 🧪 Testing

```bash
pytest tests/
```

## 📄 License

MIT License

## 👥 Contributors

- [takdim](https://github.com/takdim)

## 🐛 Bug Reports & Feature Requests

Silakan buat issue di: https://github.com/takdim/inven-go/issues

## 📞 Contact

Untuk pertanyaan lebih lanjut, silakan hubungi melalui GitHub issues.
