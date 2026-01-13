CREATE DATABASE IF NOT EXISTS inventaris_gudang;
USE inventaris_gudang;

-- Tabel Data Barang (Master Data)
CREATE TABLE barang (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kode_barang VARCHAR(50) UNIQUE NOT NULL,
    nama_barang VARCHAR(255) NOT NULL,
    satuan VARCHAR(50) NOT NULL,
    stok_awal INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_kode_barang (kode_barang)
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
    spesifikasi TEXT,
    stok_awal INT DEFAULT 0,
    stok_minimum INT DEFAULT 0,
    nomor_kontrak VARCHAR(100),
    tanggal_kontrak DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_kode_aset (kode_aset)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabel Transaksi Barang Masuk
CREATE TABLE barang_masuk (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tanggal DATE NOT NULL,
    kode_barang VARCHAR(50) NOT NULL,
    qty INT NOT NULL,
    keterangan TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (kode_barang) REFERENCES barang(kode_barang) ON UPDATE CASCADE,
    INDEX idx_tanggal (tanggal),
    INDEX idx_kode_barang (kode_barang)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabel Transaksi Barang Keluar
CREATE TABLE barang_keluar (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tanggal DATE NOT NULL,
    kode_barang VARCHAR(50) NOT NULL,
    qty INT NOT NULL,
    keterangan TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (kode_barang) REFERENCES barang(kode_barang) ON UPDATE CASCADE,
    INDEX idx_tanggal (tanggal),
    INDEX idx_kode_barang (kode_barang)
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
