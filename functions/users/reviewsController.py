import csv
import os
import sys
from datetime import datetime
from functions.helper import bersihkan_layar, garis, now

# ==========================================
# KONSTANTA GLOBAL
# ==========================================
FILE_REVIEWS = 'databases/reviews.csv'
HEADER_REVIEWS = ['id_review', 'id_film', 'username', 'rating', 'komentar', 'created_at']
FILE_FILM = 'databases/movies.csv'

# ---------- Helper & Akses File ----------

def generate_id_review(data_reviews):
    """Otomatis generate ID dengan format R001, R002, dst."""
    if not data_reviews:
        return "R001"
    angka_terakhir = max(
        (int(r['id_review'][1:]) for r in data_reviews if r['id_review'].upper().startswith('R') and r['id_review'][1:].isdigit()),
        default=0
    )
    return f"R{angka_terakhir + 1:03d}"

def load_reviews():
    if not os.path.exists(FILE_REVIEWS):
        os.makedirs(os.path.dirname(FILE_REVIEWS), exist_ok=True)
        with open(FILE_REVIEWS, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=HEADER_REVIEWS)
            writer.writeheader()
        return []
    with open(FILE_REVIEWS, mode='r', encoding='utf-8') as file:
        return list(csv.DictReader(file))

def save_reviews(data_reviews):
    with open(FILE_REVIEWS, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=HEADER_REVIEWS, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(data_reviews)

def cek_film_ada(id_film):
    """Memastikan ID film valid dan mengembalikan judulnya."""
    if not os.path.exists(FILE_FILM):
        return None
    with open(FILE_FILM, mode='r', encoding='utf-8') as file:
        for row in csv.DictReader(file):
            if row['id_film'].strip().upper() == id_film.upper():
                return row['judul']
    return None

# ---------- CREATE / UPDATE (Beri atau Ubah Rating & Komentar) ----------
def beri_rating_komentar(sesi_user, id_film_target=None):
    bersihkan_layar()
    garis(60)
    print("BERI RATING & KOMENTAR FILM")
    garis(60)

    # Jika dipanggil dari menu utama (bukan dari detail film), minta input ID Film
    if id_film_target is None:
        id_film_target = input("Masukkan ID Film (contoh: M001): ").strip().upper()
    else:
        id_film_target = id_film_target.strip().upper()

    judul_film = cek_film_ada(id_film_target)
    if not judul_film:
        print(f"[-] Film dengan ID '{id_film_target}' tidak ditemukan!")
        return

    print(f"Film Terpilih : {judul_film} [{id_film_target}]")
    print(f"Reviewer      : {sesi_user['nama']} (@{sesi_user['username']})")
    garis(60)

    data_reviews = load_reviews()
    username = sesi_user['username'].lower()

    # Cek apakah user sudah pernah mereview film ini sebelumnya
    review_lama = next(
        (r for r in data_reviews if r['id_film'].upper() == id_film_target and r['username'].lower() == username),
        None
    )

    if review_lama:
        print(f"[Info] Kamu sudah pernah menilai film ini ({review_lama['rating']}/5).")
        print("Input baru akan memperbarui rating & komentarmu sebelumnya.\n")

    # 1. Input Rating (Wajib: 1 - 5)
    while True:
        input_rating = input("Masukkan Rating (1 - 5): ").strip()
        try:
            nilai = float(input_rating)
            if 1.0 <= nilai <= 5.0:
                # Rapikan format angka (misal 4.0 tetap 4.0 atau sesuai input)
                rating_final = f"{nilai:.1f}" if '.' in input_rating else str(int(nilai))
                break
            else:
                print("[-] Rating harus di antara 1 sampai 5")
        except ValueError:
            print("[-] Masukkan angka yang valid (contoh: 4 atau 4.5)!")

    # 2. Input Komentar (Opsional)
    print("\nTulis komentar/ulasan singkat (Tekan Enter langsung jika tidak ingin berkomentar):")
    komentar = input("> ").strip()

    waktu_sekarang = now()

    if review_lama:
        review_lama['rating'] = rating_final
        review_lama['komentar'] = komentar
        review_lama['created_at'] = waktu_sekarang
        pesan = f"\n[+] Ulasan kamu untuk '{judul_film}' berhasil diperbarui!"
    else:
        data_reviews.append({
            'id_review': generate_id_review(data_reviews),
            'id_film': id_film_target,
            'username': username,
            'rating': rating_final,
            'komentar': komentar,
            'created_at': waktu_sekarang
        })
        pesan = f"\n[+] Terima kasih! Rating & ulasan untuk '{judul_film}' berhasil disimpan!"

    save_reviews(data_reviews)
    print(pesan)

# ---------- READ (Lihat Riwayat Ulasan Saya) ----------
def lihat_ulasan_saya(sesi_user):
    bersihkan_layar()
    data_reviews = load_reviews()
    username = sesi_user['username'].lower()
    
    ulasan_saya = [r for r in data_reviews if r['username'].lower() == username]

    garis(78)
    print(f"RIWAYAT RATING & ULASAN SAYA (@{username})")
    garis(78)

    if not ulasan_saya:
        print("Kamu belum pernah memberikan rating atau ulasan film apa pun.")
        return

    for r in ulasan_saya:
        judul = cek_film_ada(r['id_film']) or "(Film telah dihapus)"
        komen = r['komentar'] if r['komentar'] else "(Tanpa komentar)"
        print(f"[{r['id_review']}] {judul} ({r['id_film']}) | Rating: {r['rating']}/5")
        print(f"       Komentar : {komen}")
        print(f"       Waktu    : {r['created_at']}\n")
    garis(78)
    print(f"Total: {len(ulasan_saya)} ulasan")

# ---------- DELETE (Hapus Ulasan Saya) ----------
def hapus_ulasan_saya(sesi_user):
    lihat_ulasan_saya(sesi_user)
    data_reviews = load_reviews()
    username = sesi_user['username'].lower()
    
    ulasan_saya = [r for r in data_reviews if r['username'].lower() == username]
    if not ulasan_saya:
        return

    id_target = input("\nMasukkan ID Review yang mau dihapus (contoh: R001): ").strip().upper()
    target = next((r for r in ulasan_saya if r['id_review'].upper() == id_target), None)

    if not target:
        print("[-] ID Review tidak ditemukan atau bukan milik akun kamu.")
        return

    konfirmasi = input(f"Yakin ingin menghapus ulasan {id_target}? (y/n): ").strip().lower()
    if konfirmasi == 'y':
        data_reviews.remove(target)
        save_reviews(data_reviews)
        print(f"\n[+] Ulasan {id_target} berhasil dihapus!")
    else:
        print("\nPenghapusan dibatalkan.")

# ---------- Sub-Menu Rating & Komentar ----------
def menu_reviews_user(sesi_user):
    while True:
        bersihkan_layar()
        garis(50)
        print("MENU RATING & KOMENTAR FILM")
        garis(50)
        print("1. Beri / Ubah Rating & Komentar Film")
        print("2. Lihat Riwayat Ulasan Saya")
        print("3. Hapus Ulasan Saya")
        print("0. Kembali ke Dashboard User")
        print("e. Keluar Aplikasi")

        pilih = input("\nPilih menu: ").strip().lower()
        if pilih == '1':
            beri_rating_komentar(sesi_user)
        elif pilih == '2':
            lihat_ulasan_saya(sesi_user)
        elif pilih == '3':
            hapus_ulasan_saya(sesi_user)
        elif pilih == '0':
            break
        elif pilih == 'e':
            print("\nMenutup aplikasi... Sampai jumpa lagi, bro!")
            sys.exit()
        else:
            print("Pilihan tidak valid!")
        input("\nTekan Enter untuk lanjut...")