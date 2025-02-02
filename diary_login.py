from flask import session
import json
import os

USER_FILE = 'data/diary_users.json'  # Updated file name

# Load users
def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# Save users
def save_users(users):
    with open(USER_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=4)

# Check if logged in
def is_login():
    return 'login' in session

# Login
def try_login(user, password):
    users = load_users()
    if user in users and users[user] == password:
        session['login'] = user
        return True
    return False

# Logout
def try_logout():
    session.pop('login', None)

# Add new user
def add_user(user, password):
    users = load_users()
    if user in users:
        return False  # User already exists

    users[user] = password
    save_users(users)
    return True

# Get logged-in user
def get_user():
    return session.get('login', 'not login')
