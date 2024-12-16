import streamlit as st
from database import save_smartphone_data, get_smartphone_data, update_data, get_all_data, delete_data, save_bobot_data, get_bobot_data
from streamlit_option_menu import option_menu
import numpy as np
import pandas as pd

# Function to convert value to ranking according to a dictionary
def convert_to_ranking(value, ranking_dict):
    if isinstance(value, str):  # Check if the value is a string
        return ranking_dict.get(value, None)
    elif isinstance(value, int):  # Check if the value is an integer
        return value
    else:
        return None

# Placeholder function for TOPSIS calculation
def calculate_topsis(df):
    # Code to calculate TOPSIS should be added here
    pass

# Define ranking dictionaries
ranking_dict = {
    'kapasitas_baterai': {'<3000 mAh': 1, '3000-4000 mAh': 2, '4000-5000 mAh': 3, '>5000 mAh': 4},
    'ram': {'6 GB': 1 , '8 GB': 2, '12 GB': 3, '16 GB': 4},
    'kualitas_kamera': {'8 MP': 1, '12 MP': 2, '16 MP': 3, '32 MP': 4},
    'harga': {'<2 juta': 4, '2-4 juta': 3, '4-6 juta': 2, '>6 juta': 1},
    'rating_pengguna': {'Rendah': 1, 'Menengah': 2, 'Tinggi': 3}
}

# Sidebar menu
with st.sidebar:
    menu = option_menu(
        menu_title = "Menu",
        options = ["Home", "Create", "Read", "Update", "Delete", "Ranking"],
        icons = ["house", "plus", "list", "pencil", "trash", "bar-chart"],
        menu_icon = "heart-eyes-fill",
        default_index = 0,
    )

if menu == 'Home':
    st.title('SMARTSIS')
    st.write("Aplikasi untuk memilih smartphone terbaik berdasarkan berbagai kriteria menggunakan metode TOPSIS.")

elif menu == 'Create':
    st.title('Tambah Data Smartphone')

    # Input fields for smartphone criteria
    nama_smartphone = st.text_input('Nama Smartphone', '')
    kapasitas_baterai = st.radio('Kapasitas Baterai', ['<3000 mAh', '3000-4000 mAh', '4000-5000 mAh', '>5000 mAh'])
    ram = st.radio('ram', ['6 GB', '8 GB', '12 GB', '16 GB'])
    kualitas_kamera = st.radio('Kualitas Kamera', ['8 MP', '12 MP', '16 MP', '32 MP'])
    harga = st.radio('Harga', ['<2 juta', '2-4 juta', '4-6 juta', '>6 juta'])
    rating_pengguna = st.radio('Rating Pengguna', ['Rendah', 'Menengah', 'Tinggi'])

    if st.button('Submit'):
        # Convert values to ranking based on criteria
        kapasitas_baterai_rank = convert_to_ranking(kapasitas_baterai, ranking_dict['kapasitas_baterai'])
        ram_rank = convert_to_ranking(ram, ranking_dict['ram'])
        kualitas_kamera_rank = convert_to_ranking(kualitas_kamera, ranking_dict['kualitas_kamera'])
        harga_rank = convert_to_ranking(harga, ranking_dict['harga'])
        rating_pengguna_rank = convert_to_ranking(rating_pengguna, ranking_dict['rating_pengguna'])

        # Save data to database
        save_smartphone_data(nama_smartphone, kapasitas_baterai_rank, ram_rank, kualitas_kamera_rank, harga_rank, rating_pengguna_rank)
        st.success('Data smartphone berhasil disimpan.')

elif menu == 'Read':  
    st.title('Lihat Data Smartphone')

    # Fetch data from database
    data = get_smartphone_data()

    # Check if data has expected columns
    try:
        # Convert tuples to lists and pad data if columns are missing
        data = [list(row) + [None] * (6 - len(row)) if len(row) < 6 else list(row) for row in data]

        # Convert data to pandas DataFrame without 'id' column from the database
        df = pd.DataFrame(data, columns=['nama_smartphone', 'kapasitas_baterai', 'ram', 'kualitas_kamera', 'harga', 'rating_pengguna'])

        # Add auto-increment column for 'id'
        df.insert(0, 'id', range(1, len(df) + 1))

        # Display the DataFrame in Streamlit
        st.table(df)

    except ValueError as e:
        st.error("Data tidak memiliki jumlah kolom yang sesuai. Error: " + str(e))

elif menu == 'Update':
    st.title('Perbarui Data Smartphone')

    # Get all smartphone names from the database
    all_smartphones = [row[1] for row in get_all_data()]  # assuming id is in position [0] and name in [1]

    # Dropdown for selecting smartphone name
    selected_smartphone = st.selectbox('Pilih Smartphone', all_smartphones)

    # Input fields for updating criteria
    kapasitas_baterai = st.radio('Kapasitas Baterai', ['<3000 mAh', '3000-4000 mAh', '4000-5000 mAh', '>5000 mAh'])
    ram = st.radio('ram', ['6 GB', '8 GB', '12 GB', '16 GB'])
    kualitas_kamera = st.radio('Kualitas Kamera', ['8 MP', '12 MP', '16 MP', '32 MP'])
    harga = st.radio('Harga', ['<2 juta', '2-4 juta', '4-6 juta', '>6 juta'])
    rating_pengguna = st.radio('Rating Pengguna', ['Rendah', 'Menengah', 'Tinggi'])

    if st.button('Update'):
        # Convert values to ranking
        kapasitas_baterai_rank = convert_to_ranking(kapasitas_baterai, ranking_dict['kapasitas_baterai'])
        performa_rank = convert_to_ranking(ram, ranking_dict['ram'])
        kualitas_kamera_rank = convert_to_ranking(kualitas_kamera, ranking_dict['kualitas_kamera'])
        harga_rank = convert_to_ranking(harga, ranking_dict['harga'])
        rating_pengguna_rank = convert_to_ranking(rating_pengguna, ranking_dict['rating_pengguna'])

        # Update data in the database
        update_data(selected_smartphone, kapasitas_baterai_rank, performa_rank, kualitas_kamera_rank, harga_rank, rating_pengguna_rank)
        st.success('Data smartphone berhasil diperbarui.')

elif menu == 'Delete':
    st.title('Hapus Data Smartphone')

    # Ambil data dari database
    data = get_smartphone_data()

    try:
        # Konversi tuple ke list dan tambahkan kolom jika ada yang hilang
        data = [list(row) + [None] * (6 - len(row)) if len(row) < 6 else list(row) for row in data]

        # Konversi data ke DataFrame dengan nama kolom yang ditentukan
        df = pd.DataFrame(data, columns=['nama_smartphone', 'kapasitas_baterai', 'ram', 'kualitas_kamera', 'harga', 'rating_pengguna'])

        st.write(df)

        # Get all smartphone names from the database
        all_smartphones = [row[1] for row in get_all_data()]  # assuming id is in position [0] and name in [1]

        index_to_delete = st.selectbox('Select row to delete', all_smartphones)

        if st.button('Hapus'):
            # data = data.drop(index_to_delete)
            delete_data(index_to_delete)  # Fungsi untuk menghapus data
            st.success(f"Data smartphone '{index_to_delete}' berhasil dihapus.")
            # Tambahkan pesan untuk refresh halaman secara manual
            st.write("Silakan refresh halaman untuk melihat perubahan.")

    except ValueError as e:
        st.error("Data tidak memiliki jumlah kolom yang sesuai. Error: " + str(e))

elif menu == 'Ranking': 
    st.title('Peringkat Smartphone Terbaik')

    # Fetch all data from database
    all_data = get_all_data()

    # Check if data has expected columns
    if all_data and len(all_data[0]) == 7:
        # Convert data to pandas DataFrame dengan nama kolom yang benar
        df = pd.DataFrame(all_data, columns=['id', 'nama_smartphone', 'kapasitas_baterai', 'ram', 'kualitas_kamera', 'harga', 'rating_pengguna'])
        
        # Simpan kolom 'id' di tempat terpisah
        ids = df['id'].copy()  # Simpan id di variabel terpisah
        df_without_id = df.drop(columns=['id'])  # DataFrame tanpa kolom 'id'

        # Tampilkan DataFrame untuk debugging
        st.subheader("Data Awal")
        st.write(df_without_id)

        # Konversi kolom yang relevan ke tipe data numerik
        numeric_columns = ['kapasitas_baterai', 'ram', 'kualitas_kamera', 'harga', 'rating_pengguna']
        for column in numeric_columns:
            df_without_id[column] = pd.to_numeric(df_without_id[column], errors='coerce')

        # Cek apakah ada nilai NaN setelah konversi
        if df_without_id[numeric_columns].isnull().values.any():
            st.warning("Beberapa nilai numerik tidak valid dan akan diisi dengan rata-rata kolom.")
            df_without_id[numeric_columns] = df_without_id[numeric_columns].fillna(df_without_id[numeric_columns].mean())

        # Definisikan bobot untuk setiap kriteria (pastikan jumlah bobot = 1)
        weights = [0.2, 0.25, 0.2, 0.15, 0.2]  # Sesuaikan sesuai kebutuhan Anda
        
        # Definisikan kriteria benefit dan cost
        benefit_criteria = ['kapasitas_baterai', 'ram', 'kualitas_kamera', 'rating_pengguna']  # Kriteria yang ingin dimaksimalkan
        
        # Normalisasi matriks keputusan
        normalized_df = df_without_id.copy()
        for column in numeric_columns:
            norm_factor = (df_without_id[column] ** 2).sum() ** 0.5
            normalized_df[column] = df_without_id[column] / norm_factor
        
        # Tampilkan DataFrame setelah normalisasi
        st.subheader("Data Setelah Normalisasi")
        st.write(normalized_df)
        
        # Kalikan matriks normalisasi dengan bobot
        weighted_df = normalized_df.copy()
        for i, column in enumerate(numeric_columns):
            weighted_df[column] = normalized_df[column] * weights[i]
        
        # Tampilkan DataFrame setelah pembobotan
        st.subheader("Data Setelah Pembobotan")
        st.write(weighted_df)
        
        st.subheader('Menghitung solusi ideal positif dan negatif')
        
        # Menghitung Solusi Ideal Positif (A+)
        a_plus = weighted_df.max(numeric_only=True)

        # Menghitung Solusi Ideal Negatif (A-)
        a_minus = weighted_df.min(numeric_only=True)
        
        # Membuat DataFrame baru untuk Solusi Ideal Positif (A+) dan Solusi Ideal Negatif (A-)
        ideal_solutions = pd.DataFrame({
            'A+ (Max)': a_plus,
            'A- (Min)': a_minus
        })

        # Menampilkan DataFrame
        st.write(ideal_solutions)
        
        # Menghitung jarak antara nilai terbobot setiap alternatif dengan A+
        weighted_df['D+'] = np.sqrt(((weighted_df[numeric_columns] - a_plus) ** 2).sum(axis=1))

        # Menghitung jarak antara nilai terbobot setiap alternatif dengan A-
        weighted_df['D-'] = np.sqrt(((weighted_df[numeric_columns] - a_minus) ** 2).sum(axis=1))
        
        # Hitung kedekatan relatif terhadap solusi ideal (V)
        weighted_df['V'] = weighted_df['D-'] / (weighted_df['D+'] + weighted_df['D-'])

        # Tampilkan hasil jarak dan kedekatan relatif
        st.subheader("Jarak ke Solusi Ideal Positif (D+) dan Negatif (D-) serta Kedekatan Relatif (V)")
        st.write(weighted_df[['nama_smartphone', 'kapasitas_baterai', 'ram', 'kualitas_kamera', 'harga', 'rating_pengguna', 'D+', 'D-', 'V']])

        st.subheader("Peringkat Smartphone Berdasarkan TOPSIS")

        # Tombol untuk menghitung dan menyimpan skor
        if st.button('Hitung Skor Terbaru'):
            # Gabungkan kembali kolom 'id' sebelum menyimpan ke database
            weighted_df['id'] = ids

            # Urutkan berdasarkan skor TOPSIS secara menurun
            ranked_df = weighted_df[['id', 'nama_smartphone', 'V']].sort_values(by='V', ascending=False).reset_index(drop=True)
            ranked_df['ranking'] = range(1, len(ranked_df) + 1)

            # Simpan hasil ke database menggunakan save_bobot_data
            for index, row in ranked_df.iterrows():
                save_bobot_data(row['id'], row['V'])

            st.success("Skor berhasil dihitung dan disimpan ke database!")

        # Ambil data bobot dari database
        ranked_results = get_bobot_data()

        # Konversi hasil query ke DataFrame
        ranked_df = pd.DataFrame(ranked_results, columns=['id', 'smartphone_id', 'nilai_bobot'])

        # Tambahkan relasi ke tabel `smartphone`
        ranked_df = ranked_df.merge(df[['id', 'nama_smartphone']], left_on='smartphone_id', right_on='id', how='left')

        # Pilih kolom yang akan ditampilkan
        ranked_df = ranked_df[['nama_smartphone', 'nilai_bobot']].rename(columns={'nilai_bobot': 'topsis_score'})

        # Urutkan berdasarkan skor TOPSIS secara menurun
        ranked_df = ranked_df.sort_values(by='topsis_score', ascending=False)

        # Tambahkan kolom ranking berdasarkan urutan skor TOPSIS
        ranked_df['ranking'] = ranked_df['topsis_score'].rank(ascending=False, method='dense').astype(int)

        # Tampilkan tabel hasil
        st.write(ranked_df)

    else:
        st.error("Data tidak memiliki jumlah kolom yang sesuai.")


