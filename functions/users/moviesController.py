import csv
import sys
import textwrap
from functions.helper import bersihkan_layar, garis
from functions.users.reviewsController import beri_rating_komentar
from functions.users.wishlistController import tambah_wishlist

FILE_FILM = 'databases/movies.csv'
FILE_KOMEN = 'databases/reviews.csv'

# ---------- Akses Data ----------
def ambil_semua_film():
    try:
        with open(FILE_FILM, mode='r', encoding='utf-8') as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        print(f"[-] File {FILE_FILM} tidak ditemukan!")
        return []

def ambil_data_ulasan(id_target):
    try:
        with open(FILE_KOMEN, mode='r', encoding='utf-8') as file:
            semua_komen = list(csv.DictReader(file))

        ulasan_film = [
            row for row in semua_komen 
            if row.get('id_film', '').strip().upper() == id_target.upper()
        ]

        if not ulasan_film:
            return "Belum ada rating", []

        skor = []
        for u in ulasan_film:
            try:
                skor.append(float(u['rating']))
            except (ValueError, KeyError):
                pass

        if not skor:
            info_rating = "Belum ada rating"
        else:
            rata_rata = sum(skor) / len(skor)
            info_rating = f"{rata_rata:.1f} / 5.0 ({len(skor)} ulasan)"

        return info_rating, ulasan_film
    except FileNotFoundError:
        # Aman jika file reviews.csv belum dibuat
        return "Belum ada rating", []

def cari_film_sejenis(film_aktif, semua_film, batas=3):
    genre_aktif = [g.strip().lower() for g in film_aktif['genre'].split(',')]
    rekomendasi = []

    for film in semua_film:
        if film['id_film'] == film_aktif['id_film']:
            continue

        for g in film['genre'].split(','):
            if g.strip().lower() in genre_aktif:
                rekomendasi.append(film)
                break

        if len(rekomendasi) == batas:
            break

    return rekomendasi

# ---------- Tampilan Katalog & Detail ----------
def list_film(sesi_user):
    data_film = ambil_semua_film()
    
    while True:
        bersihkan_layar()
        garis(88)
        print("                                   KATALOG LIST FILM")
        garis(88)

        if not data_film:
            print("Belum ada film di database.")
            input("\nTekan Enter untuk kembali...")
            return

        print(f"{'ID':<6} | {'JUDUL FILM':<38} | {'TAHUN':<5} | {'GENRE'}")
        print("-" * 88)

        for film in data_film:
            judul = film['judul']
            if len(judul) > 38:
                judul = judul[:35] + "..."
            print(f"{film['id_film']:<6} | {judul:<38} | {film['tahun']:<5} | {film['genre']}")

        garis(88)
        print("Ketik ID Film (contoh: M001) untuk lihat detail")
        print("Ketik 'S' untuk urutkan film | '0' untuk kembali | 'e' keluar aplikasi")
        pilihan = input("Pilihan Anda: ").strip().upper()

        if pilihan == '0' or pilihan == '':
            break
        elif pilihan == 'E':
            print("\nMenutup aplikasi... Sampai jumpa lagi, bro!")
            sys.exit()
        elif pilihan == 'S':
            print("\nUrutkan berdasarkan: [1] Judul A-Z  [2] Tahun Terbaru  [3] Reset")
            urut = input("Pilih: ").strip()
            if urut == '1':
                data_film = sorted(data_film, key=lambda f: f['judul'].lower())
            elif urut == '2':
                data_film = sorted(data_film, key=lambda f: int(f['tahun']) if f['tahun'].isdigit() else 0, reverse=True)
            elif urut == '3':
                data_film = ambil_semua_film()
        else:
            detail_film(sesi_user, pilihan)

def detail_film(sesi_user, id_target=None):
    data_film = ambil_semua_film()

    if not data_film:
        bersihkan_layar()
        print("Belum ada film di database.")
        input("\nTekan Enter untuk kembali...")
        return

    if id_target is None:
        bersihkan_layar()
        print("=== CARI DETAIL FILM ===")
        id_target = input("Masukkan ID Film (contoh: M001): ").strip().upper()

    film_ketemu = next((f for f in data_film if f['id_film'].strip().upper() == id_target), None)

    if film_ketemu is None:
        bersihkan_layar()
        print(f"[-] Film dengan ID '{id_target}' tidak ditemukan.")
        input("\nTekan Enter untuk kembali...")
        return

    while True:
        bersihkan_layar()
        info_rating, ulasan_film = ambil_data_ulasan(film_ketemu['id_film'])
        rekomendasi = cari_film_sejenis(film_ketemu, data_film)

        garis(78)
        print(f"  {film_ketemu['judul'].upper()} ({film_ketemu['tahun']})")
        garis(78)
        print(f"  ID Film   : {film_ketemu['id_film']}")
        print(f"  Rating    : {info_rating}")
        print(f"  Sutradara : {film_ketemu['sutradara']}")
        print(f"  Genre     : {film_ketemu['genre']}")
        print(f"  Durasi    : {film_ketemu['durasi']} menit")
        print("-" * 78)

        prefix = "  Sinopsis  : "
        sinopsis_rapi = textwrap.fill(
            film_ketemu['sinopsis'],
            width=76,
            initial_indent=prefix,
            subsequent_indent=" " * len(prefix)
        )
        print(sinopsis_rapi)

        print("-" * 78)
        print("  REKOMENDASI FILM SEJENIS:")
        if rekomendasi:
            for rek in rekomendasi:
                print(f"  - [{rek['id_film']}] {rek['judul']} ({rek['tahun']}) | {rek['genre']}")
        else:
            print("  - Belum ada rekomendasi film dengan genre serupa.")

        print("-" * 78)
        print("  ULASAN PENONTON TERBARU:")
        if ulasan_film:
            for u in ulasan_film[-3:]:
                komen_teks = u.get('komentar', '').strip()
                if komen_teks:
                    print(f"  - @{u.get('username', 'anonim')} ({u.get('rating', '-')}/5): {komen_teks}")
                else:
                    print(f"  - @{u.get('username', 'anonim')} memberi rating {u.get('rating', '-')}/5")
        else:
            print("  - Belum ada ulasan untuk film ini.")
        garis(78)

        print("\nOpsi Aksi:")
        print("  [1] Tambah / Ubah Rating & Komentar")
        print("  [2] Tambah ke Wishlist")
        print("  [0] Kembali")
        print("  [e] Keluar Aplikasi")

        aksi = input("\nPilih aksi: ").strip().lower()
        if aksi == '1':
            beri_rating_komentar(sesi_user, film_ketemu['id_film'])
            input("Tekan Enter untuk lanjut...")
        elif aksi == '2':
            tambah_wishlist(sesi_user['id'], film_ketemu['id_film'])
            print(f"\n[+] Film berhasil ditambahkan ke wishlist oleh @{sesi_user['username']}.")
            input("Tekan Enter untuk lanjut...")
        elif aksi == '0' or aksi == '':
            break
        elif aksi == 'e':
            print("\nMenutup aplikasi... Sampai jumpa lagi, bro!")
            sys.exit()

def cari_film(sesi_user):
    bersihkan_layar()
    data_film = ambil_semua_film()

    garis(88)
    print("                                     PENCARIAN FILM")
    garis(88)

    if not data_film:
        print("Belum ada film di database.")
        input("\nTekan Enter untuk kembali...")
        return

    kata_kunci = input("Masukkan kata kunci (Judul / Genre / Sutradara): ").strip().lower()

    if not kata_kunci:
        print("[-] Kata kunci pencarian tidak boleh kosong!")
        input("\nTekan Enter untuk kembali...")
        return

    hasil = [
        film for film in data_film
        if kata_kunci in film['judul'].lower()
        or kata_kunci in film['genre'].lower()
        or kata_kunci in film['sutradara'].lower()
    ]

    print("\n" + "=" * 88)
    print(f"Hasil pencarian untuk '{kata_kunci}' ({len(hasil)} film ditemukan):")
    garis(88)

    if not hasil:
        print("[-] Tidak ada film yang cocok dengan kata kunci tersebut.")
        input("\nTekan Enter untuk kembali...")
        return

    print(f"{'NO':<4} | {'JUDUL FILM':<40} | {'TAHUN':<5} | {'GENRE'}")
    print("-" * 88)

    for nomor, film in enumerate(hasil, start=1):
        judul = film['judul']
        if len(judul) > 40:
            judul = judul[:37] + "..."
        print(f"{nomor:<4} | {judul:<40} | {film['tahun']:<5} | {film['genre']}")

    garis(88)
    pilihan = input("Pilih NOMOR film untuk lihat detail (atau Enter untuk kembali): ").strip()

    if pilihan == "":
        return
    elif pilihan.isdigit() and 1 <= int(pilihan) <= len(hasil):
        film_terpilih = hasil[int(pilihan) - 1]
        detail_film(sesi_user, film_terpilih['id_film'])
    else:
        print(f"[-] Pilihan tidak valid! Masukkan angka 1 sampai {len(hasil)}.")
        input("\nTekan Enter untuk kembali...")

# ---------- Sub-Menu Katalog User ----------
def menu_katalog_user(sesi_user):
    while True:
        bersihkan_layar()
        garis(50)
        print("JELAJAHI & DETAIL FILM")
        garis(50)
        print("1. List Semua Film")
        print("2. Cari Film (Judul / Genre / Sutradara)")
        print("3. Buka Detail Film Langsung (via ID)")
        print("0. Kembali ke Dashboard User")
        print("e. Keluar Aplikasi")

        pilih = input("\nPilih menu: ").strip().lower()
        if pilih == '1':
            list_film(sesi_user)
        elif pilih == '2':
            cari_film(sesi_user)
        elif pilih == '3':
            detail_film(sesi_user)
        elif pilih == '0':
            break
        elif pilih == 'e':
            print("\nMenutup aplikasi... Sampai jumpa lagi, bro!")
            sys.exit()
        else:
            print("Pilihan tidak valid!")
            input("Tekan Enter untuk lanjut...")