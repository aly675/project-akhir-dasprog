import csv
import os
import sys
from functions.helper import bersihkan_layar, garis, hash_password, now

FILE_USERS = 'databases/users.csv'
HEADER_USERS = ['id', 'username', 'password', 'nama', 'role', 'created_at']

# ---------- Akses File ----------
def load_users():
    """Baca semua user dari CSV -> list of dict."""
    if not os.path.exists(FILE_USERS):
        os.makedirs(os.path.dirname(FILE_USERS), exist_ok=True)
        default = [{
            "id": "1",
            "username": "admin",
            "password": hash_password("admin123"),
            "nama": "Administrator",
            "role": "admin",
            "created_at": now(),
        }]
        save_users(default)
        return default
    with open(FILE_USERS, "r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def save_users(users):
    with open(FILE_USERS, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADER_USERS, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(users)

def next_id(users):
    return str(max((int(u["id"]) for u in users), default=0) + 1)

def find_by_id(users, user_id):
    for u in users:
        if u["id"] == user_id:
            return u
    return None

def username_exists(users, username, abaikan_id=None):
    for u in users:
        if u["username"].lower() == username.lower() and u["id"] != abaikan_id:
            return True
    return False

# ---------- Validasi ----------
def validasi_username(users, username, abaikan_id=None):
    if len(username) < 3:
        return "Username minimal 3 karakter."
    if " " in username:
        return "Username tidak boleh mengandung spasi."
    if not username.replace("_", "").isalnum():
        return "Username hanya boleh huruf, angka, dan underscore."
    if username_exists(users, username, abaikan_id):
        return "Username sudah dipakai."
    return None

def validasi_password(password):
    if len(password) < 5:
        return "Password minimal 5 karakter."
    return None

# ---------- Tampilan ----------
def tampilkan_tabel(data):
    if not data:
        print("Data user tidak ditemukan.")
        return
    
    admins =   [u for u in data if u["role"] == "admin"]
    users =    [u for u in data if u["role"] == "user"]
    data_urut = admins + users 
    garis()
    print(f"{'ID':<5}{'Username':<18}{'Nama':<22}{'Role':<10}{'Dibuat':<20}")
    garis()
    for u in data_urut:
        print(f"{u['id']:<5}{u['username']:<18}{u['nama']:<22}{u['role']:<10}{u['created_at']:<20}")
    garis()
    print(f"Total: {len(data)} user")

# ---------- CREATE ----------
def tambah_user(users):
    bersihkan_layar()
    print("=== Tambah User ===")
    username = input("Username : ").strip().lower()
    error = validasi_username(users, username)
    if error:
        print("Gagal:", error)
        return

    password = input("Password (min 5 karakter) : ").strip().lower()
    error = validasi_password(password)
    if error:
        print("Gagal:", error)
        return

    nama = input("Nama Lengkap : ").strip().title()
    if not nama:
        print("Gagal: Nama tidak boleh kosong.")
        return

    role = input("Role (user/admin) [user]: ").strip().lower() or "user"
    if role not in ("user", "admin"):
        print("Gagal: role harus 'user' atau 'admin'.")
        return

    users.append({
        "id": next_id(users),
        "username": username,
        "password": hash_password(password),
        "nama": nama,
        "role": role,
        "created_at": now(),
    })
    save_users(users)
    print(f"User '{username}' ({nama}) berhasil ditambahkan.")

# ---------- READ (lihat, cari, urutkan) ----------
def lihat_user(users):
    bersihkan_layar()
    print("=== Daftar User ===".center(75))
    tampilkan_tabel(users)

def cari_user(users):
    bersihkan_layar()
    print("=== Cari User ===".center(75))
    kata = input("Kata kunci username / nama: ").strip().lower()
    hasil = [u for u in users if kata in u["username"].lower() or kata in u["nama"].lower()]
    tampilkan_tabel(hasil)

def urutkan_user(users):
    bersihkan_layar()
    print("=== Urutkan User ===")
    print("1. Username (A-Z)")
    print("2. Username (Z-A)")
    print("3. Terbaru dibuat")
    print("4. Terlama dibuat")
    pilih = input("Pilih: ").strip()

    if pilih == "1":
        hasil = sorted(users, key=lambda u: u["username"].lower())
    elif pilih == "2":
        hasil = sorted(users, key=lambda u: u["username"].lower(), reverse=True)
    elif pilih == "3":
        hasil = sorted(users, key=lambda u: u["created_at"], reverse=True)
    elif pilih == "4":
        hasil = sorted(users, key=lambda u: u["created_at"])
    else:
        print("Pilihan tidak valid.")
        return
    
    admins = [u for u in hasil if u["role"] == "admin"]
    users = [u for u in hasil if u["role"] == "user"]
    hasil = admins + users
    tampilkan_tabel(hasil)

# ---------- UPDATE ----------
def ubah_user(users):
    bersihkan_layar()
    print("=== Ubah User ===".center(75))
    tampilkan_tabel(users)
    user = find_by_id(users, input("Masukkan ID user: ").strip())
    if not user:
        print("User tidak ditemukan.")
        return

    print("Kosongkan input jika tidak ingin mengubah.")
    username = input(f"Username baru [{user['username']}]: ").strip().lower()
    if username:
        error = validasi_username(users, username, abaikan_id=user["id"])
        if error:
            print("Gagal:", error)
            return
        user["username"] = username

    password = input("Password baru (min 5 karakter): ").strip().lower()
    if password:
        error = validasi_password(password)
        if error:
            print("Gagal:", error)
            return
        user["password"] = hash_password(password)

    nama = input(f"Nama baru [{user['nama']}]: ").strip().title()
    if nama:
        user["nama"] = nama

    role = input(f"Role baru (user/admin) [{user['role']}]: ").strip().lower()
    if role:
        if role not in ("user", "admin"):
            print("Gagal: role harus 'user' atau 'admin'.")
            return
        user["role"] = role

    save_users(users)
    print("Data user berhasil diperbarui.")

# ---------- DELETE ----------
def hapus_user(users, admin_login):
    bersihkan_layar()
    print("=== Hapus User ===".center(75))
    tampilkan_tabel(users)
    user = find_by_id(users, input("Masukkan ID user: ").strip())
    if not user:
        print("User tidak ditemukan.")
        return
    if user["username"] == admin_login:
        print("Gagal: tidak bisa menghapus akun yang sedang login.")
        return

    konfirmasi = input(f"Yakin hapus '{user['username']}'? (y/n): ").strip().lower()
    if konfirmasi == "y":
        users.remove(user)
        save_users(users)
        print("User berhasil dihapus.")
    else:
        print("Penghapusan dibatalkan.")

# ---------- Menu Sub-Modul ----------
def menu_admin_user(admin_login):
    """Menu utama CRUD user yang dipanggil dari functions/admin/index.py"""
    while True:
        bersihkan_layar()
        users = load_users()
        garis()
        print(f"KELOLA AKUN USER (Admin: {admin_login})")
        garis()
        print("1. Lihat semua user")
        print("2. Cari user")
        print("3. Urutkan user")
        print("4. Tambah user")
        print("5. Ubah user")
        print("6. Hapus user")
        print("0. Kembali ke Dashboard Admin")
        print("e. Keluar Aplikasi")
        pilih = input("Pilih menu: ").strip().lower()

        if pilih == "1":
            lihat_user(users)
        elif pilih == "2":
            cari_user(users)
        elif pilih == "3":
            urutkan_user(users)
        elif pilih == "4":
            tambah_user(users)
        elif pilih == "5":
            ubah_user(users)
        elif pilih == "6":
            hapus_user(users, admin_login)
        elif pilih == "0":
            break
        elif pilih == "e":
            print("\nMenutup aplikasi... Sampai jumpa lagi, bro!")
            sys.exit()
        else:
            print("Pilihan tidak valid.")
        input("\nTekan Enter untuk lanjut...")