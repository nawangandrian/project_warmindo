from flet import *
import mysql.connector

# Setup koneksi ke database MySQL
koneksi_db = mysql.connector.connect(host="localhost", user="root", password="", database="mad_uas_db_2024_202153019")
cursor = koneksi_db.cursor()

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

# Fungsi untuk mengambil data kasir dari database MySQL
def ambil_data_kasir():
    query = "SELECT * FROM kasir"  # Query untuk mengambil data kasir
    cursor.execute(query)
    data_kasir = cursor.fetchall()
    return data_kasir

# Fungsi untuk mengambil data pengguna dari database MySQL
def ambil_data_user():
    query = "SELECT * FROM user ORDER BY id_user DESC"
    cursor.execute(query)
    data_user = cursor.fetchall()
    return data_user

# Halaman kelola pengguna atau user
def form_kelola_user():
    # Fetching kasir values from MySQL
    data_kasir = ambil_data_kasir()

    # Mengambil data pengguna dari database MySQL
    data_user = ambil_data_user()

    # Variabel untuk paginasi
    baris_data_per_hal = 5  # Jumlah baris per halaman
    hal_sekarang = 0  # Mulai dari halaman pertama

    # Membuat inputan untuk form entri
    inputan_pencarian = TextField(label="Cari by Username", width=300, autofocus=True)  # Membuat TextField untuk pencarian
    inputan_id_user = TextField(visible=False, width=300)  # Field ID yang disembunyikan
    inputan_username = TextField(label="Username", width=300)
    inputan_password = TextField(label="Password", width=300)
    inputan_hak_akses = Dropdown(label="Hak Akses", width=300, options=[dropdown.Option("Kasir"), dropdown.Option("Admin")])

    # Mengambil data kasir dari database
    kasir_query = "SELECT * FROM kasir ORDER BY ID_Kasir DESC"
    kasir_data = get_data_from_table(kasir_query)  # Mendapatkan data kasir terbaru
    inputan_kasir = Dropdown(
        label="Nama Kasir", 
        width=500,
        options=[dropdown.Option(row['ID_Kasir'], str(row['Nama_Kasir'])) for row in kasir_data],
        visible=False
    )

    # Fungsi untuk menangani perubahan di dropdown hak akses
    def update_visibilitas_kasir(e):
        inputan_kasir.visible = inputan_hak_akses.value == "Kasir"
        inputan_kasir.update()

    # Menghubungkan perubahan hak akses dengan perubahan visibilitas kasir
    inputan_hak_akses.on_change = update_visibilitas_kasir

    snack_bar_berhasil = SnackBar(Text("Operasi berhasil"), bgcolor="green")
    snack_bar_gagal = SnackBar(Text("Operasi gagal"), bgcolor="red")

    # Fungsi untuk membersihkan form entri
    def bersihkan_form_entri(e=None):
        inputan_id_user.value = ""
        inputan_username.value = ""
        inputan_password.value = ""
        inputan_hak_akses.value = ""
        inputan_kasir.value = ""  # Reset the kasir dropdown
        inputan_kasir.visible = False

        inputan_id_user.update()
        inputan_username.update()
        inputan_password.update()
        inputan_hak_akses.update()
        inputan_kasir.update()  # Update visibility

    # Fungsi untuk mengisi data pengguna ke dalam form entri (edit data)
    def detail_data_user(e):
        inputan_id_user.value = e.control.data[0]
        inputan_username.value = e.control.data[1]
        inputan_password.value = e.control.data[2]
        inputan_hak_akses.value = e.control.data[3]
        inputan_kasir.value = ""  # Reset the kasir dropdown
        inputan_kasir.visible = False

        inputan_id_user.update()
        inputan_username.update()
        inputan_password.update()
        inputan_hak_akses.update()
        inputan_kasir.update()

    # Fungsi untuk menyimpan data pengguna ke database
    def simpan_data_user(e):
        try:
            cursor.execute("SELECT MAX(id_user) FROM user")
            max_id_user = cursor.fetchone()[0]
            next_id_user = max_id_user + 1 if max_id_user is not None else 1

            if (inputan_id_user.value == ''):
                sql = "INSERT INTO user (id_user, username, password, hak_akses) VALUES(%s, %s, %s, %s)"
                val = (next_id_user, inputan_username.value, inputan_password.value, inputan_hak_akses.value)

                sql_kasir = "UPDATE kasir SET id_user = %s WHERE id_kasir = %s"
                val_kasir = (next_id_user, inputan_kasir.value)
            else:
                sql = "UPDATE user SET username = %s, password = %s, hak_akses = %s WHERE id_user = %s"
                val = (inputan_username.value, inputan_password.value, inputan_hak_akses.value, inputan_id_user.value)
                sql_kasir = ''
                val_kasir = ''

            cursor.execute(sql, val)
            if sql_kasir:
                cursor.execute(sql_kasir, val_kasir)
            koneksi_db.commit()
            print(cursor.rowcount, "Data di simpan!")
            data_user = ambil_data_user()  
            nonlocal filtered_data_user
            filtered_data_user = data_user  

            update_baris_data_user()
            snack_bar_berhasil.open = True
            snack_bar_berhasil.update()
            bersihkan_form_entri() 

        except Exception as e:
            print(e)
            print("Ada yang error!")

    # Fungsi untuk menghapus data pengguna
    def hapus_data_user(e):
        try:
            sql = "DELETE FROM user WHERE id_user = %s"
            val = (e.control.data,)
            cursor.execute(sql, val)
            koneksi_db.commit()
            print(cursor.rowcount, "Data di hapus!")
            data_user = ambil_data_user()  
            nonlocal filtered_data_user
            filtered_data_user = data_user  

            update_baris_data_user()

            snack_bar_berhasil.open = True
            snack_bar_berhasil.update()
            bersihkan_form_entri()

        except Exception as e:
            print(e)
            print("Ada yang error!")

    # Variabel untuk menyimpan data pengguna yang telah difilter
    filtered_data_user = data_user

    # Fungsi untuk memfilter data pengguna berdasarkan input di search field
    def filter_user(e):
        data_user = ambil_data_user()  # Mengambil kembali data pengguna yang terbaru dari database
        query_pencarian = inputan_pencarian.value.lower()  # Mendapatkan kata pencarian dalam huruf kecil
        nonlocal filtered_data_user
        filtered_data_user = [user_kolom for user_kolom in data_user if query_pencarian in user_kolom[1].lower()]
        update_baris_data_user()  # Memperbarui DataTable setelah difilter

    # Menghubungkan fungsi filter dengan perubahan nilai di search field
    inputan_pencarian.on_change = filter_user

    # Fungsi untuk membuat DataRow berdasarkan data pengguna yang sudah difilter
    def update_baris_data_user():
        nonlocal baris_data_user
        index_mulai = hal_sekarang * baris_data_per_hal
        index_selesai = index_mulai + baris_data_per_hal
        hal_data = filtered_data_user[index_mulai:index_selesai]  # Mendapatkan data sesuai dengan halaman yang aktif

        baris_data_user = [
            DataRow(
                cells=[
                    DataCell(Text(str(index_mulai + i + 1))),  # Nomor urut otomatis
                    DataCell(Text(user_kolom[1])),  # Username
                    DataCell(Text(user_kolom[2])),  # Password
                    DataCell(Text(user_kolom[3])),  # Hak Akses
                    DataCell(
                        Row([
                            IconButton("create", icon_color="grey", data=user_kolom, on_click=detail_data_user),
                            IconButton("delete", icon_color="red", data=user_kolom[0], on_click=hapus_data_user),
                        ])
                    ),
                ]
            )
            for i, user_kolom in enumerate(hal_data)
        ]

        tabel_data_user.rows = baris_data_user
        tabel_data_user.update()  # Menyegarkan DataTable untuk menampilkan baris yang sudah diperbarui

    # Inisialisasi pembuatan DataRow berdasarkan data pengguna yang sudah difilter
    baris_data_user = [
        DataRow(
            cells=[
                DataCell(Text(str(i + 1))),  # Nomor urut otomatis
                DataCell(Text(user_kolom[1])),  # Username
                DataCell(Text(user_kolom[2])),  # Password
                DataCell(Text(user_kolom[3])),  # Hak Akses
                DataCell(
                    Row([
                        IconButton("create", icon_color="grey", data=user_kolom, on_click=detail_data_user),
                        IconButton("delete", icon_color="red", data=user_kolom[0], on_click=hapus_data_user),
                    ])
                ),
            ]
        )
        for i, user_kolom in enumerate(filtered_data_user[:baris_data_per_hal])
    ]

    # Membuat DataTable dan menyimpannya dalam variabel
    tabel_data_user = DataTable(
        columns=[
            DataColumn(Text("No.")),
            DataColumn(Text("Username")),
            DataColumn(Text("Password")),
            DataColumn(Text("Hak Akses")),
            DataColumn(Text("Opsi")),
        ],
        rows=baris_data_user,  # Menggunakan baris yang dibuat secara dinamis berdasarkan data yang sudah difilter
        width="auto",  # Menyesuaikan lebar secara otomatis berdasarkan konten
    )

    # Kontrol untuk tombol navigasi pagination
    def pergi_hal_sebelumnya(e):
        nonlocal hal_sekarang
        if hal_sekarang > 0:
            hal_sekarang -= 1
            update_baris_data_user()  # Memperbarui tabel dengan data halaman baru

    def pergi_hal_selanjutnya(e):
        nonlocal hal_sekarang
        if (hal_sekarang + 1) * baris_data_per_hal < len(filtered_data_user):
            hal_sekarang += 1
            update_baris_data_user()  # Memperbarui tabel dengan data halaman baru

    btn_sebelumnya = ElevatedButton("Sebelumnya", on_click=pergi_hal_sebelumnya)
    btn_selanjutnya = ElevatedButton("Berikutnya", on_click=pergi_hal_selanjutnya)

    # Membuat bagian kiri dengan form
    form_kiri = Container(
        Column(
            controls = [
                Text("Form Entri", size = 14, weight = FontWeight.BOLD),
                inputan_id_user,
                Text("Masukkan Username :"),
                inputan_username,
                Text("Masukkan Password :"),
                inputan_password,
                Text("Masukkan Hak Akses :"),
                inputan_hak_akses,
                inputan_kasir,
                Row(
                    controls = [
                        ElevatedButton("S i m p a n", on_click = simpan_data_user),
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
        Column(
            controls = [
                Text("Tabel Data", size = 14, weight = FontWeight.BOLD),
                inputan_pencarian,  # Menambahkan search field di sini
                Row(
                    controls = [
                        tabel_data_user  # Menampilkan DataTable
                    ],
                    scroll = "always",  # Membolehkan scroll horizontal pada Row
                ),
                Row([btn_sebelumnya, btn_selanjutnya]),  # Menambahkan tombol navigasi di sini
            ],
            width = "700",  # Lebar bagian kanan
            scroll="always",  # Membolehkan scroll vertikal pada Column
        ),
        border_radius = 20,
        border = border.all(color = colors.GREY_900, width = 0.5),
        padding = 20,
    )

    # Menambahkan baris ke halaman
    return Container(  # Wrap seluruh Column ke dalam Container
        content = Column(
            controls = [
                # Baris pertama
                Row([
                        Icon(name = icons.PERSON_PIN_ROUNDED, size = 50, color = colors.BLUE_400),
                        Text("Kelola Akun Pengguna", size = 30, weight = "bold")
                    ], alignment = MainAxisAlignment.CENTER),
                Row(
                    controls = [form_kiri, form_kanan],
                    alignment = MainAxisAlignment.START,  # Menyusun item di kiri
                    vertical_alignment = CrossAxisAlignment.START,  # Menyusun item di atas secara vertikal
                ),
                snack_bar_berhasil, snack_bar_gagal
            ]
        ),
        margin = 10    # Memberikan jarak di luar container
    )
