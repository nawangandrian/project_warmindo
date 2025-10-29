from flet import *
# Mengimpor fungsi halaman dari file lain
from form.form_beranda import form_beranda  
from form.form_profil import form_profil
from form.form_kelola_user import form_kelola_user
from form.form_kelola_menu import form_kelola_menu
from form.form_kelola_kasir import form_kelola_kasir
from form.form_kelola_pelanggan import form_kelola_pelanggan
from form.form_kelola_transaksi import form_kelola_transaksi
from form.form_kelola_riwayat_transaksi import form_kelola_riwayat_transaksi
from form.form_kelola_laporan_transaksi import form_kelola_laporan_transaksi

from session_manager import get_session, clear_session  # Mengimpor dari session_manager

def main_hal_pengguna(page: Page):
    # Mendapatkan sesi pengguna
    user = get_session()
    page.title = f"Aplikasi Penjualan Warmindo - Halaman Pengguna ({user['username']})"
    page.window_width = "auto"  # Menentukan lebar jendela aplikasi

    if user['hak_akses'] == 'Admin':
        pages = [form_beranda, form_kelola_menu, form_kelola_kasir, form_kelola_user, form_kelola_laporan_transaksi, form_profil]
    elif user['hak_akses'] == 'Kasir':
        pages = [form_beranda, form_kelola_pelanggan, form_kelola_transaksi, form_kelola_riwayat_transaksi, form_kelola_laporan_transaksi, form_profil]
    # Inisialisasi indeks halaman yang dipilih
    selected_index = 0

    # Fungsi untuk menangani perubahan navigasi
    def on_navigation_change(e):
        nonlocal selected_index
        selected_index = e.control.selected_index
        # Perbarui halaman yang ditampilkan
        content_area.controls.clear()  # Hapus konten yang ada
        content_area.controls.append(pages[selected_index]())  # Tambahkan halaman baru
        page.update()

    # Membuat NavigationRail untuk navigasi berdasarkan hak akses pengguna
    rail = NavigationRail(
        selected_index=selected_index,  # Indeks halaman yang dipilih
        label_type=NavigationRailLabelType.ALL,  # Tampilkan label untuk semua destinasi
        destinations=[
            
            # Menu yang bisa diakses oleh semua pengguna
            NavigationRailDestination(
                icon=icons.HOME,
                selected_icon=icons.HOME,
                label="Beranda"
            ),
            
            # Menu untuk Admin
            *([
                NavigationRailDestination(
                    icon=icons.DATASET,
                    selected_icon=icons.DATASET,
                    label="Kelola Menu"
                ),
                NavigationRailDestination(
                    icon=icons.PERSON_ADD_ROUNDED,
                    selected_icon=icons.PERSON_ADD_ROUNDED,
                    label="Kelola Kasir"
                ),
                NavigationRailDestination(
                    icon=icons.PERSON_PIN_ROUNDED,
                    selected_icon=icons.PERSON_PIN_ROUNDED,
                    label="Kelola Pengguna"
                ),
            ] if user['hak_akses'] == 'Admin' else []),

            # Menu untuk Kasir
            *([
                NavigationRailDestination(
                    icon=icons.PERSON_ADD_ROUNDED,
                    selected_icon=icons.PERSON_ADD_ROUNDED,
                    label="Kelola Pelanggan"
                ),
                NavigationRailDestination(
                    icon=icons.TABLE_VIEW_ROUNDED,
                    selected_icon=icons.TABLE_VIEW_ROUNDED,
                    label="Transaksi"
                ),
                NavigationRailDestination(
                    icon=icons.DATA_THRESHOLDING_ROUNDED,
                    selected_icon=icons.DATA_THRESHOLDING_ROUNDED,
                    label="Riwayat Transaksi"
                ),
            ] if user['hak_akses'] == 'Kasir' else []),

            # Menu yang bisa diakses oleh Admin dan Kasir
            NavigationRailDestination(
                icon=icons.DATA_EXPLORATION_ROUNDED,
                selected_icon=icons.DATA_EXPLORATION_ROUNDED,
                label="Laporan Transaksi"
            ),

            # Menu untuk semua pengguna (Profil)
            NavigationRailDestination(
                icon=icons.PERSON,
                selected_icon=icons.PERSON,
                label="Profil"
            ),
        ],
        height=400,  # Menentukan tinggi dari NavigationRail
        on_change=on_navigation_change,  # Fungsi untuk menangani perubahan pada navigasi
    )

    # Membuat area konten untuk menampung halaman
    content_area = Column()
    content_area.controls.append(pages[selected_index]())  # Menampilkan halaman awal

    # Menambahkan NavigationRail dan area konten ke halaman utama
    page.add(
        Row(
            [
                Column([  # Kolom untuk NavigationRail dan tombol Keluar
                    Container(
                        Column(
                            [
                                Icon(icons.ACCOUNT_CIRCLE, size = 100, color = colors.BLUE_500),
                                Text(user['username'], size = 14, weight="bold", text_align = "center"),
                                Text(f"Hak Akses: {user['hak_akses']}", size = 12, color=colors.GREY),
                            ],
                            alignment="center",  # Menyusun isi kolom ke tengah secara vertikal dan horizontal
                            horizontal_alignment="center",  # Menyusun isi kolom secara horizontal di tengah
                        ),
                        padding = padding.symmetric(vertical = 20),
                        alignment = alignment.center,
                        width = 200,
                    ),
                    rail, 
                    Container(  # Membungkus ElevatedButton dalam Container untuk menata posisinya
                        ElevatedButton(
                            "Keluar", 
                            color = 'white',  # Warna teks tombol
                            width = 100,  # Lebar tombol
                            bgcolor = 'black',  # Warna latar belakang tombol
                            on_click = lambda e: handle_logout(page)  # Menangani klik tombol Keluar
                        ),
                        alignment = alignment.center,  # Menyusun tombol di tengah
                        width = 200,  # Menetapkan lebar Container agar sesuai dengan ukuran tombol
                    ),
                ], alignment = alignment.center, width = 200),  # Penyusunan vertikal dari rail dan tombol
                VerticalDivider(width = 1),  # Membuat pemisah vertikal
                content_area,  # Menampilkan area konten
            ],
            expand = True,  # Membuat layout mengisi seluruh ruang
        ),
        
    )

def handle_logout(page: Page):
    def on_confirm(e):
        page.dialog.open = False
        page.update()

        # Menghapus sesi pengguna
        clear_session()
        # Hapus semua kontrol yang ada (halaman dashboard)
        page.clean()
    
        from hal_awal import main
        # Menampilkan halaman login di jendela yang sama
        main(page)
        
    def on_cancel(e):
        page.dialog.open = False
        page.update()

    konfirmasi_dialog = AlertDialog(
        title = Row([
            Icon(icons.WARNING_ROUNDED, color = colors.RED, size = 30),  # Ikon peringatan
            Text("Konfirmasi Keluar", size = 20, weight = "bold", color = colors.BLACK),  # Judul dengan teks
        ],
        spacing = 10,  # Jarak antara ikon dan teks
        alignment = "start",  # Menyusun ke kiri
    ),
        content = Text("Apakah Anda yakin ingin keluar?"),
        actions = [
            TextButton("Batal", on_click = on_cancel),
            TextButton("Keluar", on_click = on_confirm),
        ],
        actions_alignment = "end",
    )
    
    # Membuka dialog konfirmasi
    page.dialog = konfirmasi_dialog
    konfirmasi_dialog.open = True
    page.update()
    
# Menjalankan aplikasi
# app(target = main_hal_pengguna)
