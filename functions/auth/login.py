import csv
from functions.helper import bersihkan_layar, garis, hash_password

FILE_USERS = 'databases/users.csv'

def proses_login():
    bersihkan_layar()
    garis(45)
    print("LOGIN APLIKASI")
    garis(45)
    username = input("Username: ").strip().lower()
    password = input("Password: ").strip().lower()
    
    hashed_input_pw = hash_password(password)
    
    try:
        with open(FILE_USERS, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                if row['username'] == username and row['password'] == hashed_input_pw:
                    print(f"\nLogin berhasil! Selamat datang, {row['nama']} ({row['role']}).")
                    return row 
                    
        print("\nLogin gagal! Username atau password salah!")
        return None
        
    except FileNotFoundError:
        print("\nDatabase user belum ditemukan! Silakan register dulu.")
        return None