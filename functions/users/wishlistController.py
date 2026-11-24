import csv
import os
import sys
from functions.helper import bersihkan_layar, garis, now

# ==========================================
# KONSTANTA GLOBAL
# ==========================================
FILE_FILM = 'databases/movies.csv'
FILE_WISHLIST = 'databases/wishlist.csv'
HEADER_WISHLIST = ['id', 'user_id', 'film_id', 'prioritas', 'status', 'created_at']

PRIORITAS = ("tinggi", "sedang", "rendah")
STATUS = ("belum", "sudah")
URUT_PRIORITAS = {"tinggi": 0, "sedang": 1, "rendah": 2}

# ---------- Akses File ----------
def load_films():
    """Baca semua film dari movies.csv -> list of dict."""
    if not os.path.exists(FILE_FILM):
        return []
    with open(FILE_FILM, "r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def load_wishlist():
    """Baca semua wishlist dari CSV. Buat file kosong jika belum ada."""
    if not os.path.exists(FILE_WISHLIST):
        os.makedirs(os.path.dirname(FILE_WISHLIST), exist_ok=True)
        save_wishlist([])
        return []
    with open(FILE_WISHLIST, "r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def save_wishlist(data):
    with open(FILE_WISHLIST, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADER_WISHLIST, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(data)

def next_id(data):
    return str(max((int(w["id"]) for w in data), default=0) + 1)

# ---------- Helper Lokal ----------
def judul_film(film):
    return film.get("judul") or "(tanpa judul)"

def find_film(films, film_id):
    for f in films:
        if f["id_film"].strip().upper() == film_id.strip().upper():
            return f
    return None

def wishlist_milik(wishlist, user_id):
    return [w for w in wishlist if w["user_id"] == str(user_id)]

def find_item(wishlist, user_id, item_id):
    """Cari item wishlist berdasarkan ID, hanya milik user yang login."""
    for w in wishlist:
        if w["id"] == item_id and w["user_id"] == str(user_id):
            return w
    return None

def sudah_ada(wishlist, user_id, film_id):
    for w in wishlist:
        if w["user_id"] == str(user_id) and w["film_id"].upper() == film_id.upper():
            return True
    return False

# ---------- Tampilan ----------
def tampilkan_film(films):
    if not films:
        print("Belum ada data film.")
        return
    garis(55)
    print(f"{'ID':<8}{'Judul':<47}")
    garis(55)
    for f in films:
        print(f"{f['id_film']:<8}{judul_film(f):<47}")
    garis(55)

def tampilkan_wishlist(data, films):
    if not data:
        print("Wishlist kosong / tidak ditemukan.")
        return
    garis(75)
    print(f"{'ID':<5}{'Judul':<30}{'Prioritas':<12}{'Status':<10}{'Ditambahkan':<20}")
    garis(75)
    for w in data:
        film = find_film(films, w["film_id"])
        judul = judul_film(film) if film else "(film dihapus)"
        if len(judul) > 28:
            judul = judul[:25] + "..."
        print(f"{w['id']:<5}{judul:<30}{w['prioritas']:<12}{w['status']:<10}{w['created_at']:<20}")
    garis(75)
    print(f"Total: {len(data)} film")

# ---------- CREATE ----------
def tambah_wishlist(user_id, film_id_target=None):
    bersihkan_layar()
    print("=== Tambah ke Wishlist ===".center(50))
    films = load_films()
    if not films:
        print("Belum ada film yang tersedia.")
        return

    wishlist = load_wishlist()

    # Jika dipanggil dari menu Wishlist tampilkan daftar film, jika dari Detail Film langsung pakai ID-nya
    if film_id_target is None:
        tampilkan_film(films)
        film_id = input("Masukkan ID film (contoh: M001): ").strip().upper()
    else:
        film_id = film_id_target.strip().upper()

    film_ketemu = find_film(films, film_id)
    if not film_ketemu:
        print(f"[-] Gagal: film dengan ID '{film_id}' tidak ditemukan.")
        return

    if sudah_ada(wishlist, user_id, film_id):
        print(f"[-] Gagal: '{judul_film(film_ketemu)}' sudah ada di wishlist kamu.")
        return

    print(f"Film Terpilih: {judul_film(film_ketemu)} [{film_id}]")
    prioritas = input("Prioritas (tinggi/sedang/rendah) [sedang]: ").strip().lower() or "sedang"
    if prioritas not in PRIORITAS:
        print("[-] Gagal: prioritas harus 'tinggi', 'sedang', atau 'rendah'.")
        return

    wishlist.append({
        "id": next_id(wishlist),
        "user_id": str(user_id),
        "film_id": film_id,
        "prioritas": prioritas,
        "status": "belum",
        "created_at": now(),
    })
    save_wishlist(wishlist)
    print(f"\n[+] '{judul_film(film_ketemu)}' berhasil ditambahkan ke wishlist!")

# ---------- READ (lihat, cari, filter, urutkan) ----------
def lihat_wishlist(user_id):
    bersihkan_layar()
    print("=== Wishlist Saya ===".center(75))
    tampilkan_wishlist(wishlist_milik(load_wishlist(), user_id), load_films())

def cari_wishlist(user_id):
    bersihkan_layar()
    print("=== Cari di Wishlist ===")
    films = load_films()
    kata = input("Kata kunci judul: ").strip().lower()
    hasil = []
    for w in wishlist_milik(load_wishlist(), user_id):
        film = find_film(films, w["film_id"])
        if film and kata in judul_film(film).lower():
            hasil.append(w)
    tampilkan_wishlist(hasil, films)

def filter_status(user_id):
    bersihkan_layar()
    print("=== Filter Status ===")
    print("1. Belum ditonton")
    print("2. Sudah ditonton")
    pilih = input("Pilih: ").strip()
    if pilih == "1":
        status = "belum"
    elif pilih == "2":
        status = "sudah"
    else:
        print("Pilihan tidak valid.")
        return
    hasil = [w for w in wishlist_milik(load_wishlist(), user_id) if w["status"] == status]
    tampilkan_wishlist(hasil, load_films())

def urutkan_wishlist(user_id):
    bersihkan_layar()
    print("=== Urutkan Wishlist ===")
    print("1. Judul (A-Z)")
    print("2. Judul (Z-A)")
    print("3. Prioritas (tinggi -> rendah)")
    print("4. Terbaru ditambahkan")
    print("5. Terlama ditambahkan")
    pilih = input("Pilih: ").strip()

    films = load_films()
    data = wishlist_milik(load_wishlist(), user_id)

    def judul_key(w):
        film = find_film(films, w["film_id"])
        return judul_film(film).lower() if film else ""

    if pilih == "1":
        hasil = sorted(data, key=judul_key)
    elif pilih == "2":
        hasil = sorted(data, key=judul_key, reverse=True)
    elif pilih == "3":
        hasil = sorted(data, key=lambda w: URUT_PRIORITAS.get(w["prioritas"], 9))
    elif pilih == "4":
        hasil = sorted(data, key=lambda w: w["created_at"], reverse=True)
    elif pilih == "5":
        hasil = sorted(data, key=lambda w: w["created_at"])
    else:
        print("Pilihan tidak valid.")
        return
    tampilkan_wishlist(hasil, films)

# ---------- UPDATE ----------
def ubah_wishlist(user_id):
    bersihkan_layar()
    print("=== Ubah Wishlist ===".center(75))
    wishlist = load_wishlist()
    films = load_films()
    milik = wishlist_milik(wishlist, user_id)
    tampilkan_wishlist(milik, films)
    if not milik:
        return

    item = find_item(wishlist, user_id, input("\nMasukkan ID wishlist: ").strip())
    if not item:
        print("Item wishlist tidak ditemukan.")
        return

    print("Kosongkan input jika tidak ingin mengubah.")
    prioritas = input(f"Prioritas baru (tinggi/sedang/rendah) [{item['prioritas']}]: ").strip().lower()
    if prioritas:
        if prioritas not in PRIORITAS:
            print("Gagal: prioritas harus 'tinggi', 'sedang', atau 'rendah'.")
            return
        item["prioritas"] = prioritas

    status = input(f"Status baru (belum/sudah) [{item['status']}]: ").strip().lower()
    if status:
        if status not in STATUS:
            print("Gagal: status harus 'belum' atau 'sudah'.")
            return
        item["status"] = status

    save_wishlist(wishlist)
    print("\n[+] Wishlist berhasil diperbarui.")

def tandai_ditonton(user_id):
    bersihkan_layar()
    print("=== Tandai Sudah Ditonton ===")
    wishlist = load_wishlist()
    films = load_films()
    belum = [w for w in wishlist_milik(wishlist, user_id) if w["status"] == "belum"]
    tampilkan_wishlist(belum, films)
    if not belum:
        return

    item = find_item(wishlist, user_id, input("\nMasukkan ID wishlist: ").strip())
    if not item:
        print("Item wishlist tidak ditemukan.")
        return
    item["status"] = "sudah"
    save_wishlist(wishlist)
    print("\n[+] Film ditandai sudah ditonton. Jangan lupa beri review & rating!")

# ---------- DELETE ----------
def hapus_wishlist(user_id):
    bersihkan_layar()
    print("=== Hapus dari Wishlist === ".center(75))
    wishlist = load_wishlist()
    films = load_films()
    milik = wishlist_milik(wishlist, user_id)
    tampilkan_wishlist(milik, films)
    if not milik:
        return

    item = find_item(wishlist, user_id, input("\nMasukkan ID wishlist: ").strip())
    if not item:
        print("Item wishlist tidak ditemukan.")
        return

    film = find_film(films, item["film_id"])
    judul = judul_film(film) if film else "film ini"
    konfirmasi = input(f"Yakin hapus '{judul}' dari wishlist? (y/n): ").strip().lower()
    if konfirmasi == "y":
        wishlist.remove(item)
        save_wishlist(wishlist)
        print("\n[+] Film berhasil dihapus dari wishlist.")
    else:
        print("\nPenghapusan dibatalkan.")

# ---------- Sub-Menu Wishlist ----------
def menu_user_wishlist(sesi_user):
    """Menu wishlist untuk user yang dipanggil dari functions/users/index.py"""
    user_id = sesi_user["id"]
    while True:
        bersihkan_layar()
        garis(50)
        print(f"MENU WISHLIST (@{sesi_user['username']})")
        garis(50)
        print("1. Lihat wishlist saya")
        print("2. Cari di wishlist")
        print("3. Filter berdasarkan status")
        print("4. Urutkan wishlist")
        print("5. Tambah film ke wishlist")
        print("6. Ubah prioritas / status")
        print("7. Tandai sudah ditonton")
        print("8. Hapus dari wishlist")
        print("0. Kembali ke Dashboard User")
        print("e. Keluar Aplikasi")
        pilih = input("\nPilih menu: ").strip().lower()

        if pilih == "1":
            lihat_wishlist(user_id)
        elif pilih == "2":
            cari_wishlist(user_id)
        elif pilih == "3":
            filter_status(user_id)
        elif pilih == "4":
            urutkan_wishlist(user_id)
        elif pilih == "5":
            tambah_wishlist(user_id)
        elif pilih == "6":
            ubah_wishlist(user_id)
        elif pilih == "7":
            tandai_ditonton(user_id)
        elif pilih == "8":
            hapus_wishlist(user_id)
        elif pilih == "0":
            break
        elif pilih == "e":
            print("\nMenutup aplikasi... Sampai jumpa lagi, bro!")
            sys.exit()
        else:
            print("Pilihan tidak valid.")
        input("\nTekan Enter untuk lanjut...")