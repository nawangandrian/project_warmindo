from flet import *
import mysql.connector
from session_manager import get_session  # Mengimpor dari session_manager

# Koneksi ke database MySQL
koneksi_db = mysql.connector.connect(host = "localhost", user = "root", password = "", database = "mad_uas_db_2024_202153019")
cursor = koneksi_db.cursor()

# SnackBar untuk operasi berhasil dan gagal
snack_bar_berhasil = SnackBar( Text("Operasi berhasil"), bgcolor = "green")
snack_bar_gagal = SnackBar( Text("Operasi gagal"), bgcolor = "red")

# Mengambil data profil pengguna berdasarkan username
def ambil_user_data(username):
    cursor.execute("SELECT username, password FROM user WHERE username = %s", (username,))
    data_akun_user = cursor.fetchone()
    return data_akun_user  # Mengembalikan tuple (username, password)

# Memperbarui data profil pengguna ke database
def update_user_data(username, password_baru):
    # Query untuk memperbarui data pengguna
    query = "UPDATE user SET password = %s WHERE username = %s"
    cursor.execute(query, (password_baru, username))
    koneksi_db.commit()  # Menyimpan perubahan ke database

# Formulir Profil dengan mengambil data dari database berdasarkan session username
def form_profil():
    # Mendapatkan session pengguna
    user = get_session()
    username = user['username'] if 'username' in user else None
    
    # Jika tidak ada username pada session, tampilkan pesan error atau navigasi kembali ke halaman login
    if not username:
        return Text("User not logged in.")

    print(username)

    # Mengambil data profil dari database
    user_data = ambil_user_data(username)
    
    if user_data:
        username_db, password_db = user_data
    else:
        username_db, password_db = "", ""  # Jika tidak ada data pengguna

    # Set nilai untuk inputan_password dengan data dari database
    inputan_username = TextField(label = "Username", value = username_db, read_only = True)
    inputan_password = TextField(label = "Password", value = password_db, password = True)
    
    # Fungsi untuk menangani penyimpanan profil
    def simpan_profil(e):
        # Mendapatkan nilai dari TextField
        password_baru = inputan_password.value
        
        # Memperbarui data pengguna di database
        try:
            update_user_data(username, password_baru)
            snack_bar_berhasil.open = True  # Menampilkan SnackBar sukses
            snack_bar_berhasil.update()
            print("Profil disimpan")
        except Exception as ex:
            snack_bar_gagal.open = True  # Menampilkan SnackBar gagal
            snack_bar_gagal.update()
            print(f"Error saving profile: {ex}")

    return Container(  # Membungkus seluruh Column dalam sebuah Container
        content = Column([
            # Judul dengan ikon pengguna
            Row([ 
                Icon(name = icons.PERSON, size = 50, color = colors.BLUE_400),
                Text("Profil Pengguna", size = 30, weight = "bold")
            ]),

            # Formulir untuk informasi profil pengguna
            Container(  # Membungkus seluruh Column dalam sebuah Container
                content = Column([
                    # Memusatkan Ikon dengan Row
                    Row([ 
                        Icon(name = icons.PERSON_PIN_CIRCLE_ROUNDED, size = 125, color = colors.GREY_500)
                    ], width = 350, alignment=MainAxisAlignment.CENTER),  # Memusatkan ikon dalam Row

                    Text("Username"),
                    inputan_username,

                    Text("Password"),
                    inputan_password,

                    ElevatedButton("Simpan Profil", on_click = simpan_profil)
                ], spacing = 10),
                # Menambahkan border pada Container yang membungkus seluruh Column
                border_radius = 20, 
                border = border.all(color=colors.GREY_900, width = 0.5), # Border hitam di sekeliling seluruh Column
                padding = 20,  # Memberikan padding di dalam container
            ),
        ], alignment = MainAxisAlignment.CENTER),  # Centering all content

        width = 350,
        margin = 10    # Memberikan jarak di luar container
    )
