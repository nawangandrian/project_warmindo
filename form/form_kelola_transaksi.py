from flet import *
from datetime import datetime
import mysql.connector

from session_manager import get_session, clear_session  # Mengimpor dari session_manager

# Setup koneksi ke database MySQL
koneksi_db = mysql.connector.connect(host="localhost", user="root", password="", database="mad_uas_db_2024_202153019")
cursor = koneksi_db.cursor(dictionary=True)

# Fungsi untuk membuat koneksi ke database MySQL
def get_db_connection():
    # Membuat koneksi baru setiap kali dipanggil
    koneksi_db = mysql.connector.connect(
        host="localhost", 
        user="root", 
        password="", 
        database="mad_uas_db_2024_202153019"
    )
    return koneksi_db

# Fungsi untuk mengambil data dari tabel tertentu
def get_data_from_table(query):
    koneksi_db = get_db_connection()  # Mendapatkan koneksi baru
    cursor = koneksi_db.cursor(dictionary=True)
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    koneksi_db.close()  # Menutup koneksi setelah query selesai
    return data

# Membuat layout halaman transaksi
def form_kelola_transaksi():

    data_keranjang = []

    # SnackBar untuk memberi feedback operasional
    snack_bar_berhasil = SnackBar(Text("Operasi berhasil"), bgcolor="green")
    snack_bar_gagal = SnackBar(Text("Operasi gagal"), bgcolor="red")

    # Ambil ID pengguna dari sesi
    user_session = get_session()  # Fungsi untuk mendapatkan sesi aktif
    id_user_aktif = user_session.get("id_user")  # Ambil id_user dari sesi

    # Query untuk mendapatkan data kasir berdasarkan ID_User
    kasir_query = f"SELECT * FROM kasir WHERE ID_User = {id_user_aktif}"
    kasir_data = get_data_from_table(kasir_query)  # Mendapatkan data kasir berdasarkan ID_User

    # Jika kasir ditemukan, buat dropdown untuk memilih kasir
    if kasir_data:
        inputan_kasir = Dropdown(
            label="Nama Kasir",
            width=500,
            options=[dropdown.Option(row['ID_Kasir'], row['Nama_Kasir']) for row in kasir_data]
        )
    else:
        inputan_kasir = None  # Tidak ada kasir terkait pengguna aktif
    
    # Mengambil data pelanggan dari database
    pelanggan_query = "SELECT * FROM pelanggan ORDER BY ID_Pelanggan DESC"
    pelanggan_data = get_data_from_table(pelanggan_query)  # Mendapatkan data pelanggan terbaru
    inputan_pelanggan = Dropdown(
        label="Nama Pelanggan", 
        width=500,
        options=[dropdown.Option(row['ID_Pelanggan'], str(row['Nama_Pelanggan'])) for row in pelanggan_data]
    )

    # Mengambil data menu dari database
    menu_query = "SELECT * FROM menu ORDER BY ID_Menu DESC"
    menu_data = get_data_from_table(menu_query)  # Mendapatkan data menu terbaru
    inputan_menu = Dropdown(
        label="Nama Menu", 
        width=500,
        options=[dropdown.Option(row['ID_Menu'], str(row['Nama_Menu'])) for row in menu_data]
    )

    def validate_numeric_input(e):
        # Only allow numbers, if the input has anything other than digits, reset the value
        if not e.control.value.isdigit():
            e.control.value = ''.join([char for char in e.control.value if char.isdigit()])
        e.control.update()

    # Inputan jumlah beli dan total harga
    inputan_jumlah_beli = TextField(label="Jumlah Beli", width=500, on_change=validate_numeric_input)
    inputan_pajak = TextField(label="Jumlah Pajak", width=200, on_change=validate_numeric_input)
    inputan_diskon = TextField(label="Jumlah Diskon", width=200, on_change=validate_numeric_input)
    inputan_total_harga = TextField(label="Total Harga", width=500, read_only=True)
    inputan_pencarian = TextField(label="Cari Nama Kasir", width=500, autofocus=True)

    # Dropdown untuk memilih metode pembayaran
    inputan_metode_pembayaran = Dropdown(label="Metode Pembayaran", width=200,
        options=[dropdown.Option('Tunai', 'Tunai'),
                 dropdown.Option('Kartu Kredit', 'Kartu Kredit'),
                 dropdown.Option('Transfer', 'Transfer')])
    
    inputan_jenis_pesanan = Dropdown(label="Jenis Pesanan", width=200,
        options=[dropdown.Option('Take Away', 'Take Away'),
                 dropdown.Option('Dine In', 'Dine In')])

    # Fungsi untuk menghitung total harga berdasarkan jumlah beli dan harga per item
    def hitung_total_harga(e=None):
        try:
            # Periksa jika jumlah beli kosong atau tidak valid
            if inputan_jumlah_beli.value.strip() == '' or not inputan_jumlah_beli.value.isdigit():
                inputan_total_harga.value = ""
                inputan_total_harga.update()
                return  # Jangan lanjutkan jika jumlah beli tidak valid

            jumlah_beli = int(inputan_jumlah_beli.value)

            # Periksa apakah ID menu valid dan ambil harga per item
            cursor.execute("SELECT Harga FROM menu WHERE ID_Menu = %s", (inputan_menu.value,))
            menu_data = cursor.fetchone()

            if menu_data is None:
                inputan_total_harga.value = "Menu tidak ditemukan"
                inputan_total_harga.update()
                return  # Jika menu tidak ditemukan, berhenti

            harga_per_item = menu_data['Harga']

            # Hitung total harga
            total_harga = jumlah_beli * harga_per_item
            inputan_total_harga.value = str(total_harga)
            inputan_total_harga.update()

        except Exception as ex:
            print(f"Error menghitung total harga: {ex}")
            inputan_total_harga.value = "Error"
            inputan_total_harga.update()

    # Update total harga setiap kali jumlah beli atau menu berubah
    inputan_jumlah_beli.on_change = hitung_total_harga
    inputan_menu.on_change = hitung_total_harga

    # Fungsi untuk membersihkan form entri
    def bersihkan_form_entri(e=None):
        inputan_jumlah_beli.value = ""
        inputan_total_harga.value = ""
        inputan_metode_pembayaran.value = ""
        inputan_jenis_pesanan.value = ""
        inputan_pajak.value = ""
        inputan_diskon.value = ""
        inputan_kasir.value = ""
        inputan_menu.value = ""
        inputan_pelanggan.value = ""
        
        inputan_jumlah_beli.update()
        inputan_total_harga.update()
        inputan_metode_pembayaran.update()
        inputan_jenis_pesanan.update()
        inputan_kasir.update()
        inputan_pajak.update()
        inputan_diskon.update()
        inputan_menu.update()
        inputan_pelanggan.update()

    def simpan_data_transaksi(e):
        try:
            if not data_keranjang:
                snack_bar_gagal.text = "Keranjang kosong."
                snack_bar_gagal.open = True
                snack_bar_gagal.update()
                return

            # Hitung jumlah beli dan total harga dari data keranjang
            jumlah_beli = sum(item['Jumlah'] for item in data_keranjang)
            total_harga = sum(item['Subtotal'] for item in data_keranjang)

            # Ambil inputan diskon dan pajak dari field
            diskon_persen = float(inputan_diskon.value) if inputan_diskon.value else 0
            pajak_persen = float(inputan_pajak.value) if inputan_pajak.value else 0

            # Hitung diskon dalam bentuk persen
            diskon = (diskon_persen / 100) * total_harga

            # Hitung pajak dalam bentuk persen
            pajak = (pajak_persen / 100) * total_harga

            # Hitung total harga setelah diskon dan pajak
            total_harga_setelah_diskon = total_harga - diskon
            total_harga_final = total_harga_setelah_diskon + pajak

            # Dapatkan waktu dan tanggal saat ini
            tanggal_transaksi = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Mendapatkan tanggal hari ini dalam format DDMMYY
            tanggal_sekarang = datetime.now().strftime("%d%m%y")

            # Mendapatkan ID_Transaksi terakhir dari tabel transaksi
            cursor.execute("SELECT ID_Transaksi FROM transaksi WHERE ID_Transaksi LIKE %s ORDER BY ID_Transaksi DESC LIMIT 1", (f"TR{tanggal_sekarang}%",))
            result = cursor.fetchone()

            # Debugging: Menampilkan hasil query
            print(f"Result Query: {result}")

            if result and result['ID_Transaksi']:  # Jika result adalah dictionary
                # Jika sudah ada, kita ambil nomor urut terakhir dan tambahkan 1
                last_id = result['ID_Transaksi']
                print(f"Last ID: {last_id}")

                try:
                    # Mengambil 3 digit terakhir dari ID transaksi
                    last_number = last_id[-3:]  # Ambil 3 digit terakhir dari ID transaksi
                    print(f"Last Number (String): {last_number}")

                    # Cek jika 3 digit terakhir memang bisa diparse ke integer
                    id_number = int(last_number) + 1
                    print(f"Last Number (Integer): {id_number}")
                except ValueError:
                    # Jika terjadi ValueError, kita atur nomor urut ke 1
                    print("Error: Invalid ID format, resetting number to 1.")
                    id_number = 1
            else:
                # Jika belum ada, kita mulai dari 1
                id_number = 1

            # Membuat angka dengan panjang 3 digit
            new_id_number = str(id_number).zfill(3)
            print(f"New ID Number (Padded): {new_id_number}")

            # Membuat ID_Transaksi baru dengan format yang diinginkan (TRDDMMYY001)
            ID_Transaksi = f"TR{tanggal_sekarang}{new_id_number}"
            print(f"Generated ID_Transaksi: {ID_Transaksi}")

            # Simpan transaksi baru
            sql = """INSERT INTO transaksi (ID_Transaksi, Tanggal_Transaksi, Jumlah_Beli, Diskon_Transaksi, Pajak_Transaksi, Total_Harga, Metode_Pembayaran, Jenis_Pesanan, ID_Kasir, ID_Pelanggan) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            val = (ID_Transaksi, tanggal_transaksi, jumlah_beli, diskon, pajak, total_harga_final, 
                inputan_metode_pembayaran.value, inputan_jenis_pesanan.value, inputan_kasir.value, inputan_pelanggan.value)
            cursor.execute(sql, val)
            koneksi_db.commit()

            # Ambil ID transaksi yang baru saja disimpan
            id_transaksi = cursor.lastrowid

            # Simpan detail transaksi dan update stok
            for item in data_keranjang:
                sql_detail = """INSERT INTO detail_transaksi (ID_Transaksi, ID_Menu, Jumlah, Subtotal) 
                                VALUES (%s, %s, %s, %s)"""
                val_detail = (ID_Transaksi, item['ID_Menu'], item['Jumlah'], item['Subtotal'])
                cursor.execute(sql_detail, val_detail)

                cursor.execute("UPDATE menu SET Stok = Stok - %s WHERE ID_Menu = %s", (item['Jumlah'], item['ID_Menu']))
                koneksi_db.commit()

            snack_bar_berhasil.text = "Transaksi berhasil disimpan."
            snack_bar_berhasil.open = True
            snack_bar_berhasil.update()

            data_keranjang.clear()
            update_tabel_keranjang()
            bersihkan_form_entri()

        except Exception as e:
            print(f"Error: {e}")
            snack_bar_gagal.text = str(e)
            snack_bar_gagal.open = True
            snack_bar_gagal.update()
    
    # Variabel untuk menyimpan data kasir yang telah difilter
    filtered_data_keranjang = data_keranjang
    
    # Fungsi untuk menambahkan item ke keranjang
    def tambah_ke_keranjang(e):
        try:
            if not inputan_menu.value or not inputan_jumlah_beli.value.isdigit():
                snack_bar_gagal.text = "Input tidak valid."
                snack_bar_gagal.open = True
                snack_bar_gagal.update()
                return

            jumlah_beli = int(inputan_jumlah_beli.value)

            # Ambil detail menu dari database
            cursor.execute("SELECT * FROM menu WHERE ID_Menu = %s", (inputan_menu.value,))
            menu_data = cursor.fetchone()

            if not menu_data:
                snack_bar_gagal.text = "Menu tidak ditemukan."
                snack_bar_gagal.open = True
                snack_bar_gagal.update()
                return

            stok_tersedia = menu_data['Stok']
            if jumlah_beli > stok_tersedia:
                snack_bar_gagal.text = f"Stok tidak mencukupi. Stok tersedia: {stok_tersedia}."
                snack_bar_gagal.open = True
                snack_bar_gagal.update()
                return

            harga = menu_data['Harga']
            subtotal = jumlah_beli * harga

            # Tambahkan item ke keranjang
            data_keranjang.append({
                "ID_Menu": inputan_menu.value,
                "Nama_Menu": menu_data['Nama_Menu'],
                "Jumlah": jumlah_beli,
                "Harga": harga,
                "Subtotal": subtotal
            })

            snack_bar_berhasil.text = "Item berhasil ditambahkan ke keranjang."
            snack_bar_berhasil.open = True
            snack_bar_berhasil.update()

            update_tabel_keranjang()
            bersihkan_form_entri()

        except Exception as ex:
            print(f"Error: {ex}")
            snack_bar_gagal.text = "Terjadi kesalahan."
            snack_bar_gagal.open = True
            snack_bar_gagal.update()

    # Fungsi untuk menghapus item dari keranjang
    def hapus_dari_keranjang(e):
        try:
            index = e.control.data
            del data_keranjang[index]
            update_tabel_keranjang()
        except Exception as ex:
            print(f"Error: {ex}")

    # Fungsi untuk memperbarui tampilan tabel keranjang
    def update_tabel_keranjang():
        tabel_keranjang.rows = [
            DataRow(
                cells=[
                    DataCell(Text(str(i + 1))),
                    DataCell(Text(item['Nama_Menu'])),
                    DataCell(Text(str(item['Jumlah']))),
                    DataCell(Text(f"Rp {item['Harga']:,}")),
                    DataCell(Text(f"Rp {item['Subtotal']:,}")),
                    DataCell(
                        IconButton(
                            icon="delete",
                            icon_color="red",
                            data=i,
                            on_click=hapus_dari_keranjang
                        )
                    ),
                ]
            ) for i, item in enumerate(data_keranjang)
        ]
        tabel_keranjang.update()
    
    tabel_keranjang = DataTable(
        columns=[
            DataColumn(Text("No.")),
            DataColumn(Text("Nama Menu")),
            DataColumn(Text("Jumlah")),
            DataColumn(Text("Harga")),
            DataColumn(Text("Subtotal")),
            DataColumn(Text("Opsi")),
        ],
        rows=[],
        width="auto",
    )

    btn_tambah_ke_keranjang = ElevatedButton("Tambah ke Keranjang", on_click=tambah_ke_keranjang)

    form_keranjang = Container(
        content=Column(
            controls=[
                Text("Tabel Keranjang", size=14, weight=FontWeight.BOLD),
                Row(
                    controls = [
                        tabel_keranjang,  # Menampilkan DataTable
                    ],
                    scroll = "auto",  # Membolehkan scroll horizontal pada Row
                    alignment=MainAxisAlignment.CENTER, 
                ),
            ],
            width="950",
            scroll="always",
        ),
        height=400,  
        border_radius=20,
        border=border.all(color=colors.GREY_900, width=0.5),
        padding=20,
    )

    # Membuat layout halaman transaksi dengan scroll
    form_menu = Container(
        content=Column(
            controls=[
                Text("Form Entri Menu", size=14, weight=FontWeight.BOLD),
                Text("Menu :"),
                inputan_menu,
                Text("Jumlah Beli :"),
                inputan_jumlah_beli,
                Text("Total Harga :"),
                inputan_total_harga,
                Row(
                    controls=[
                        btn_tambah_ke_keranjang,
                        ElevatedButton("Batal", on_click=bersihkan_form_entri),
                    ],
                    alignment=MainAxisAlignment.CENTER,  # Menyusun tombol di tengah
                    spacing=20,  # Menambahkan jarak antara tombol
                ),
            ],
            scroll="always",  # Mengaktifkan scrolling
        ),
        width=500,  # Lebar bagian transaksi
        height=400,  # Tinggi maksimal sebelum scroll muncul
        border_radius=20,
        border=border.all(color=colors.GREEN_200),
        padding=20,
    )

    # Membuat layout halaman transaksi dengan scroll
    form_transaksi = Container(
        content=Column(
            controls=[
                Text("Form Entri Data", size=14, weight=FontWeight.BOLD),
                Text("Kasir :"),
                inputan_kasir,
                Text("Pelanggan :"),
                inputan_pelanggan,
                Row(
                    controls=[
                        Column(
                            controls=[
                                Text("Masukkan Metode Pembayaran :"),
                                inputan_metode_pembayaran,
                            ],
                        ),
                        Column(
                            controls=[
                                Text("Masukkan Jenis Pesanan :"),
                                inputan_jenis_pesanan,
                            ],
                        ),
                    ],
                    alignment=MainAxisAlignment.START,  # Menyusun tombol di tengah
                    spacing=20,  # Menambahkan jarak antara tombol
                ),
                Row(
                    controls=[
                        Column(
                            controls=[
                                Text("Masukkan Diskon :"),
                                inputan_diskon,
                            ],
                        ),
                        Column(
                            controls=[
                                Text("Masukkan Pajak :"),
                                inputan_pajak,
                            ],
                        ),
                    ],
                    alignment=MainAxisAlignment.START,  # Menyusun tombol di tengah
                    spacing=20,  # Menambahkan jarak antara tombol
                ),
                Row(
                    controls=[
                        ElevatedButton("S i m p a n", on_click=simpan_data_transaksi),
                        ElevatedButton("Batal", on_click=bersihkan_form_entri),
                    ],
                    alignment=MainAxisAlignment.CENTER,  # Menyusun tombol di tengah
                    spacing=20,  # Menambahkan jarak antara tombol
                ),
            ],
            scroll="always",  # Mengaktifkan scrolling
        ),
        width=500,  # Lebar bagian transaksi
        height=400,  # Tinggi maksimal sebelum scroll muncul
        border_radius=20,
        border=border.all(color=colors.GREEN_200),
        padding=20,
    )
    
    return Container(  # Wrap seluruh Column ke dalam Container
        content=Column(
            controls=[
                Row([ 
                    Icon(name=icons.TABLE_VIEW_ROUNDED, size=50, color=colors.BLUE_400),
                    Text("Kelola Transaksi", size=30, weight="bold")
                ], alignment=MainAxisAlignment.START),

                Row(
                    controls=[form_menu, form_transaksi],
                    alignment=MainAxisAlignment.CENTER,  # Untuk menyusun secara horizontal di tengah
                    vertical_alignment=CrossAxisAlignment.START, 
                ),

                Row(
                    controls=[form_keranjang],
                    alignment=MainAxisAlignment.CENTER,  # Untuk menyusun secara horizontal di tengah
                    vertical_alignment=CrossAxisAlignment.START, 
                ),

                snack_bar_berhasil, snack_bar_gagal  # Pastikan SnackBar ditambahkan ke halaman
            ],
            scroll="adaptive",  # Mengaktifkan scroll untuk seluruh konten Column
            alignment=MainAxisAlignment.CENTER,  # Menyusun semua elemen secara vertikal di tengah
        ),
        margin = 10,   # Memberikan jarak di luar container
        width=1150,  # Lebar bagian transaksi
        height= 700,  # Tinggi maksimal sebelum scroll muncul
    )
