from flet import *
import mysql.connector
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import inch
import os
import webbrowser

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
    cursor = koneksi_db.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    koneksi_db.close()  # Menutup koneksi setelah query selesai
    return data

def ambil_data_transaksi():
    # Query untuk mengambil data transaksi
    query = "SELECT * FROM transaksi ORDER BY ID_Transaksi DESC"
    data_transaksi = get_data_from_table(query) 

    return data_transaksi

def format_tanggal(tanggal):
    if isinstance(tanggal, datetime):
        return tanggal.strftime("%d-%m-%Y %H:%M:%S")
    return str(tanggal)

def format_tanggal_dmy(tanggal):
    return tanggal.strftime("%d-%m-%Y")

def draw_line(c, y, x_start, x_end):
    c.line(x_start, y, x_end, y)

def halaman_baru(c, page_width, page_height, center_x):
    """Menambahkan halaman baru dan mengatur ulang posisi y"""
    c.showPage()  # Buat halaman baru
    return page_height - 1 * inch  # Reset y ke posisi atas halaman baru

def buat_pdf_pratinjau(data_transaksi):
    # Setup untuk ukuran halaman dan file PDF
    page_width = 6 * inch
    page_height = 8 * inch
    id_transaksi = str(data_transaksi[0][1])  # Misal kolom [0][1] adalah ID Transaksi
    pdf_file = f"nota_transaksi_{id_transaksi}.pdf"
    logo_path = "shop.png"  # Ganti dengan path logo Anda
    c = canvas.Canvas(pdf_file, pagesize=(page_width, page_height))

    # Margin dan posisi awal
    margin_left = 0.5 * inch
    margin_right = page_width - 0.5 * inch
    column_pos = margin_left + 0.5 * inch  # Posisi tetap untuk titik dua
    center_x = page_width / 2
    y = page_height - 1 * inch  # Mulai dari bawah header, lebih dekat dengan atas

    # Menambahkan logo
    c.drawImage(logo_path, center_x - 0.4 * inch, y, width=0.8 * inch, height=0.8 * inch, preserveAspectRatio=True, mask='auto')
    y -= 0.5 * inch  # Logo lebih dekat dengan judul

    # Header restoran
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(center_x, y, "WARMINDO KUDUS")
    y -= 15
    c.setFont("Helvetica", 8)
    c.drawCentredString(center_x, y, "Rahtawu Raya Street No. 2, Gondosari, Gebog District, Kudus Regency")
    y -= 25

    # Informasi umum
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(center_x, y, str(data_transaksi[0][10]))  # Tampilkan Jenis Pesanan dari data_transaksi
    y -= 20

    # Garis pemisah
    draw_line(c, y, margin_left, margin_right)
    y -= 20

    # Detail transaksi
    c.setFont("Helvetica", 9)
    c.drawString(margin_left, y, "Cashier")
    c.drawString(column_pos + 5, y, ":")
    c.drawString(column_pos + 10, y, str(data_transaksi[0][7]))  # Nama Kasir
    c.drawRightString(margin_right - 1 * inch, y, "Date")
    c.drawString(margin_right - 0.9 * inch, y, ": " + format_tanggal_dmy(data_transaksi[0][13]))  # Tanggal Transaksi
    y -= 15

    c.drawString(margin_left, y, "Customer")
    c.drawString(column_pos + 5, y, ":")
    c.drawString(column_pos + 10, y, str(data_transaksi[0][6]))  # Nama Pelanggan
    c.drawRightString(margin_right - 1 * inch, y, "Trx ID")
    c.drawString(margin_right - 0.9 * inch, y, ": " + str(data_transaksi[0][1]))  # ID Transaksi
    y -= 20

    # Garis pemisah
    draw_line(c, y, margin_left, margin_right)
    y -= 20

    # Daftar pesanan (loop untuk menampilkan item pesanan)
    subtotal = 0  # Inisialisasi subtotal
    for i, item in enumerate(data_transaksi):
        c.setFont("Helvetica-Bold", 9)
        c.drawString(margin_left, y, item[3] + " x" + str(item[4]))  # Nama menu dan jumlah
        c.drawRightString(margin_right, y, "Rp. " + "{:,.0f}".format(item[5]))  # Menampilkan jumlah total per item
        subtotal += item[5]  # Menambahkan total item ke subtotal
        y -= 15

        c.setFont("Helvetica", 9)
        c.drawString(margin_left, y, "Rp. " + "{:,.0f}".format(item[14]))
        y -= 20

        # Cek apakah posisi y sudah terlalu dekat dengan bawah halaman, jika ya, buat halaman baru
        if y < 1 * inch:
            y = halaman_baru(c, page_width, page_height, center_x)  # Membuat halaman baru

    # Garis pemisah
    draw_line(c, y, margin_left, margin_right)
    y -= 20

    # Detail pembayaran
    c.setFont("Helvetica-Bold", 9)
    c.drawString(margin_left, y, "Subtotal")
    c.drawRightString(margin_right, y, "Rp. " + "{:,.0f}".format(subtotal))  # Menampilkan subtotal
    y -= 15

    c.drawString(margin_left, y, "Discount")
    c.drawRightString(margin_right, y, "Rp. " + "{:,.0f}".format(data_transaksi[0][8]))  # Diskon
    y -= 15

    c.drawString(margin_left, y, "Tax")
    c.drawRightString(margin_right, y, "Rp. " + "{:,.0f}".format(data_transaksi[0][9]))  # Pajak
    y -= 15

    c.setFont("Helvetica-Bold", 10)
    c.drawString(margin_left, y, "Total")
    c.drawRightString(margin_right, y, "Rp. " + "{:,.0f}".format(data_transaksi[0][12]))  # Total
    y -= 20

    # Garis pemisah
    draw_line(c, y, margin_left, margin_right)
    y -= 20

    # Metode pembayaran
    c.setFont("Helvetica", 9)
    c.drawString(margin_left, y, "Payment Method")
    c.drawRightString(margin_right, y, str(data_transaksi[0][11]))  # Metode Pembayaran
    y -= 15

    # Garis pemisah
    draw_line(c, y, margin_left, margin_right)
    y -= 20

    # Memastikan ada ruang untuk "Thank you" dan tanggal transaksi, jika tidak ada, buat halaman baru
    if y < 20:
        y = halaman_baru(c, page_width, page_height, center_x)

    # Tulisan PAID rata tengah
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(center_x, y, "PAID")
    y -= 15

    c.setFont("Helvetica", 8)
    c.drawCentredString(center_x, y, format_tanggal(data_transaksi[0][13])[:16])  # Waktu Transaksi
    y -= 20

    # Footer
    c.setFont("Helvetica", 9)
    c.drawCentredString(center_x, y, "Thank you for your order!")

    # Simpan PDF
    c.save()
    return pdf_file

# Halaman kelola riwayat transaksi
def form_kelola_riwayat_transaksi():
    # Mengambil data transaksi dari database MySQL
    data_transaksi = ambil_data_transaksi()

    # Variabel untuk paginasi
    baris_data_per_hal = 5  # Jumlah baris per halaman
    hal_sekarang = 0  # Mulai dari halaman pertama

    # Membuat inputan untuk form entri transaksi
    inputan_pencarian = TextField(label="Cari by ID Transaksi", width=300, autofocus=True)  # Pencarian transaksi
    snack_bar_berhasil = SnackBar(Text("Operasi berhasil"), bgcolor="green")
    snack_bar_gagal = SnackBar(Text("Operasi gagal"), bgcolor="red")

    # Fungsi untuk mengambil detail transaksi berdasarkan ID Transaksi
    def ambil_detail_transaksi(id_transaksi):
        try:
            query = """
            SELECT 
                dt.ID_Detail, -- 0
                dt.ID_Transaksi, -- 1
                dt.ID_Menu, -- 2
                m.Nama_Menu, -- 3
                dt.Jumlah, -- 4
                dt.Subtotal, -- 5
                p.Nama_Pelanggan, -- 6
                k.Nama_Kasir, -- 7
                t.Diskon_Transaksi, -- 8
                t.Pajak_Transaksi, -- 9
                t.Jenis_Pesanan, -- 10
                t.Metode_Pembayaran, -- 11
                t.Total_Harga, -- 12
                t.Tanggal_Transaksi, -- Menambahkan Tanggal Transaksi adalah datetime (2025-01-11 19:59:30)
                m.Harga
            FROM 
                detail_transaksi dt
            JOIN 
                menu m ON dt.ID_Menu = m.ID_Menu
            JOIN 
                transaksi t ON dt.ID_Transaksi = t.ID_Transaksi  -- Menggabungkan transaksi untuk mendapatkan pelanggan
            JOIN 
                pelanggan p ON t.ID_Pelanggan = p.ID_Pelanggan  -- Menggabungkan pelanggan untuk mendapatkan nama pelanggan
            JOIN 
                kasir k ON t.ID_Kasir = k.ID_Kasir  -- Menggabungkan pelanggan untuk mendapatkan nama pelanggan
            WHERE 
                dt.ID_Transaksi = %s
            """
            cursor.execute(query, (id_transaksi,))
            hasil = cursor.fetchall()
            koneksi_db.commit()
            print(f"Detail transaksi untuk ID {id_transaksi}: {hasil}")  # Log hasil query
            return hasil
        except Exception as e:
            print(f"Error: {e}")
            return []
        
    detail_dialog = None 

    # Fungsi untuk menampilkan dialog detail transaksi
    def lihat_detail_transaksi(e):
        global detail_dialog
        id_transaksi = e.control.data  # Mendapatkan ID Transaksi dari tombol
        data_detail = ambil_detail_transaksi(id_transaksi)
        nama_pelanggan = data_detail[0][6]

        # Buat baris untuk detail transaksi
        detail_rows = [
            Row([
                Text(f"{i + 1}.", weight="bold"),  # Nomor urut
                Column([
                    Text(f"ID Menu: {detail[2]}"),
                    Text(f"Nama Menu: {detail[3]}"),
                    Text(f"Jumlah: {detail[4]}"),
                    Text(f"Subtotal: Rp {detail[5]:,}"),
                    Divider(), 
                ])
            ])
            for i, detail in enumerate(data_detail)
        ]

        # Konten dialog
        dialog_content = Column(
            controls=[
                Text(f"Detail Transaksi (ID: {id_transaksi})", size=18, weight="bold"),
                Text(f"Nama Pelanggan: {nama_pelanggan}", size=16, weight="bold", color=colors.BLUE_400),
                Divider(),
            ] + detail_rows + [
                Divider(),
                Row(
                    controls=[
                        ElevatedButton("Tutup", on_click=tutup_dialog),
                    ],
                    alignment="end",
                ),
            ],
            scroll="always",  # Menambahkan scroll yang selalu aktif
        )

        # Membuat dialog
        detail_dialog = AlertDialog(
            title=Row(
                controls=[
                    Icon(icons.LIST_ALT, size=30, color=colors.BLUE_400),
                    Text("Detail Transaksi", size=20, weight="bold"),
                ],
                alignment="start",
                spacing=10,
            ),
            content=Container(
                content=dialog_content,  # Konten dialog di dalam Container
                width=500,  # Lebar tetap untuk dialog
            ),
            actions=[],
        )

        # Menampilkan dialog
        hal_riwayat.content.controls.append(detail_dialog)
        detail_dialog.open = True
        hal_riwayat.update()

    # Fungsi untuk menutup dialog
    def tutup_dialog(e):
        global detail_dialog  # Mengakses variabel global detail_dialog
        if detail_dialog:
            detail_dialog.open = False
            hal_riwayat.update()

    # Fungsi untuk menghapus data transaksi dan detailnya
    def hapus_data_transaksi(e):
        try:
            id_transaksi = e.control.data  # Mendapatkan ID Transaksi dari tombol

            # Pertama, hapus data dari tabel detail_transaksi yang mengacu pada ID_Transaksi
            sql_detail = "DELETE FROM detail_transaksi WHERE ID_Transaksi = %s"
            val_detail = (id_transaksi,)
            cursor.execute(sql_detail, val_detail)
            koneksi_db.commit()
            print(cursor.rowcount, "Data detail transaksi dihapus!")

            # Kemudian, hapus data dari tabel transaksi
            sql = "DELETE FROM transaksi WHERE ID_Transaksi = %s"
            val = (id_transaksi,)
            cursor.execute(sql, val)
            koneksi_db.commit()
            print(cursor.rowcount, "Data transaksi dihapus!")

            # Update data transaksi setelah penghapusan
            data_transaksi = ambil_data_transaksi()  # Mengambil kembali data transaksi yang terbaru dari database
            nonlocal filtered_data_transaksi
            filtered_data_transaksi = data_transaksi  # Update filtered data transaksi

            update_baris_data_transaksi()

            # Menampilkan SnackBar Berhasil
            snack_bar_berhasil.open = True
            snack_bar_berhasil.update()

        except Exception as e:
            print(e)
            print("Ada yang error!")

    # Variabel untuk menyimpan data transaksi yang telah difilter
    filtered_data_transaksi = data_transaksi

    def print_nota_transaksi(e=None):
        # Pastikan ada data transaksi yang telah difilter
        if e is not None:
            id_transaksi = e.control.data  # Mendapatkan ID Transaksi dari tombol
            data_transaksi = ambil_detail_transaksi(id_transaksi)
            
            # Pastikan data transaksi ada
            if data_transaksi:
                # Membuat file PDF pratinjau dengan data transaksi
                pdf_file = buat_pdf_pratinjau(data_transaksi)
                
                # Buka file PDF di browser
                webbrowser.open("file://" + os.path.abspath(pdf_file))
            else:
                # Jika data transaksi tidak ditemukan
                snack_bar_gagal.text = "Transaksi tidak ditemukan."
                snack_bar_gagal.open()
        else:
            # Jika tidak ada ID Transaksi yang diberikan
            snack_bar_gagal.text = "ID Transaksi tidak valid."
            snack_bar_gagal.open()

    # Tambahkan tombol untuk melihat detail transaksi di tabel transaksi utama
    def update_baris_data_transaksi():
        nonlocal baris_data_transaksi
        index_mulai = hal_sekarang * baris_data_per_hal
        index_selesai = index_mulai + baris_data_per_hal
        hal_data = filtered_data_transaksi[index_mulai:index_selesai]

        baris_data_transaksi = [
            DataRow(
                cells=[
                    DataCell(Text(str(index_mulai + i + 1))),
                    DataCell(Text(transaksi_kolom[0])),  # ID Transaksi
                    DataCell(Text(transaksi_kolom[8])),  # ID Pelanggan
                    DataCell(Text(transaksi_kolom[1].date())),  # Tanggal Transaksi
                    DataCell(Text(transaksi_kolom[2])),  # Jumlah
                    DataCell(Text(transaksi_kolom[6])),  # Status Transaksi
                    DataCell(Text(transaksi_kolom[7])),  # Transaksi
                    DataCell(
                        Row([
                            IconButton("print", icon_color="green", data=transaksi_kolom[0], on_click=print_nota_transaksi),
                            IconButton("visibility", icon_color="blue", data=transaksi_kolom[0], on_click=lihat_detail_transaksi),
                            IconButton("delete", icon_color="red", data=transaksi_kolom[0], on_click=hapus_data_transaksi),
                        ])
                    ),
                ]
            )
            for i, transaksi_kolom in enumerate(hal_data)
        ]

        tabel_data_transaksi.rows = baris_data_transaksi
        tabel_data_transaksi.update()

    # Inisialisasi pembuatan DataRow berdasarkan data transaksi yang sudah difilter
    baris_data_transaksi = [
        DataRow(
            cells=[
                DataCell(Text(str(i + 1))),
                DataCell(Text(transaksi_kolom[0])),  # ID Transaksi
                DataCell(Text(transaksi_kolom[8])),  # ID Pelanggan
                DataCell(Text(transaksi_kolom[1].date())),  # Tanggal Transaksi
                DataCell(Text(transaksi_kolom[2])),  # Jumlah
                DataCell(Text(transaksi_kolom[6])),  # Status Transaksi
                DataCell(Text(transaksi_kolom[7])),  # Status Transaksi
                DataCell(
                    Row([
                        IconButton("print", icon_color="green", data=transaksi_kolom[0], on_click=print_nota_transaksi),
                        IconButton("visibility", icon_color="blue", data=transaksi_kolom[0], on_click=lihat_detail_transaksi),
                        IconButton("delete", icon_color="red", data=transaksi_kolom[0], on_click=hapus_data_transaksi),
                    ])
                ),
            ]
        )
        for i, transaksi_kolom in enumerate(filtered_data_transaksi[:baris_data_per_hal])
    ]

    tabel_data_transaksi = DataTable(
        columns=[
            DataColumn(Text("No.")),
            DataColumn(Text("ID Transaksi")),
            DataColumn(Text("ID Pelanggan")),
            DataColumn(Text("Tanggal Transaksi")),
            DataColumn(Text("Jumlah")),
            DataColumn(Text("Metode Pembayaran")),
            DataColumn(Text("Jenis Pesanan")),
            DataColumn(Text("Opsi")),
        ],
        rows=baris_data_transaksi,
        width="auto",
    )

    # Kontrol untuk tombol navigasi pagination
    def pergi_hal_sebelumnya(e):
        nonlocal hal_sekarang
        if hal_sekarang > 0:
            hal_sekarang -= 1
            update_baris_data_transaksi()

    def pergi_hal_selanjutnya(e):
        nonlocal hal_sekarang
        if (hal_sekarang + 1) * baris_data_per_hal < len(filtered_data_transaksi):
            hal_sekarang += 1
            update_baris_data_transaksi()

    btn_sebelumnya = ElevatedButton("Sebelumnya", on_click=pergi_hal_sebelumnya)
    btn_selanjutnya = ElevatedButton("Berikutnya", on_click=pergi_hal_selanjutnya)

    # Membuat bagian kanan dengan search field dan table
    form_kanan = Container(
        Column(
            controls=[
                Text("Tabel Riwayat Transaksi", size=14, weight=FontWeight.BOLD),
                inputan_pencarian,
                Row(
                    controls = [
                        tabel_data_transaksi # Menampilkan DataTable
                    ],
                    scroll = "always",  # Membolehkan scroll horizontal pada Row
                ),
                Row([btn_sebelumnya, btn_selanjutnya]),
            ],
            width="980",
        ),
        border_radius=20,
        border=border.all(color=colors.GREY_900, width=0.5),
        padding=20,
    )

    hal_riwayat = Container(  # Wrap seluruh Column ke dalam Container
        content=Column(
            controls=[
                Row([Icon(name=icons.DATA_THRESHOLDING_ROUNDED, size=50, color=colors.BLUE_400), Text("Kelola Riwayat Transaksi", size=30, weight="bold")], alignment=MainAxisAlignment.CENTER),
                Row(controls=[form_kanan], alignment=MainAxisAlignment.START, vertical_alignment=CrossAxisAlignment.START),
                snack_bar_berhasil, snack_bar_gagal
            ]
        ),
        margin=10
    )

    return hal_riwayat
