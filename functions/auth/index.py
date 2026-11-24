import sys
from functions.helper import bersihkan_layar, garis
from functions.auth.register import proses_register
from functions.auth.login import proses_login

def menu_auth():
    while True:
        bersihkan_layar()
        garis(45)
        print("Halaman Login LETTERBOX")
        garis(45)
        print("1. Login")
        print("2. Register")
        print("e. Keluar Aplikasi")
        
        pilihan = input("Pilih menu: ").strip().lower()
        
        if pilihan == '1':
            user_data = proses_login()
            if user_data:
                return user_data
            input("\nTekan Enter untuk kembali...")
        elif pilihan == '2':
            proses_register()
            input("\nTekan Enter untuk kembali...")
        elif pilihan == 'e':
            print("\nMenutup aplikasi... Sampai jumpa lagi")
            sys.exit() 
        else:
            print("Pilihan tidak valid! Ketik 1, 2, atau 'e' untuk keluar.")
            input("\nTekan Enter untuk lanjut...")