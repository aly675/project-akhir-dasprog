import csv
data1 = input("Masukkan ID film: ")
data2 = input("Masukkan judul film: ")
data3 = input("Masukkan tahun film: ")
data4 = input("Masukkan genre film: ")

# Data baru yang mau dimasukin bentuknya Dictionary
film_baru = {'id': data1, 'judul': data2, 'tahun': data3, 'genre': data4}

# Buka file dengan mode 'a' (append)
# with open('database/movies.csv', mode='a', encoding='utf-8', newline='') as file:
    # Tentukan nama kolom (header) biar penulisannya sejajar
kolom = [ 'judul', 'tahun', 'genre', 'id' ]
    
    # Siapkan alat penulis CSV
csv_writer = csv.DictWriter(open('database/movies.csv', mode='a', encoding='utf-8', newline=''), fieldnames=kolom)
    
    # Tulis data dictionary ke dalam baris baru (Create)
csv_writer.writerow(film_baru)

print("Data film berhasil ditambahkan, bro!")