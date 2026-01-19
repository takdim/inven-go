CREATE DATABASE IF NOT EXISTS inventaris_gudang;
USE inventaris_gudang;

-- Tabel Kategori Barang
CREATE TABLE kategori_barang (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_kategori VARCHAR(100) UNIQUE NOT NULL,
    deskripsi TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabel Merk Barang
CREATE TABLE merk_barang (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_merk VARCHAR(100) UNIQUE NOT NULL,
    tipe VARCHAR(100),
    tanggal_pengadaan DATE,
    nomor_kontrak VARCHAR(100),
    spesifikasi TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabel Merk Aset Tetap (Master Data)
CREATE TABLE merk_aset_tetap (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_merk VARCHAR(100) UNIQUE NOT NULL,
    tipe VARCHAR(100),
    tanggal_pengadaan DATE,
    nomor_kontrak VARCHAR(100),
    spesifikasi TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_nama_merk (nama_merk)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabel Kontrak Barang
CREATE TABLE kontrak_barang (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nomor_kontrak VARCHAR(100) UNIQUE NOT NULL,
    tanggal_kontrak DATE NOT NULL,
    deskripsi TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_nomor_kontrak (nomor_kontrak)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabel Data Barang (Master Data)
CREATE TABLE barang (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kode_barang VARCHAR(50) UNIQUE NOT NULL,
    nama_barang VARCHAR(255) NOT NULL,
    satuan VARCHAR(50) NOT NULL,
    stok_awal INT DEFAULT 0,
    kategori_id INT,
    merk_id INT,
    jenis_barang VARCHAR(50),
    stok_minimum INT DEFAULT 0,
    stok_maksimum INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (kategori_id) REFERENCES kategori_barang(id),
    FOREIGN KEY (merk_id) REFERENCES merk_barang(id),
    INDEX idx_kode_barang (kode_barang)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabel Barang Kontrak (junction table)
CREATE TABLE barang_kontrak (
    id INT AUTO_INCREMENT PRIMARY KEY,
    barang_id INT NOT NULL,
    kontrak_id INT NOT NULL,
    qty_kontrak INT NOT NULL,
    harga_satuan DECIMAL(12, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (barang_id) REFERENCES barang(id) ON DELETE CASCADE,
    FOREIGN KEY (kontrak_id) REFERENCES kontrak_barang(id) ON DELETE CASCADE,
    INDEX idx_barang_id (barang_id),
    INDEX idx_kontrak_id (kontrak_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabel Data Aset Tetap (Master Data)
CREATE TABLE aset_tetap (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kode_aset VARCHAR(50) UNIQUE NOT NULL,
    nama_aset VARCHAR(255) NOT NULL,
    satuan VARCHAR(50) NOT NULL,
    satuan_kecil VARCHAR(50),
    kategori_id INT,
    merk_id INT,
    merk_aset_tetap_id INT,
    spesifikasi TEXT,
    stok_awal INT DEFAULT 0,
    stok_minimum INT DEFAULT 0,
    nomor_kontrak VARCHAR(100),
    tanggal_kontrak DATE,
    kontrak_spk VARCHAR(200),
    tempat_penggunaan VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (merk_aset_tetap_id) REFERENCES merk_aset_tetap(id),
    INDEX idx_kode_aset (kode_aset)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabel Transaksi Barang Masuk
CREATE TABLE barang_masuk (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tanggal DATE NOT NULL,
    barang_id INT NOT NULL,
    qty INT NOT NULL,
    keterangan TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (barang_id) REFERENCES barang(id) ON DELETE CASCADE,
    INDEX idx_tanggal (tanggal),
    INDEX idx_barang_id (barang_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabel Transaksi Barang Keluar
CREATE TABLE barang_keluar (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tanggal DATE NOT NULL,
    barang_id INT NOT NULL,
    qty INT NOT NULL,
    keterangan TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (barang_id) REFERENCES barang(id) ON DELETE CASCADE,
    INDEX idx_tanggal (tanggal),
    INDEX idx_barang_id (barang_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- View untuk Stok Gudang (Menghitung otomatis)
CREATE VIEW vw_stok_gudang AS
SELECT 
    b.kode_barang,
    b.nama_barang,
    b.satuan,
    b.stok_awal,
    COALESCE(SUM(bm.qty), 0) as total_masuk,
    COALESCE(SUM(bk.qty), 0) as total_keluar,
    (b.stok_awal + COALESCE(SUM(bm.qty), 0) - COALESCE(SUM(bk.qty), 0)) as stok_akhir
FROM barang b
LEFT JOIN barang_masuk bm ON b.kode_barang = bm.kode_barang
LEFT JOIN barang_keluar bk ON b.kode_barang = bk.kode_barang
GROUP BY b.kode_barang, b.nama_barang, b.satuan, b.stok_awal;

-- Tabel User untuk Login
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    nama_lengkap VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    role ENUM('admin', 'staff', 'viewer') DEFAULT 'staff',
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabel untuk Log Aktivitas User (Opsional, untuk audit trail)
CREATE TABLE user_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    activity VARCHAR(255) NOT NULL,
    description TEXT,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
