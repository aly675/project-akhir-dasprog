import sys
from functions.helper import bersihkan_layar, garis
from functions.users.moviesController import menu_katalog_user
from functions.users.reviewsController import menu_reviews_user
from functions.users.wishlistController import menu_user_wishlist

def menu_user(sesi_user):
    while True:
        bersihkan_layar()
        garis(50)
        print(f"DASHBOARD USER - Halo, {sesi_user['nama']}")
        garis(50)
        print("1. Jelajahi & Detail Film")
        print("2. Beri Rating & Komentar Film")
        print("3. Kelola Wishlist Saya")
        print("0. Logout (Kembali ke Gerbang Utama)")
        print("e. Keluar Aplikasi")
        
        pilihan = input("Pilih menu: ").strip().lower()
        
        if pilihan == '1':
            menu_katalog_user(sesi_user)
        elif pilihan == '2':
            menu_reviews_user(sesi_user)
            input("Tekan Enter untuk lanjut...")
        elif pilihan == '3':
            menu_user_wishlist(sesi_user)
            input("Tekan Enter untuk lanjut...")
        elif pilihan == '0':
            print("\nLogout berhasil! Kembali ke menu utama...")
            break
        elif pilihan == 'e':
            print("\nMenutup aplikasi... Sampai jumpa lagi, bro!")
            sys.exit()
        else:
            print("Pilihan tidak valid!")
            input("Tekan Enter untuk lanjut...")