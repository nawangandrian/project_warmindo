<p align="center">
  <a href="https://flet.dev" target="_blank">
    <img src="https://raw.githubusercontent.com/flet-dev/flet/main/media/logo/flet-logo.svg" width="400" alt="Flet Logo">
  </a>
</p>

<p align="center">
  <a href="https://pypi.org/project/flet/"><img src="https://img.shields.io/pypi/dm/flet" alt="Total Downloads"></a>
  <a href="https://pypi.org/project/flet/"><img src="https://img.shields.io/pypi/v/flet" alt="Latest Stable Version"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
</p>

# Aplikasi Penjualan Warmindo Berbasis Flet

**"Solusi Modern untuk Kasir Warung Makan Indomie"**

Temukan kemudahan mengelola transaksi, pelanggan, dan laporan penjualan hanya dalam satu aplikasi!  
**Aplikasi Penjualan Warmindo** adalah sistem penjualan berbasis desktop (GUI) yang dibuat menggunakan **Flet (Python framework mirip Flutter)**.  
Cocok untuk digunakan pada **Warung Makan Indomie (Warmindo)** yang ingin digitalisasi proses penjualan mereka.

---

## Tentang Aplikasi

Aplikasi ini dirancang sebagai **sistem kasir berbasis peran (role-based)** dengan dua tipe pengguna utama, yaitu **Admin** dan **Kasir**, untuk memudahkan pengelolaan data, transaksi, serta laporan keuangan harian.

---

## Fitur Utama

### Role-based Access

Aplikasi memiliki dua jenis hak akses:

- **Admin**
  - Kelola Data Menu  
  - Kelola Kasir  
  - Kelola Pengguna  
  - Kelola Laporan Transaksi  
  - Akses Profil  

- **Kasir**
  - Kelola Pelanggan  
  - Kelola Transaksi  
  - Lihat Riwayat Transaksi  
  - Lihat Laporan Transaksi  
  - Akses Profil  

---


---

## Penjelasan File `main_hal_pengguna.py`

File ini merupakan inti dari aplikasi yang mengatur:

- **Navigasi antar halaman** menggunakan `NavigationRail`
- **Manajemen sesi pengguna** (menampilkan username dan hak akses)
- **Pemanggilan halaman dinamis** berdasarkan peran pengguna
- **Fitur logout** dengan dialog konfirmasi (`AlertDialog`)

---

## Alur Program

1. Saat pengguna berhasil login, data sesi disimpan melalui `session_manager.py`.  
2. Fungsi `main_hal_pengguna(page)` dijalankan untuk menampilkan halaman utama.  
3. Sistem menyesuaikan daftar halaman (`pages`) berdasarkan `hak_akses` pengguna.  
4. Navigasi antar halaman dikontrol menggunakan `NavigationRail`.  
5. Tombol **Keluar** akan memunculkan dialog konfirmasi.  
6. Jika dikonfirmasi, sesi dihapus dan pengguna kembali ke halaman login (`hal_awal.py`).  

---

## Contoh Tampilan Navigasi

| Peran | Menu Navigasi |
|-------|----------------|
| **Admin** | Beranda, Kelola Menu, Kelola Kasir, Kelola Pengguna, Laporan Transaksi, Profil |
| **Kasir** | Beranda, Kelola Pelanggan, Transaksi, Riwayat Transaksi, Laporan Transaksi, Profil |

---

## Screenshot Aplikasi

<p align="center">
  <img src="public/screenshots/dashboard.png" width="600" alt="Halaman Dashboard">
</p>

<p align="center">
  <img src="public/screenshots/transaksi.png" width="600" alt="Halaman Transaksi">
</p>

<p align="center">
  <img src="public/screenshots/laporan.png" width="600" alt="Halaman Laporan Transaksi">
</p>

---

## Instalasi dan Menjalankan Aplikasi

### Persyaratan

Pastikan sudah terpasang **Python 3.10+**
