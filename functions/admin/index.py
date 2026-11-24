import sys
from functions.helper import bersihkan_layar, garis
from functions.admin.usersController import menu_admin_user
from functions.admin.moviesController import menu_admin_movies

def menu_admin(sesi_user):
    while True:
        bersihkan_layar()
        garis(45)
        print(f"DASHBOARD ADMIN - Halo, {sesi_user['nama']}")
        garis(45)
        print("1. Kelola Film (CRUD Movies)")
        print("2. Kelola Akun User (CRUD Users)")
        print("0. Logout (Kembali ke Gerbang Utama)")
        print("e. Keluar Aplikasi")
        
        pilihan = input("Pilih menu: ").strip().lower()
        
        if pilihan == '1':
            menu_admin_movies()
        elif pilihan == '2':
            menu_admin_user(sesi_user['username'])
        elif pilihan == '0':
            print("\nLogout berhasil! Kembali ke menu utama...")
            break
        elif pilihan == 'e':
            print("\nMenutup aplikasi... Sampai jumpa lagi!")
            sys.exit()
        else:
            print("Pilihan tidak valid!")
            input("Tekan Enter untuk lanjut...")
