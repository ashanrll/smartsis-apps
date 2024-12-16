import mysql.connector

# Pilih mode koneksi: 'lokal' atau 'online'
mode_koneksi = 'lokal'  # Ubah menjadi 'online' jika menggunakan database online

try:
    if mode_koneksi == 'lokal':
        # Koneksi ke database lokal (XAMPP)
        cnx = mysql.connector.connect(
            user='root', 
            password='', 
            host='localhost', 
            database='spk'
        )
        print("Koneksi berhasil ke database lokal (XAMPP).")
    elif mode_koneksi == 'online':
        # Koneksi ke database online
        cnx = mysql.connector.connect(
            user='your-username', 
            password='your-password', 
            host='your-database-host.com',  # Hostname database online
            database='spk'
        )
        print("Koneksi berhasil ke database online.")
    else:
        print("Mode koneksi tidak valid. Pilih 'lokal' atau 'online'.")
    
    # Tutup koneksi setelah sukses
    cnx.close()
except mysql.connector.Error as err:
    print(f"Error: {err}")
