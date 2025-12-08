import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

# Set the encryption key from the env file
ENCRYPTION_KEY = os.getenv("BACKUP_KEY")
if not ENCRYPTION_KEY:
    raise ValueError("ERROR: BACKUP_KEY env not set!")

# Initialize the encryption
fernet = Fernet(ENCRYPTION_KEY.encode())


# Input the encrypted file to decrypt
file = input("Enter encrypted file: ").strip()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKUP_DIR = os.path.join(BASE_DIR, "backups")
enc_file = os.path.join(BACKUP_DIR, file)
output = enc_file.replace(".enc", "")

# Decrypt the encrypted file
with open(enc_file, "rb") as f:
    decrypted = fernet.decrypt(f.read())

# Save the decrypted file
with open(output, "wb") as f:
    f.write(decrypted)


print(f"Decrypted file: {decrypted}")