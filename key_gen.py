from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())

with open("encryption_key.txt", "w") as key_file:
    key_file.write(Fernet.generate_key().decode())