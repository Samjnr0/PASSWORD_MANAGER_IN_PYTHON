import hashlib
import secrets
import json
import os

def generate_salt():
    return secrets.token_hex(16)

def hash_password(password, salt):
    password_salt = password + salt
    return hashlib.sha512(password_salt.encode()).hexdigest()

def save_user(username, hashed_password, salt):
    if not os.path.exists("users.json"):
        with open("users.json", "w") as user_file:
            json.dump({}, user_file)

    with open("users.json", "r") as user_file:
        users = json.load(user_file)

    users[username] = {"password": hashed_password, "salt": salt}

    with open("users.json", "w") as user_file:
        json.dump(users, user_file, indent=4)

def user_exists(username):
    if not os.path.exists("users.json"):
        return False

    with open("users.json", "r") as user_file:
        users = json.load(user_file)
    return username in users

def sign_up():
    username = input("Please enter a username: ")
    password = input("Please enter a password: ")

    if user_exists(username):
        print("Username already exists. Please choose a different one.")
    else:
        salt = generate_salt()
        hashed_password = hash_password(password, salt)
        save_user(username, hashed_password, salt)
        print("Your account has been created successfully!")

def login():
    username = input("Please enter your username: ")
    password = input("Please enter your password: ")

    if user_exists(username):
        with open("users.json", "r") as user_file:
            users = json.load(user_file)
        stored_password = users[username]["password"]
        stored_salt = users[username]["salt"]
        hashed_password = hash_password(password, stored_salt)

        if hashed_password == stored_password:
            print("Logged in successfully!")
        else:
            print("Incorrect password. Please try again.")
    else:
        print("Username not found. Please sign up.")

def main():
    while True:
        print("\nWelcome to the Password Manager")
        print("1. Sign Up")
        print("2. Login")
        print("3. Exit")
        choice = input("Please select an option: ")

        if choice == "1":
            sign_up()
        elif choice == "2":
            login()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
