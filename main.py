from functions.auth.index import menu_auth
from functions.admin.index import menu_admin
from functions.users.index import menu_user

def main():
    while True:
        sesi_user = menu_auth() # row 
        
        if sesi_user['role'] == 'admin':
            menu_admin(sesi_user)
            
        elif sesi_user['role'] == 'user':
            menu_user(sesi_user)

if __name__ == "__main__":
    main()