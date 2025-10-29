from flet import *
import mysql.connector

# Setup koneksi ke database MySQL
koneksi_db = mysql.connector.connect(host="localhost", user="root", password="", database="mad_uas_db_2024_202153019")
cursor = koneksi_db.cursor()

# Fungsi untuk mengambil data pelanggan dari database MySQL
def ambil_data_pelanggan():
    # Query untuk mengambil data pelanggan
    query = "SELECT * FROM pelanggan ORDER BY ID_Pelanggan DESC"
    cursor.execute(query)

    # Mengambil semua baris data
    data_pelanggan = cursor.fetchall()

    return data_pelanggan

# Halaman kelola pelanggan
def form_kelola_pelanggan():
    # Mengambil data pelanggan dari database MySQL
    data_pelanggan = ambil_data_pelanggan()

    # Variabel untuk paginasi
    baris_data_per_hal = 5  # Jumlah baris per halaman
    hal_sekarang = 0  # Mulai dari halaman pertama

    # Membuat inputan untuk form entri
    inputan_pencarian = TextField(label="Cari by Nama Pelanggan", width=300, autofocus=True)  # Pencarian pelanggan
    inputan_id_pelanggan = TextField(visible=False, width=300)  # Field ID yang disembunyikan
    inputan_nama_pelanggan = TextField(label="Nama Pelanggan", width=300)

    def validate_numeric_input(e):
        # Only allow numbers, if the input has anything other than digits, reset the value
        if not e.control.value.isdigit():
            e.control.value = ''.join([char for char in e.control.value if char.isdigit()])
        e.control.update()

    inputan_no_telepon = TextField(label="No Telepon", width=300, on_change=validate_numeric_input)
    inputan_alamat_pelanggan = TextField(label="Alamat Pelanggan", width=300)
    snack_bar_berhasil = SnackBar(Text("Operasi berhasil"), bgcolor="green")
    snack_bar_gagal = SnackBar(Text("Operasi gagal"), bgcolor="red")

    # Fungsi untuk membersihkan form entri
    def bersihkan_form_entri(e=None):
        inputan_id_pelanggan.value = ""
        inputan_nama_pelanggan.value = ""
        inputan_no_telepon.value = ""
        inputan_alamat_pelanggan.value = ""
        
        inputan_id_pelanggan.update()
        inputan_nama_pelanggan.update()
        inputan_no_telepon.update()
        inputan_alamat_pelanggan.update()

    # Fungsi untuk mengisi data pelanggan ke dalam form entri (edit data)
    def detail_data_pelanggan(e):
        inputan_id_pelanggan.value = e.control.data[0]
        inputan_nama_pelanggan.value = e.control.data[1]
        inputan_no_telepon.value = e.control.data[2]
        inputan_alamat_pelanggan.value = e.control.data[3]
        
        inputan_id_pelanggan.update()
        inputan_nama_pelanggan.update()
        inputan_no_telepon.update()
        inputan_alamat_pelanggan.update()

    # Fungsi untuk menyimpan data pelanggan ke database
    def simpan_data_pelanggan(e):
        try:
            if (inputan_id_pelanggan.value == ''):
                sql = "INSERT INTO pelanggan (Nama_Pelanggan, No_Telepon_Pelanggan, Alamat_Pelanggan) VALUES(%s, %s, %s)"
                val = (inputan_nama_pelanggan.value, inputan_no_telepon.value, inputan_alamat_pelanggan.value)
            else:
                sql = "UPDATE pelanggan SET Nama_Pelanggan = %s, No_Telepon_Pelanggan = %s, Alamat_Pelanggan = %s WHERE ID_Pelanggan = %s"
                val = (inputan_nama_pelanggan.value, inputan_no_telepon.value, inputan_alamat_pelanggan.value, inputan_id_pelanggan.value)
            
            cursor.execute(sql, val)
            koneksi_db.commit()
            print(cursor.rowcount, "Data disimpan!")
            
            data_pelanggan = ambil_data_pelanggan()  # Mengambil kembali data pelanggan yang terbaru dari database
            nonlocal filtered_data_pelanggan
            filtered_data_pelanggan = data_pelanggan  # Update filtered data pelanggan

            update_baris_data_pelanggan()
            bersihkan_form_entri()

            snack_bar_berhasil.open = True
            snack_bar_berhasil.update()

        except Exception as e:
            print(e)
            print("Ada yang error!")

    # Fungsi untuk menghapus data pelanggan
    def hapus_data_pelanggan(e):
        try:
            sql = "DELETE FROM pelanggan WHERE ID_Pelanggan = %s"
            val = (e.control.data,)
            cursor.execute(sql, val)
            koneksi_db.commit()
            print(cursor.rowcount, "Data dihapus!")

            data_pelanggan = ambil_data_pelanggan()  # Mengambil kembali data pelanggan yang terbaru dari database
            nonlocal filtered_data_pelanggan
            filtered_data_pelanggan = data_pelanggan  # Update filtered data pelanggan

            update_baris_data_pelanggan()

            snack_bar_berhasil.open = True
            snack_bar_berhasil.update()
            bersihkan_form_entri()
            
        except Exception as e:
            print(e)
            print("Ada yang error!")

    # Variabel untuk menyimpan data pelanggan yang telah difilter
    filtered_data_pelanggan = data_pelanggan

    # Fungsi untuk memfilter data pelanggan berdasarkan input di search field
    def filter_pelanggan(e):
        data_pelanggan = ambil_data_pelanggan()  # Mengambil kembali data pelanggan yang terbaru dari database
        query_pencarian = inputan_pencarian.value.lower()  # Mendapatkan kata pencarian dalam huruf kecil
        nonlocal filtered_data_pelanggan
        filtered_data_pelanggan = [pelanggan_kolom for pelanggan_kolom in data_pelanggan if query_pencarian in pelanggan_kolom[1].lower()]
        update_baris_data_pelanggan()

    # Menghubungkan fungsi filter dengan perubahan nilai di search field
    inputan_pencarian.on_change = filter_pelanggan

    # Fungsi untuk membuat DataRow berdasarkan data pelanggan yang sudah difilter
    def update_baris_data_pelanggan():
        nonlocal baris_data_pelanggan
        index_mulai = hal_sekarang * baris_data_per_hal
        index_selesai = index_mulai + baris_data_per_hal
        hal_data = filtered_data_pelanggan[index_mulai:index_selesai]  # Mendapatkan data sesuai dengan halaman yang aktif
        
        baris_data_pelanggan = [
            DataRow(
                cells=[
                    DataCell(Text(str(index_mulai + i + 1))),  # Nomor urut otomatis
                    DataCell(Text(pelanggan_kolom[1])),  # Nama Pelanggan
                    DataCell(Text(pelanggan_kolom[2])),  # No Telepon
                    DataCell(Text(pelanggan_kolom[3])),  # Alamat Pelanggan
                    DataCell(
                        Row([
                            IconButton("create", icon_color="grey", data=pelanggan_kolom, on_click=detail_data_pelanggan),
                            IconButton("delete", icon_color="red", data=pelanggan_kolom[0], on_click=hapus_data_pelanggan),
                        ])
                    ),
                ]
            )
            for i, pelanggan_kolom in enumerate(hal_data)
        ]
        
        tabel_data_pelanggan.rows = baris_data_pelanggan
        tabel_data_pelanggan.update()  # Menyegarkan DataTable untuk menampilkan baris yang sudah diperbarui

    # Inisialisasi pembuatan DataRow berdasarkan data pelanggan yang sudah difilter
    baris_data_pelanggan = [
        DataRow(
            cells=[
                DataCell(Text(str(i + 1))),
                DataCell(Text(pelanggan_kolom[1])),  # Nama Pelanggan
                DataCell(Text(pelanggan_kolom[2])),  # No Telepon
                DataCell(Text(pelanggan_kolom[3])),  # Alamat Pelanggan
                DataCell(
                    Row([
                        IconButton("create", icon_color="grey", data=pelanggan_kolom, on_click=detail_data_pelanggan),
                        IconButton("delete", icon_color="red", data=pelanggan_kolom[0], on_click=hapus_data_pelanggan),
                    ])
                ),
            ]
        )
        for i, pelanggan_kolom in enumerate(filtered_data_pelanggan[:baris_data_per_hal])
    ]

    tabel_data_pelanggan = DataTable(
        columns=[
            DataColumn(Text("No.")),
            DataColumn(Text("Nama Pelanggan")),
            DataColumn(Text("No Telepon")),
            DataColumn(Text("Alamat Pelanggan")),
            DataColumn(Text("Opsi")),
        ],
        rows=baris_data_pelanggan,
        width="auto",
    )

    # Kontrol untuk tombol navigasi pagination
    def pergi_hal_sebelumnya(e):
        nonlocal hal_sekarang
        if hal_sekarang > 0:
            hal_sekarang -= 1
            update_baris_data_pelanggan()

    def pergi_hal_selanjutnya(e):
        nonlocal hal_sekarang
        if (hal_sekarang + 1) * baris_data_per_hal < len(filtered_data_pelanggan):
            hal_sekarang += 1
            update_baris_data_pelanggan()

    btn_sebelumnya = ElevatedButton("Sebelumnya", on_click=pergi_hal_sebelumnya)
    btn_selanjutnya = ElevatedButton("Berikutnya", on_click=pergi_hal_selanjutnya)

    # Membuat bagian kiri dengan form
    form_kiri = Container(
        Column(
            controls=[
                Text("Form Entri", size=14, weight=FontWeight.BOLD),
                inputan_id_pelanggan,
                Text("Masukkan Nama Pelanggan :"),
                inputan_nama_pelanggan,
                Text("Masukkan No Telepon :"),
                inputan_no_telepon,
                Text("Masukkan Alamat :"),
                inputan_alamat_pelanggan,
                Row(
                    controls=[
                        ElevatedButton("S i m p a n", on_click=simpan_data_pelanggan),
                        ElevatedButton("Batal", on_click=bersihkan_form_entri),
                    ],
                    alignment=MainAxisAlignment.CENTER,
                    spacing=20,
                ),
            ],
            width=300,
        ),
        border_radius=20,
        border=border.all(color=colors.GREY_900, width=0.5),
        padding=20,
    )

    # Membuat bagian kanan dengan search field dan table
    form_kanan = Container(
        Column(
            controls=[
                Text("Tabel Data", size=14, weight=FontWeight.BOLD),
                inputan_pencarian,
                Row(
                    controls = [
                        tabel_data_pelanggan # Menampilkan DataTable
                    ],
                    scroll = "always",  # Membolehkan scroll horizontal pada Row
                ),
                Row([btn_sebelumnya, btn_selanjutnya]),
            ],
            width="700",  # Lebar bagian kanan
            scroll="always",  # Membolehkan scroll vertikal pada Column
        ),
        border_radius=20,
        border=border.all(color=colors.GREY_900, width=0.5),
        padding=20,
    )

    return Container(  # Wrap seluruh Column ke dalam Container
        content=Column(
            controls=[
                Row([Icon(name=icons.PERSON_ADD_ROUNDED, size=50, color=colors.BLUE_400), Text("Kelola Pelanggan", size=30, weight="bold")], alignment=MainAxisAlignment.CENTER),
                Row(controls=[form_kiri, form_kanan], alignment=MainAxisAlignment.START, vertical_alignment=CrossAxisAlignment.START),
                snack_bar_berhasil, snack_bar_gagal
            ]
        ),
        margin=10
    )
