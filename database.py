import mysql.connector

# Fungsi untuk menyimpan data ke tabel 'smartphone'
def save_smartphone_data(nama_smartphone, kapasitas_baterai, ram, kualitas_kamera, harga, rating_pengguna):
    cnx = mysql.connector.connect(user='root', password='', host='localhost', database='spk')
    cursor = cnx.cursor()
    query = ("INSERT INTO smartphone "
             "(nama_smartphone, kapasitas_baterai, ram, kualitas_kamera, harga, rating_pengguna) "
             "VALUES (%s, %s, %s, %s, %s, %s)")
    cursor.execute(query, (nama_smartphone, kapasitas_baterai, ram, kualitas_kamera, harga, rating_pengguna))
    cnx.commit()
    cursor.close()
    cnx.close()

# Fungsi untuk mengambil semua data dari tabel 'smartphone'
def get_smartphone_data():
    cnx = mysql.connector.connect(user='root', password='', host='localhost', database='spk')
    cursor = cnx.cursor()
    query = "SELECT nama_smartphone, kapasitas_baterai, ram, kualitas_kamera, harga, rating_pengguna FROM smartphone"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    cnx.close()
    return rows

# Fungsi untuk menyimpan atau memperbarui data di tabel 'bobot'
def save_bobot_data(smartphone_id, nilai_bobot):
    cnx = mysql.connector.connect(user='root', password='', host='localhost', database='spk')
    cursor = cnx.cursor()

    # Periksa apakah smartphone_id sudah ada
    check_query = "SELECT COUNT(*) FROM bobot WHERE smartphone_id = %s"
    cursor.execute(check_query, (smartphone_id,))
    exists = cursor.fetchone()[0] > 0

    # Jika tidak ada, masukkan data baru
    if not exists:
        insert_query = """
        INSERT INTO bobot (smartphone_id, nilai_bobot)
        VALUES (%s, %s)
        """
        cursor.execute(insert_query, (smartphone_id, nilai_bobot))
        cnx.commit()

    cursor.close()
    cnx.close()


# Fungsi untuk mengambil semua data dari tabel 'bobot'
def get_bobot_data():
    cnx = mysql.connector.connect(user='root', password='', host='localhost', database='spk')
    cursor = cnx.cursor()
    query = "SELECT * FROM bobot"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    cnx.close()
    return rows

# Fungsi untuk memperbarui data pada tabel 'smartphone'
def update_data(nama_smartphone, kapasitas_baterai, ram, kualitas_kamera, harga, rating_pengguna):
    cnx = mysql.connector.connect(user='root', password='', host='localhost', database='spk')
    cursor = cnx.cursor()
    query = ("UPDATE smartphone SET kapasitas_baterai = %s, ram = %s, kualitas_kamera = %s, "
             "harga = %s, rating_pengguna = %s WHERE nama_smartphone = %s")
    cursor.execute(query, (kapasitas_baterai, ram, kualitas_kamera, harga, rating_pengguna, nama_smartphone))
    cnx.commit()
    cursor.close()
    cnx.close()

# Fungsi untuk mengambil semua nama smartphone dari tabel 'smartphone'
def get_all_smartphones():
    cnx = mysql.connector.connect(user='root', password='', host='localhost', database='spk')
    cursor = cnx.cursor()
    query = "SELECT nama_smartphone FROM smartphone"
    cursor.execute(query)
    rows = [row[0] for row in cursor.fetchall()]
    cursor.close()
    cnx.close()
    return rows

# Fungsi untuk menghapus data dari tabel 'smartphone' berdasarkan nama
def delete_data(nama_smartphone):
    cnx = mysql.connector.connect(user='root', password='', host='localhost', database='spk')
    cursor = cnx.cursor()
    query = "DELETE FROM smartphone WHERE nama_smartphone = %s"
    cursor.execute(query, (nama_smartphone,))
    cnx.commit()
    cursor.close()
    cnx.close()

# Fungsi untuk mengambil semua data dari tabel 'smartphone' (untuk ranking)
def get_all_data():
    cnx = mysql.connector.connect(user='root', password='', host='localhost', database='spk')
    cursor = cnx.cursor()
    query = "SELECT * FROM smartphone"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    cnx.close()
    return rows
