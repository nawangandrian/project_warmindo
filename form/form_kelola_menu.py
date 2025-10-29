from flet import *
import mysql.connector

# Setup koneksi ke database MySQL
koneksi_db = mysql.connector.connect(host = "localhost", user = "root", password = "", database = "mad_uas_db_2024_202153019")
cursor = koneksi_db.cursor()

# Fungsi untuk mengambil data menu dari database MySQL
def ambil_data_menu():
    # Query untuk mengambil data menu
    query = "SELECT * FROM menu ORDER BY id_menu DESC"
    cursor.execute(query)

    # Mengambil semua baris data
    data_menu = cursor.fetchall()

    return data_menu

# Halaman kelola menu
def form_kelola_menu():

    # Mengambil data menu dari database MySQL
    data_menu = ambil_data_menu()

    # Variabel untuk paginasi
    baris_data_per_hal = 5  # Jumlah baris per halaman
    hal_sekarang = 0  # Mulai dari halaman pertama

    # Membuat inputan untuk form entri
    inputan_pencarian = TextField(label = "Cari by Nama Menu", width = 300, autofocus = True) # Membuat TextField untuk pencarian
    inputan_id_menu = TextField(visible = False, width = 300)  # Field ID yang disembunyikan
    inputan_nama_menu = TextField(label = "Nama Menu", width = 300)
    inputan_jenis_menu = Dropdown(label = "Jenis Menu", width = 300,
        options = [
            dropdown.Option("Mie Goreng"),
            dropdown.Option("Mie Kuah"),
        ],
    )
    def validate_numeric_input(e):
        # Only allow numbers, if the input has anything other than digits, reset the value
        if not e.control.value.isdigit():
            e.control.value = ''.join([char for char in e.control.value if char.isdigit()])
        e.control.update()
    inputan_harga_menu = TextField(label="Harga", width=300, on_change=validate_numeric_input)
    inputan_stok_menu = TextField(label="Stok", width=300, on_change=validate_numeric_input)
    snack_bar_berhasil = SnackBar( Text("Operasi berhasil"), bgcolor = "green")
    snack_bar_gagal = SnackBar( Text("Operasi gagal"), bgcolor = "red")

    # Fungsi untuk membersihkan form entri
    def bersihkan_form_entri(e = None):
        inputan_id_menu.value = ""
        inputan_nama_menu.value = ""
        inputan_jenis_menu.value = ""
        inputan_harga_menu.value = ""
        inputan_stok_menu.value = ""
        
        inputan_id_menu.update()
        inputan_nama_menu.update()
        inputan_jenis_menu.update()
        inputan_harga_menu.update()
        inputan_stok_menu.update()

    # Fungsi untuk mengisi data menu ke dalam form entri (edit data)
    def detail_data_menu(e):
        # Ambil ID_Menu dari data
        menu_id = e.control.data[0]  # Pastikan mengambil elemen pertama sebagai ID_Menu (integer)

        try:
            # Query untuk mengambil data berdasarkan ID_Menu
            cursor.execute("SELECT * FROM menu WHERE ID_Menu = %s", (menu_id,))
            menu_details = cursor.fetchone()  # Ambil satu baris data

            if menu_details:
                # Isi form dengan data yang didapat dari database
                inputan_id_menu.value = menu_details[0]  # ID_Menu
                inputan_nama_menu.value = menu_details[1]  # Nama_Menu
                inputan_jenis_menu.value = menu_details[2]  # Jenis_Menu
                inputan_harga_menu.value = str(menu_details[3])  # Harga
                inputan_stok_menu.value = str(menu_details[4])  # Stok

                # Update input field
                inputan_id_menu.update()
                inputan_nama_menu.update()
                inputan_jenis_menu.update()
                inputan_harga_menu.update()
                inputan_stok_menu.update()

        except Exception as error:
            print(f"Error: {error}")

    # Fungsi untuk menyimpan data menu ke database
    def simpan_data_menu(e):
        try:
            if inputan_id_menu.value == '':
                sql = "INSERT INTO menu (Nama_Menu, Jenis_Menu, Harga, Stok) VALUES(%s, %s, %s, %s)"
                val = (inputan_nama_menu.value, inputan_jenis_menu.value, int(inputan_harga_menu.value), int(inputan_stok_menu.value))
            else:
                sql = "UPDATE menu SET Nama_Menu = %s, Jenis_Menu = %s, Harga = %s, Stok = %s WHERE ID_Menu = %s"
                val = (inputan_nama_menu.value, inputan_jenis_menu.value, int(inputan_harga_menu.value), int(inputan_stok_menu.value), inputan_id_menu.value)
            
            cursor.execute(sql, val)
            koneksi_db.commit()
            print(cursor.rowcount, "Data di simpan!")
            
            data_menu = ambil_data_menu()  # Mengambil kembali data menu yang terbaru dari database
            # Reset data yang telah difilter menjadi data terbaru
            nonlocal filtered_data_menu
            filtered_data_menu = data_menu  # Set data yang difilter menjadi data terbaru

            # Memperbarui baris data menu di tabel berdasarkan data yang sudah difilter
            update_baris_data_menu()
            bersihkan_form_entri()

            # Menampilkan snack bar sukses
            snack_bar_berhasil.open = True
            snack_bar_berhasil.update()

        except Exception as e:
            print(e)
            print("Ada yang error!")

    # Fungsi untuk menghapus data menu
    def hapus_data_menu(e):
        try:
            sql = "DELETE FROM menu WHERE id_menu = %s"
            val = (e.control.data,)
            cursor.execute(sql, val)
            koneksi_db.commit()
            print(cursor.rowcount, "Data di hapus!")

            # Setelah data dihapus, ambil kembali data menu dan update tabel
            data_menu = ambil_data_menu()  # Mengambil kembali data menu yang terbaru dari database

            # Reset data yang telah difilter menjadi data terbaru
            nonlocal filtered_data_menu
            filtered_data_menu = data_menu  # Set data yang difilter menjadi data terbaru

            # Memperbarui baris data menu di tabel berdasarkan data yang sudah difilter
            update_baris_data_menu()

            # Menampilkan snack bar sukses
            snack_bar_berhasil.open = True
            snack_bar_berhasil.update()
            bersihkan_form_entri()
            
        except Exception as e:
            print(e)
            print("Ada yang error!")

    # Variabel untuk menyimpan data menu yang telah difilter
    filtered_data_menu = data_menu

    # Fungsi untuk memfilter data menu berdasarkan input di search field
    def filter_menu(e):
        data_menu = ambil_data_menu()  # Mengambil kembali data menu yang terbaru dari database
        query_pencarian = inputan_pencarian.value.lower()  # Mendapatkan kata pencarian dalam huruf kecil
        nonlocal filtered_data_menu
        # Memfilter data menu berdasarkan menuname (tidak peka huruf besar/kecil)
        filtered_data_menu = [menu_kolom for menu_kolom in data_menu if query_pencarian in menu_kolom[1].lower()]
        update_baris_data_menu()  # Memperbarui DataTable setelah difilter

    # Menghubungkan fungsi filter dengan perubahan nilai di search field
    inputan_pencarian.on_change = filter_menu

    # Fungsi untuk membuat DataRow berdasarkan data menu yang sudah difilter
    def update_baris_data_menu():
        nonlocal baris_data_menu
        # Menghitung indeks mulai dan akhir berdasarkan halaman saat ini
        index_mulai = hal_sekarang * baris_data_per_hal
        index_selesai = index_mulai + baris_data_per_hal
        hal_data = filtered_data_menu[index_mulai:index_selesai]  # Mendapatkan data sesuai dengan halaman yang aktif
        
        baris_data_menu = [
            DataRow(
                cells=[
                    DataCell(Text(str(index_mulai + i + 1))),  # Nomor urut otomatis (indeks mulai dari 1)
                    DataCell(Text(menu_kolom[1])),  # Nama Menu
                    DataCell(Text(menu_kolom[2])),  # Jenis Menu
                    DataCell(Text(str(menu_kolom[3]))),  # Harga
                    DataCell(Text(str(menu_kolom[4]))),
                    DataCell(
                        Row([
                            IconButton("create", icon_color = "grey", data = menu_kolom, on_click = detail_data_menu),
                            IconButton("delete", icon_color = "red", data = menu_kolom[0], on_click = hapus_data_menu),
                        ])
                    ),
                ]
            )
            for i, menu_kolom in enumerate(hal_data)
        ]
        
        # Memperbarui DataTable dengan baris yang sudah difilter
        tabel_data_menu.rows = baris_data_menu
        tabel_data_menu.update()  # Menyegarkan DataTable untuk menampilkan baris yang sudah diperbarui

    # Inisialisasi pembuatan DataRow berdasarkan data menu yang sudah difilter
    baris_data_menu = [
        DataRow(
            cells = [
                DataCell(Text(str(i + 1))),  # Nomor urut otomatis (indeks mulai dari 1)
                DataCell(Text(menu_kolom[1])),
                DataCell(Text(menu_kolom[2])),  # Jenis Menu
                DataCell(Text(str(menu_kolom[3]))),  # Harga
                DataCell(Text(str(menu_kolom[4]))),  # nama menu
                DataCell(
                    Row([
                        IconButton("create", icon_color = "grey", data = menu_kolom, on_click = detail_data_menu),
                        IconButton("delete", icon_color = "red", data = menu_kolom[0], on_click = hapus_data_menu),
                    ])
                ),
            ]
        )
        for i, menu_kolom in enumerate(filtered_data_menu[:baris_data_per_hal])
    ]
    
    # Membuat DataTable dan menyimpannya dalam variabel
    tabel_data_menu = DataTable(
        columns = [
            DataColumn(Text("No.")),
            DataColumn(Text("Nama Menu")),
            DataColumn(Text("Jenis Menu")),
            DataColumn(Text("Harga")),
            DataColumn(Text("Stok")),
            DataColumn(Text("Opsi")),
        ],
        rows = baris_data_menu,  # Menggunakan baris yang dibuat secara dinamis berdasarkan data yang sudah difilter
        width = "auto",  # Menyesuaikan lebar secara otomatis berdasarkan konten
    )

    # Kontrol untuk tombol navigasi pagination
    def pergi_hal_sebelumnya(e):
        nonlocal hal_sekarang
        if hal_sekarang > 0:
            hal_sekarang -= 1
            update_baris_data_menu()  # Memperbarui tabel dengan data halaman baru

    def pergi_hal_selanjutnya(e):
        nonlocal hal_sekarang
        if (hal_sekarang + 1) * baris_data_per_hal < len(filtered_data_menu):
            hal_sekarang += 1
            update_baris_data_menu()  # Memperbarui tabel dengan data halaman baru

    btn_sebelumnya = ElevatedButton("Sebelumnya", on_click = pergi_hal_sebelumnya)
    btn_selanjutnya = ElevatedButton("Berikutnya", on_click = pergi_hal_selanjutnya)

    # Membuat bagian kiri dengan form
    form_kiri = Container(
        Column(
            controls = [
                Text("Form Entri", size = 14, weight = FontWeight.BOLD),
                inputan_id_menu,
                Text("Masukkan Nama Menu :"),
                inputan_nama_menu,
                Text("Masukkan Jenis Menu :"),
                inputan_jenis_menu,
                Text("Masukkan Harga Menu :"),
                inputan_harga_menu,
                Text("Masukkan Stok Menu :"),
                inputan_stok_menu,
                Row(
                    controls = [
                        ElevatedButton("S i m p a n", on_click = simpan_data_menu),
                        ElevatedButton("Batal", on_click = bersihkan_form_entri),
                    ],
                    alignment = MainAxisAlignment.CENTER,  # Menyusun tombol di tengah
                    spacing = 20,  # Menambahkan jarak antara tombol
                ),
            ],
            width = 300,  # Lebar bagian kiri
        ),
        border_radius = 20,
        border = border.all(color = colors.GREY_900, width = 0.5),
        padding = 20,
    )

    # Membuat bagian kanan dengan search field dan table
    form_kanan = Container(
        content=Column(
            controls = [
                Text("Tabel Data", size=14, weight=FontWeight.BOLD),
                inputan_pencarian,  # Menambahkan search field di sini

                # Membuat Row dengan tabel data yang bisa digulir
                Row(
                    controls = [
                        tabel_data_menu  # Menambahkan DataTable di sini
                    ],
                    scroll = "always",  # Membolehkan scroll pada Row
                ),
                
                # Menambahkan tombol navigasi
                Row([btn_sebelumnya, btn_selanjutnya]),
            ],
            width="700",  # Lebar bagian kanan
            scroll="always",  # Membolehkan scroll vertikal pada Column
        ),
        border_radius=20,
        border=border.all(color=colors.GREY_900, width=0.5),
        padding=20,
    )

    # Menambahkan baris ke halaman
    return Container(  # Wrap seluruh Column ke dalam Container
        content = Column(
            controls = [
                # Baris pertama
                Row([
                        Icon(name = icons.DATASET, size = 50, color = colors.BLUE_400),
                        Text("Kelola Menu", size = 30, weight = "bold")
                    ], alignment = MainAxisAlignment.CENTER),
                Row(
                    controls = [form_kiri, form_kanan],
                    alignment = MainAxisAlignment.START,  # Menyusun item di kiri
                    vertical_alignment = CrossAxisAlignment.START,  # Menyusun item di atas secara vertikal
                ),
                snack_bar_berhasil, snack_bar_gagal
            ],
        ),
        margin = 10
    )
