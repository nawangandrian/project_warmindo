from flet import *
import mysql.connector

# Setup koneksi ke database MySQL
koneksi_db = mysql.connector.connect(host="localhost", user="root", password="", database="mad_uas_db_2024_202153019")
cursor = koneksi_db.cursor()

# Fungsi untuk mengambil data kasir dari database MySQL
def ambil_data_kasir():
    query = "SELECT * FROM kasir ORDER BY ID_Kasir DESC"
    cursor.execute(query)
    return cursor.fetchall()

# Halaman kelola kasir
def form_kelola_kasir():
    data_kasir = ambil_data_kasir()

    # Variabel untuk paginasi
    baris_data_per_hal = 5
    hal_sekarang = 0

    # Membuat inputan untuk form entri
    inputan_pencarian = TextField(label="Cari Nama Kasir", width=300, autofocus=True)
    inputan_id_kasir = TextField(visible=False, width=300)
    inputan_nama_kasir = TextField(label="Nama Kasir", width=300)
    def validate_numeric_input(e):
        # Only allow numbers, if the input has anything other than digits, reset the value
        if not e.control.value.isdigit():
            e.control.value = ''.join([char for char in e.control.value if char.isdigit()])
        e.control.update()

    inputan_no_telepon = TextField(label="No Telepon", width=300, on_change=validate_numeric_input)
    inputan_alamat = TextField(label="Alamat", width=300)
    
    snack_bar_berhasil = SnackBar(Text("Operasi berhasil"), bgcolor="green")
    snack_bar_gagal = SnackBar(Text("Operasi gagal"), bgcolor="red")

    # Fungsi untuk membersihkan form entri
    def bersihkan_form_entri(e=None):
        inputan_id_kasir.value = ""
        inputan_nama_kasir.value = ""
        inputan_no_telepon.value = ""
        inputan_alamat.value = ""
        inputan_id_kasir.update()
        inputan_nama_kasir.update()
        inputan_no_telepon.update()
        inputan_alamat.update()

    # Fungsi untuk mengisi data kasir ke dalam form entri
    def detail_data_kasir(e):
        inputan_id_kasir.value = e.control.data[0]
        inputan_nama_kasir.value = e.control.data[1]
        inputan_no_telepon.value = e.control.data[2]
        inputan_alamat.value = e.control.data[3]
        inputan_id_kasir.update()
        inputan_nama_kasir.update()
        inputan_no_telepon.update()
        inputan_alamat.update()

    # Fungsi untuk menyimpan data kasir ke database
    def simpan_data_kasir(e):
        try:
            if inputan_id_kasir.value == '':  # Check if it's an insert operation (no ID)
                sql_kasir = """
                INSERT INTO kasir (Nama_Kasir, No_Telepon_Kasir, Alamat_Kasir)
                VALUES (%s, %s, %s)
                """
                val_kasir = (inputan_nama_kasir.value, inputan_no_telepon.value, inputan_alamat.value)
                cursor.execute(sql_kasir, val_kasir)  # Make sure to pass the parameters with execute
            else:
                sql = """
                UPDATE kasir 
                SET Nama_Kasir = %s, No_Telepon_Kasir = %s, Alamat_Kasir = %s
                WHERE ID_Kasir = %s
                """
                val = (inputan_nama_kasir.value, inputan_no_telepon.value, inputan_alamat.value, inputan_id_kasir.value)
                cursor.execute(sql, val)

            koneksi_db.commit()  # Commit the changes to the database
            print(cursor.rowcount, "Data disimpan!")
            bersihkan_form_entri()  # Reset the form after saving
            data_kasir = ambil_data_kasir()  # Refresh the data
            nonlocal filtered_data_kasir
            filtered_data_kasir = data_kasir  # Update filtered data
            update_baris_data_kasir()  # Update the table with the new data
            snack_bar_berhasil.open = True
            snack_bar_berhasil.update()
        except Exception as e:
            print(e)
            snack_bar_gagal.open = True
            snack_bar_gagal.update()

    def hapus_data_kasir(e):
        try:
            print("Data yang akan dihapus:", e.control.data)  # Debugging
            sql = "DELETE FROM kasir WHERE ID_Kasir = %s"
            val = (e.control.data,)
            cursor.execute(sql, val)
            koneksi_db.commit()
            print(cursor.rowcount, "Data dihapus!")

            # Perbarui data kasir
            data_kasir = ambil_data_kasir()
            nonlocal filtered_data_kasir
            filtered_data_kasir = data_kasir
            update_baris_data_kasir()
            snack_bar_berhasil.open = True
            snack_bar_berhasil.update()
        except Exception as err:
            print("Error saat menghapus data:", err)
            snack_bar_gagal.open = True
            snack_bar_gagal.update()

    # Variabel untuk menyimpan data kasir yang telah difilter
    filtered_data_kasir = data_kasir

    # Fungsi untuk memfilter data kasir berdasarkan input di search field
    def filter_kasir(e):
        data_kasir = ambil_data_kasir()
        query_pencarian = inputan_pencarian.value.lower()
        nonlocal filtered_data_kasir
        filtered_data_kasir = [kasir_kolom for kasir_kolom in data_kasir if query_pencarian in kasir_kolom[1].lower()]
        update_baris_data_kasir()

    inputan_pencarian.on_change = filter_kasir

    # Fungsi untuk membuat DataRow berdasarkan data kasir yang sudah difilter
    def update_baris_data_kasir():
        nonlocal baris_data_kasir
        index_mulai = hal_sekarang * baris_data_per_hal
        index_selesai = index_mulai + baris_data_per_hal
        hal_data = filtered_data_kasir[index_mulai:index_selesai]
        
        baris_data_kasir = [
            DataRow(
                cells=[
                    DataCell(Text(str(index_mulai + i + 1))),
                    DataCell(Text(kasir_kolom[1])),
                    DataCell(Text(kasir_kolom[2])),
                    DataCell(Text(kasir_kolom[3])),
                    DataCell(
                        Row([
                            IconButton("create", icon_color="grey", data=kasir_kolom, on_click=detail_data_kasir),
                            IconButton("delete", icon_color="red", data=kasir_kolom[0], on_click=hapus_data_kasir),
                        ])
                    ),
                ]
            )
            for i, kasir_kolom in enumerate(hal_data)
        ]
        tabel_data_kasir.rows = baris_data_kasir
        tabel_data_kasir.update()

    # Inisialisasi pembuatan DataRow berdasarkan data menu yang sudah difilter
    baris_data_kasir = [
        DataRow(
            cells = [
                DataCell(Text(str(i + 1))),  # Nomor urut otomatis (indeks mulai dari 1)
                DataCell(Text(menu_kolom[1])),
                DataCell(Text(menu_kolom[2])),  # Jenis Menu
                DataCell(Text(str(menu_kolom[3]))),  # Harga
                DataCell(
                    Row([
                        IconButton("create", icon_color = "grey", data = menu_kolom, on_click = detail_data_kasir),
                        IconButton("delete", icon_color = "red", data = menu_kolom[0], on_click = hapus_data_kasir),
                    ])
                ),
            ]
        )
        for i, menu_kolom in enumerate(filtered_data_kasir[:baris_data_per_hal])
    ]

    tabel_data_kasir = DataTable(
        columns=[
            DataColumn(Text("No.")),
            DataColumn(Text("Nama Kasir")),
            DataColumn(Text("No Telepon")),
            DataColumn(Text("Alamat")),
            DataColumn(Text("Opsi")),
        ],
        rows=baris_data_kasir,
        width="auto",
    )

    def pergi_hal_sebelumnya(e):
        nonlocal hal_sekarang
        if hal_sekarang > 0:
            hal_sekarang -= 1
            update_baris_data_kasir()

    def pergi_hal_selanjutnya(e):
        nonlocal hal_sekarang
        if (hal_sekarang + 1) * baris_data_per_hal < len(filtered_data_kasir):
            hal_sekarang += 1
            update_baris_data_kasir()

    btn_sebelumnya = ElevatedButton("Sebelumnya", on_click=pergi_hal_sebelumnya)
    btn_selanjutnya = ElevatedButton("Berikutnya", on_click=pergi_hal_selanjutnya)

    form_kiri = Container(
        Column(
            controls=[
                Text("Form Entri", size=14, weight=FontWeight.BOLD),
                inputan_id_kasir,
                Text("Nama Kasir:"),
                inputan_nama_kasir,
                Text("No Telepon:"),
                inputan_no_telepon,
                Text("Alamat:"),
                inputan_alamat,
                Row(
                    controls=[
                        ElevatedButton("Simpan", on_click=simpan_data_kasir),
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

    form_kanan = Container(
        Column(
            controls=[
                Text("Tabel Data", size=14, weight=FontWeight.BOLD),
                inputan_pencarian,
                Row(
                    controls = [
                        tabel_data_kasir,  # Menampilkan DataTable
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

    return Container(
        content=Column(
            controls=[
                Row([
                    Icon(name=icons.PERSON_ADD_ROUNDED, size=50, color=colors.BLUE_400),
                    Text("Kelola Kasir", size=30, weight="bold"),
                ], alignment=MainAxisAlignment.CENTER),
                Row(
                    controls=[form_kiri, form_kanan],
                    alignment=MainAxisAlignment.START,
                    vertical_alignment=CrossAxisAlignment.START,
                ),
                snack_bar_berhasil, snack_bar_gagal,
            ]
        ),
        margin=10,
    )
