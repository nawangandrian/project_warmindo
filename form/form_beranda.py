from flet import *
from flet.matplotlib_chart import MatplotlibChart
import matplotlib.pyplot as plt
import mysql.connector
import matplotlib
matplotlib.use('Agg')

# Koneksi ke database MySQL
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
    data = cursor.fetchone()
    cursor.close()
    koneksi_db.close()  # Menutup koneksi setelah query selesai
    return data

# Fungsi untuk mendapatkan data penjualan per menu
def get_penjualan_per_menu():
    query = """
        SELECT Nama_Menu, SUM(Jumlah) AS Total_Jual
        FROM detail_transaksi
        JOIN menu ON detail_transaksi.ID_Menu = menu.ID_Menu
        GROUP BY Nama_Menu
        ORDER BY Total_Jual DESC
    """
    koneksi_db = get_db_connection()
    cursor = koneksi_db.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    koneksi_db.close()
    return data

# Fungsi untuk membuat pie chart
def buat_pie_chart(data_dict):
    labels = data_dict.keys()
    sizes = data_dict.values()
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0', '#ffb3e6']
    explode = [0.1] + [0] * (len(labels) - 1)
    
    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    return fig

# Fungsi untuk membuat bar chart
def buat_bar_chart(data):
    labels = [item[0] for item in data]  # Nama menu
    values = [item[1] for item in data]  # Total penjualan

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(labels, values, color='#66b3ff', alpha=0.7)
    ax.set_title('Penjualan per Menu', fontsize=16)
    ax.set_xlabel('Menu', fontsize=12)
    ax.set_ylabel('Total Penjualan', fontsize=12)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha='right')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    return fig

# Fungsi untuk mendapatkan jumlah data dari tabel transaksi
def hitung_transaksi():
    query = "SELECT COUNT(*) FROM transaksi"
    result = get_data_from_table(query) 
    return result[0]

# Fungsi untuk mendapatkan jumlah data dari tabel kasir
def hitung_kasir():
    query = "SELECT COUNT(*) FROM kasir"
    result = get_data_from_table(query) 
    return result[0]

# Fungsi untuk mendapatkan jumlah data dari tabel menu
def hitung_menu():
    query = "SELECT COUNT(*) FROM menu"
    result = get_data_from_table(query) 
    return result[0]

# Fungsi untuk menghitung jumlah pelanggan
def hitung_pelanggan():
    query = "SELECT COUNT(*) FROM pelanggan"
    result = get_data_from_table(query) 
    return result[0]

def hitung_jumlah_data(table_name):
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    return cursor.fetchone()[0]

# Halaman Beranda
def form_beranda():
    data_chart = {
        "Transaksi": hitung_jumlah_data("transaksi"),
        "Pelanggan": hitung_jumlah_data("pelanggan"),
        "Menu": hitung_jumlah_data("menu"),
        "Kasir": hitung_jumlah_data("kasir"),
    }

    pie_chart_fig = buat_pie_chart(data_chart)
    penjualan_data = get_penjualan_per_menu()
    bar_chart_fig = buat_bar_chart(penjualan_data)

    # Mengambil jumlah data dari tabel transaksi
    transaksi_count = hitung_transaksi()

    # Mengambil jumlah data dari tabel kasir
    kasir_count = hitung_kasir()

    # Mengambil jumlah data dari tabel menu
    menu_count = hitung_menu()

    # Mengambil jumlah data dari tabel pelanggan
    pelanggan_count = hitung_pelanggan()

    return Container(
        content=Column([
            Row([  # Center the title
                Icon(name=icons.HOME_ROUNDED, size=50, color=colors.BLUE_400),
                Text("Beranda", size=30, weight="bold")
            ], alignment=MainAxisAlignment.START),

            Row([  # Image banner and title at the top
                Container(
                    content=Stack(
                        controls=[ 
                            Image(
                                src="bg9.jpg",
                                width=1050,
                                height=200,
                                border_radius=10,
                                fit="cover",
                            ),
                            Container(
                                content=Text(
                                    "Menu Aplikasi Penjualan Warmindo",
                                    size=35,
                                    color=colors.WHITE,
                                    weight="bold",
                                    text_align="center",
                                ),
                                alignment=alignment.center,  # Center the text
                            ),
                        ],
                    ),
                    width=1050,
                    height=200,
                ),
            ], alignment="center"),  # Centers the row in the page

            Row([
                Container(
                    content=MatplotlibChart(pie_chart_fig),
                    height=400,
                    width=400,
                    border=border.all(color=colors.GREY_900, width=0.5),
                    border_radius=10,
                    bgcolor=colors.WHITE,
                    alignment=alignment.center,
                ),
                Container(
                    content=MatplotlibChart(bar_chart_fig),
                    height=400,
                    width=600,
                    border=border.all(color=colors.GREY_900, width=0.5),
                    border_radius=10,
                    bgcolor=colors.WHITE,
                    alignment=alignment.center,
                ),
            ], alignment=MainAxisAlignment.CENTER),


            
            Row([  # Baris pertama: Menampilkan data jumlah transaksi, kasir, menu, dan pelanggan
                Container(  # Wrap cards in a container to control the layout
                    content=Row([ 
                        Card(
                            content=Container(
                                content=Column([
                                    Icon(name=icons.INFO_ROUNDED, size=30, color=colors.GREY_900),
                                    Text(f"{transaksi_count} data", size=35, weight="bold"),
                                    Text("Transaksi", size=12),
                                ]),
                                padding=10,
                                bgcolor=colors.RED_100,
                                width=250,
                                height=150,
                                border_radius=15,
                                border=border.all(color=colors.GREY_900, width=0.5)
                            ),
                            elevation=3
                        ),
                        Card(
                            content=Container(
                                content=Column([
                                    Icon(name=icons.INFO_ROUNDED, size=30, color=colors.GREY_900),
                                    Text(f"{kasir_count} data", size=35, weight="bold"),
                                    Text("Kasir", size=12),
                                ]),
                                padding=10,
                                bgcolor=colors.GREEN_100,
                                width=250,
                                height=150,
                                border_radius=15,
                                border=border.all(color=colors.GREY_900, width=0.5)
                            ),
                            elevation=3
                        ),
                        Card(
                            content=Container(
                                content=Column([
                                    Icon(name=icons.INFO_ROUNDED, size=30, color=colors.GREY_900),
                                    Text(f"{menu_count} data", size=35, weight="bold"),
                                    Text("Menu", size=12),
                                ]),
                                padding=10,
                                bgcolor=colors.BLUE_100,
                                width=250,
                                height=150,
                                border_radius=15,
                                border=border.all(color=colors.GREY_900, width=0.5)
                            ),
                            elevation=3
                        ),
                        Card(
                            content=Container(
                                content=Column([
                                    Icon(name=icons.INFO_ROUNDED, size=30, color=colors.GREY_900),
                                    Text(f"{pelanggan_count} data", size=35, weight="bold"),
                                    Text("Pelanggan", size=12),
                                ]),
                                padding=10,
                                bgcolor=colors.PURPLE_100,
                                width=250,
                                height=150,
                                border_radius=15,
                                border=border.all(color=colors.GREY_900, width=0.5)
                            ),
                            elevation=3
                        ),
                    ], alignment=MainAxisAlignment.CENTER),  # Center the cards
                ),
            ], alignment=MainAxisAlignment.CENTER),

            Row([  # Baris ketiga untuk copyright atau informasi tambahan
            ], alignment=MainAxisAlignment.CENTER),

            Row([  # Copyright information at the bottom
                Icon(name=icons.COPYRIGHT_ROUNDED, size=14),
                Text("Mobile Application Development", size=14, weight="bold"),
                Text(" - ", size=14, weight="bold"),
                Text("Nawang Alan Andrian", size=14),
            ], alignment=MainAxisAlignment.CENTER),
        ],
        scroll="adaptive",  # Mengaktifkan scroll untuk seluruh konten Column
        ),
        margin=10,
        width=1150,  # Lebar bagian transaksi
        height=750,  # Tinggi maksimal sebelum scroll muncul
    )