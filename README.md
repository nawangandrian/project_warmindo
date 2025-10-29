```markdown
# Aplikasi Penjualan Warmindo Berbasis Flet

Aplikasi ini merupakan **sistem penjualan berbasis desktop (GUI)** yang dibuat menggunakan **Flet (Python framework untuk membuat aplikasi seperti Flutter)**.  
Aplikasi ini digunakan untuk mengelola transaksi, data menu, pengguna, kasir, pelanggan, serta laporan penjualan pada **Warung Makan Indomie (Warmindo)**.

---

## Fitur Utama

### **Role-based Access**
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

## **Struktur Proyek**

```

📁 warmindo_app/
│
├── main_hal_pengguna.py        # Halaman utama (dashboard pengguna)
├── session_manager.py          # Manajemen sesi login/logout
│
├── 📁 form/                    # Folder berisi halaman (form) aplikasi
│   ├── form_beranda.py
│   ├── form_profil.py
│   ├── form_kelola_user.py
│   ├── form_kelola_menu.py
│   ├── form_kelola_kasir.py
│   ├── form_kelola_pelanggan.py
│   ├── form_kelola_transaksi.py
│   ├── form_kelola_riwayat_transaksi.py
│   └── form_kelola_laporan_transaksi.py
│
└── hal_awal.py                 # Halaman login/awal aplikasi

````

---

## **Penjelasan File `main_hal_pengguna.py`**

File `main_hal_pengguna.py` merupakan inti dari aplikasi yang mengatur:
- **Navigasi antar halaman** menggunakan `NavigationRail`
- **Manajemen sesi pengguna** (menampilkan username dan hak akses)
- **Pemanggilan halaman dinamis** berdasarkan peran pengguna
- **Tombol logout** dengan konfirmasi menggunakan `AlertDialog`

---

## **Alur Program**

1. Saat pengguna berhasil login, data sesi akan disimpan menggunakan `session_manager.py`.
2. Fungsi `main_hal_pengguna(page)` dijalankan untuk menampilkan halaman utama.
3. Berdasarkan `hak_akses` pengguna, sistem akan menentukan daftar halaman (`pages`) yang ditampilkan.
4. Navigasi antar halaman dikontrol melalui `NavigationRail`.
5. Jika pengguna menekan tombol **Keluar**, maka akan muncul dialog konfirmasi.
6. Setelah konfirmasi, sesi dihapus dan pengguna dikembalikan ke halaman login (`hal_awal.py`).

---

## **Contoh Tampilan Navigasi**

| Peran | Menu Navigasi |
|-------|----------------|
| **Admin** | Beranda, Kelola Menu, Kelola Kasir, Kelola Pengguna, Laporan Transaksi, Profil |
| **Kasir** | Beranda, Kelola Pelanggan, Transaksi, Riwayat Transaksi, Laporan Transaksi, Profil |

---

## **Instalasi dan Menjalankan Aplikasi**

### Persyaratan

Pastikan kamu sudah menginstal **Python 3.10+**

### Instalasi Library

Jalankan perintah berikut di terminal:
```bash
pip install flet
````

### Jalankan Aplikasi

Untuk menjalankan halaman utama pengguna:

```bash
python main_hal_pengguna.py
```

> Pastikan kamu sudah login terlebih dahulu agar sesi pengguna (`session_manager`) tersedia.

---

## **Fitur Logout**

* Tombol **Keluar** akan memunculkan dialog konfirmasi.
* Jika dikonfirmasi, sesi akan dihapus melalui `clear_session()`.
* Aplikasi kembali ke halaman login (`hal_awal.main(page)`).

---

## **Kontributor**

* **Nawang Alan Andrian** — Developer utama
* Teknologi: `Python`, `Flet`, `JSON` (untuk penyimpanan sesi), `UI berbasis NavigationRail`

---

## **Lisensi**

Proyek ini bersifat **Open Source** untuk keperluan pembelajaran dan pengembangan aplikasi kasir sederhana berbasis Python & Flet.

---

**Dibuat dengan ❤️ menggunakan [Flet](https://flet.dev)**

```

---

Apakah kamu ingin saya tambahkan juga **preview screenshot layout dashboard Warmindo (mockup Flet UI)** dalam README ini (misalnya dengan gambar “📸 Tampilan Aplikasi”)?  
Kalau iya, aku bisa bantu buatkan versi dengan contoh layout dan diagram navigasi di README-nya.
```
