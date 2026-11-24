import csv
import os
from functions.helper import bersihkan_layar, garis, hash_password, now

# ==========================================
# KONSTANTA GLOBAL
# ==========================================
FILE_USERS = 'databases/users.csv'
HEADER_USERS = ['id', 'username', 'password', 'nama', 'role', 'created_at']

def proses_register():
    bersihkan_layar()
    garis(45)
    print("REGISTER AKUN BARU")
    garis(45)
    
    username = input("Buat username: ").strip().lower()
    if not username:
        print("Username tidak boleh kosong!")
        return

    next_id = 1
    file_ada = os.path.exists(FILE_USERS)
    
    if file_ada:
        with open(FILE_USERS, mode='r', encoding='utf-8') as file:
            reader = list(csv.DictReader(file))
            for row in reader:
                if row['username'] == username:
                    print("Username sudah dipakai!")
                    return
            
            if reader:
                next_id = int(reader[-1]['id']) + 1

    while True:
        password = input("Buat password (minimal 5 karakter): ").strip().lower()
        if len(password) < 5:
            print("Password minimal 5 karakter!")
        else:
            break

    nama = input("Masukkan nama lengkap: ").strip().title()
    if not nama:
        print("Nama tidak boleh kosong!")
        return

    hashed_pw = hash_password(password)
    waktu_sekarang = now()

    os.makedirs(os.path.dirname(FILE_USERS), exist_ok=True)
    with open(FILE_USERS, mode='a', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=HEADER_USERS, extrasaction='ignore')
        if not file_ada:
            writer.writeheader()
        writer.writerow({
            'id': next_id,
            'username': username,
            'password': hashed_pw,
            'nama': nama,
            'role': 'user',
            'created_at': waktu_sekarang
        })
        
    print("\nAkun anda berhasil dibuat! Silakan login.")