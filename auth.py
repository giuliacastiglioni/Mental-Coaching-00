import json
import os
import bcrypt

USERS_FILE = "users.json"

# -------------------------
# UTILS
# -------------------------
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)

# -------------------------
# REGISTRAZIONE
# -------------------------
def register_user(nome, ruolo, password):
    users = load_users()

    if nome in users:
        return False, "Utente già esistente"

    hashed_pw = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

    users[nome] = {
        "ruolo": ruolo,
        "password": hashed_pw
    }

    save_users(users)
    return True, "Registrazione completata"

# -------------------------
# LOGIN
# -------------------------
def check_login(nome, password):
    users = load_users()

    if nome not in users:
        return False, None

    stored_hash = users[nome]["password"].encode()

    if bcrypt.checkpw(password.encode(), stored_hash):
        return True, users[nome]["ruolo"]

    return False, None
