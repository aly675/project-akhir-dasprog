import csv
import os
import sys
import textwrap
from functions.helper import bersihkan_layar, garis

FILE_FILM = 'databases/movies.csv'
HEADER_FILM = ['id_film', 'judul', 'sinopsis', 'tahun', 'sutradara', 'genre', 'durasi']

# ---------- Generate ID Film ----------
def generate_id_film(data_film):
    """Otomatis generate ID dengan format M001, M002, dst."""
    if not data_film:
        return "M001"
    
    # Ambil semua angka di belakang huruf 'M', cari yang paling besar, lalu + 1
    angka_terakhir = max(
        (int(f['id_film'][1:]) for f in data_film if f['id_film'].upper().startswith('M') and f['id_film'][1:].isdigit()),
        default=0
    )
    return f"M{angka_terakhir + 1:03d}"

# ---------- Akses File ----------
def load_movies():
    """Membaca semua data film dari CSV -> list of dict."""
    if not os.path.exists(FILE_FILM):
        os.makedirs(os.path.dirname(FILE_FILM), exist_ok=True)
        with open(FILE_FILM, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=HEADER_FILM)
            writer.writeheader()
        return []
    with open(FILE_FILM, mode='r', encoding='utf-8') as file:
        return list(csv.DictReader(file))

def save_movies(data_film):
    """Menyimpan ulang seluruh list data film ke CSV."""
    with open(FILE_FILM, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=HEADER_FILM, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(data_film)

# ---------- Tampilan ----------
def tampilkan_daftar_film(data_film):
    """Fungsi tampilan terpisah agar bisa dipakai ulang di Read, Search, Sort, Edit, Delete."""
    if not data_film:
        print("Data film tidak ditemukan / masih kosong.")
        return

    garis()
    for film in data_film:
        print(f"[{film['id_film']}] {film['judul']} ({film['tahun']}) - Genre: {film['genre']}")
        print(f"       Sutradara : {film['sutradara']} | Durasi: {film['durasi']} menit")
        
        prefix = "       Sinopsis  : "
        sinopsis_rapi = textwrap.fill(
            film['sinopsis'],
            width=75,
            initial_indent=prefix,
            subsequent_indent=" " * len(prefix)
        )
        print(f"{sinopsis_rapi}\n")
    garis()
    print(f"Total: {len(data_film)} film")

# ---------- 1. READ (Lihat Semua) ----------
def lihat_film(data_film):
    bersihkan_layar()
    print("=== DAFTAR SEMUA FILM ===".center(75))
    tampilkan_daftar_film(data_film)

# ---------- 2. SEARCHING ----------
def cari_film(data_film):
    bersihkan_layar()
    print("=== CARI FILM ===")
    kata_kunci = input("Masukkan kata kunci (Judul / Genre / Sutradara): ").strip().lower()
    
    hasil = [
        f for f in data_film 
        if kata_kunci in f['judul'].lower() 
        or kata_kunci in f['genre'].lower() 
        or kata_kunci in f['sutradara'].lower()
    ]
    print(f"\nHasil pencarian untuk '{kata_kunci}':")
    tampilkan_daftar_film(hasil)

# ---------- 3. SORTING ----------
def urutkan_film(data_film):
    bersihkan_layar()
    print("=== URUTKAN FILM ===")
    print("1. Judul (A - Z)")
    print("2. Judul (Z - A)")
    print("3. Tahun Rilis (Terbaru)")
    print("4. Tahun Rilis (Terlama)")
    print("5. Durasi (Terlama)")
    pilih = input("Pilih metode urut: ").strip()

    if pilih == '1':
        hasil = sorted(data_film, key=lambda f: f['judul'].lower())
    elif pilih == '2':
        hasil = sorted(data_film, key=lambda f: f['judul'].lower(), reverse=True)
    elif pilih == '3':
        hasil = sorted(data_film, key=lambda f: int(f['tahun']) if f['tahun'].isdigit() else 0, reverse=True)
    elif pilih == '4':
        hasil = sorted(data_film, key=lambda f: int(f['tahun']) if f['tahun'].isdigit() else 0)
    elif pilih == '5':
        hasil = sorted(data_film, key=lambda f: int(f['durasi']) if f['durasi'].isdigit() else 0, reverse=True)
    else:
        print("Pilihan tidak valid.")
        return

    tampilkan_daftar_film(hasil)

# ---------- 4. CREATE (Tambah Film) ----------
def tambah_film(data_film):
    bersihkan_layar()
    print("=== TAMBAH FILM BARU ===")
    
    id_film = generate_id_film(data_film)
    print(f"ID Film (Otomatis)     : {id_film}")

    judul = input("Judul Film             : ").strip().title()
    sinopsis = input("Sinopsis singkat       : ").strip()
    tahun = input("Tahun Rilis            : ").strip()
    sutradara = input("Sutradara / Author     : ").strip().title()
    genre = input("Genre                  : ").strip().title()
    durasi = input("Durasi (menit)         : ").strip()

    if not judul or not tahun.isdigit() or not durasi.isdigit():
        print("[-] Gagal: Judul wajib diisi, Tahun & Durasi harus berupa angka!")
        return

    film_baru = {
        'id_film': id_film,
        'judul': judul,
        'sinopsis': sinopsis,
        'tahun': tahun,
        'sutradara': sutradara,
        'genre': genre,
        'durasi': durasi
    }
    
    data_film.append(film_baru)
    save_movies(data_film)
    print(f"\n[+] Film '{judul}' ({id_film}) berhasil ditambahkan!")

# ---------- 5. UPDATE (Edit Film) ----------
def edit_film(data_film):
    bersihkan_layar()
    print("=== EDIT DATA FILM ===".center(75))
    tampilkan_daftar_film(data_film)
    if not data_film:
        return
    
    id_target = input("\nMasukkan ID Film yang mau diedit: ").strip().upper()
    
    ditemukan = False
    for film in data_film:
        if film['id_film'].upper() == id_target:
            ditemukan = True
            print(f"\nEdit data untuk: {film['judul']} (Kosongkan jika tidak diubah)")
            
            film['judul'] = input(f"Judul baru [{film['judul']}]: ").strip().title() or film['judul']
            film['sinopsis'] = input(f"Sinopsis baru [{film['sinopsis']}]: ").strip() or film['sinopsis']
            
            tahun_baru = input(f"Tahun baru [{film['tahun']}]: ").strip()
            if tahun_baru:
                if not tahun_baru.isdigit():
                    print("[-] Gagal: Tahun harus berupa angka!")
                    return
                film['tahun'] = tahun_baru

            film['sutradara'] = input(f"Sutradara baru [{film['sutradara']}]: ").strip().title() or film['sutradara']
            film['genre'] = input(f"Genre baru [{film['genre']}]: ").strip().title() or film['genre']
            
            durasi_baru = input(f"Durasi baru [{film['durasi']}]: ").strip()
            if durasi_baru:
                if not durasi_baru.isdigit():
                    print("[-] Gagal: Durasi harus berupa angka!")
                    return
                film['durasi'] = durasi_baru

            save_movies(data_film)
            print("\n[+] Data film berhasil diperbarui!")
            break
            
    if not ditemukan:
        print("[-] ID Film tidak ditemukan.")

# ---------- 6. DELETE (Hapus Film) ----------
def hapus_film(data_film):
    bersihkan_layar()
    print("=== HAPUS FILM ===".center(75))
    tampilkan_daftar_film(data_film)
    if not data_film:
        return
    
    id_target = input("\nMasukkan ID Film yang mau dihapus: ").strip().upper()
    
    target_film = None
    for film in data_film:
        if film['id_film'].upper() == id_target:
            target_film = film
            break

    if not target_film:
        print("[-] ID Film tidak ditemukan.")
        return

    konfirmasi = input(f"Yakin ingin menghapus film '{target_film['judul']}'? (y/n): ").strip().lower()
    if konfirmasi == 'y':
        data_film.remove(target_film)
        save_movies(data_film)
        print(f"\n[+] Film '{target_film['judul']}' berhasil dihapus!")
    else:
        print("\nPenghapusan dibatalkan.")

# ---------- MENU UTAMA KELOLA FILM ----------
def menu_admin_movies():
    """Menu utama CRUD Film yang dipanggil dari functions/admin/index.py"""
    while True:
        data_film = load_movies()
        bersihkan_layar()
        garis()
        print("KELOLA DATA FILM (CRUD MOVIES)")
        garis()
        print("1. Lihat semua film")
        print("2. Cari film")
        print("3. Urutkan film")
        print("4. Tambah film")
        print("5. Ubah film")
        print("6. Hapus film")
        print("0. Kembali ke Dashboard Admin")
        print("e. Keluar Aplikasi")
        
        pilih = input("Pilih menu: ").strip().lower()
        
        if pilih == '1':
            lihat_film(data_film)
        elif pilih == '2':
            cari_film(data_film)
        elif pilih == '3':
            urutkan_film(data_film)
        elif pilih == '4':
            tambah_film(data_film)
        elif pilih == '5':
            edit_film(data_film)
        elif pilih == '6':
            hapus_film(data_film)
        elif pilih == '0':
            break
        elif pilih == 'e':
            print("\nMenutup aplikasi... Sampai jumpa lagi!")
            sys.exit()
        else:
            print("Pilihan tidak valid.")
        input("\nTekan Enter untuk lanjut...")