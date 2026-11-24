from datetime import datetime
import os
import hashlib

def bersihkan_layar():
    os.system('cls' if os.name == 'nt' else 'clear')

def garis(panjang=75):
    print("=" * panjang)

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")