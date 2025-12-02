import os, subprocess, datetime
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

# Terms: Daily backups - Database only, Global backups - Roles only

# Configuration variables

DBA = "dba" # The user account for daily backups
ADMIN = "admin" # The user account for global backups (SUPERUSER)
DB_NAME = "university" # The database name

# Configure the folder of the backups
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKUP_DIR = os.path.join(BASE_DIR, "backups")

# Days for how long the daily backups and global backups (monthly) are kept
RETENTION_DAYS = 7
RETENTION_MONTHS = 6

# Call the backup key from Fernet and raise an error if not set in order to avoid unencrypt backups
ENCRYPTION_KEY = os.getenv("BACKUP_KEY")
if not ENCRYPTION_KEY:
    raise ValueError("ERROR: BACKUP_KEY env not set!")

# Initialize Fernet encyrption
fernet = Fernet(ENCRYPTION_KEY.encode())

# Create the folder for the backups
os.makedirs(BACKUP_DIR, exist_ok=True)

# Configure the dates for daily and monthly backups save date
today = datetime.datetime.now().strftime("%Y-%m-%d")
month = datetime.datetime.now().strftime("%Y-%m")

# Create the functions

# Create a function to encrypt the backup file
def encrypt_file(base_file):
    encrypted_file = base_file + ".enc"
    with open(base_file, "rb") as f:
        encrypted_data = f.read()
    encrypted_data = fernet.encrypt(encrypted_data)
    with open(encrypted_file, "wb") as f:
        f.write(encrypted_data)
    os.remove(base_file)
    return encrypted_file

# Create the function for the daily backups
def daily_backup():
    base_file = os.path.join(BACKUP_DIR, f"{DB_NAME}_{today}.dump")
    cmd = [
        "pg_dump", "-U", DBA, "-Fc",
        "--serializable-deferrable", "--no-owner", DB_NAME
    ]

    print("Running pg_dump...")
    with open(base_file, "wb") as f:
        result = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print("Database backup FAILED!")
        print(result.stderr)
        exit(1)

    print("Database backup successful.")
    enc = encrypt_file(base_file)
    print(f"Encrypted DB backup: {enc}")

# Create the function for the global backups
def global_backup():
    global_file = os.path.join(BACKUP_DIR, f"global_{month}.sql")
    cmd = [
        "pg_dumpall", "-U", ADMIN, "--globals-only"
    ]

    print("Running pg_dumpall --globals-only")
    with open(global_file, "wb") as f:
        result = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print("Globals backup FAILED!")
        print(result.stderr)
        exit(1)

    print("Globals backup successful.")
    enc = encrypt_file(global_file)
    print(f"Encrypted globals backup: {enc}")

# Create the function for deleting the old files age which matches the retention days
def delete_backup():
    now = datetime.datetime.now()

    for filename in os.listdir(BACKUP_DIR):
        file_path = os.path.join(BACKUP_DIR, filename)

        if not filename.endswith(".enc"):
            continue
        file_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))

        if filename.startswith(DB_NAME):
            if (now - file_time).days > RETENTION_DAYS:
                os.remove(file_path)
                print(f"Deleted old DB backup: {filename}")

        if filename.startswith("globals_"):
            month_old = (now.year - file_time).year * 12 + (now.month - file_time.month)
            if month_old > RETENTION_MONTHS:
                os.remove(file_path)
                print(f"Deleted old Globals backup: {filename}")

# Run the backup

print("PostgreSQL backup running...")
print("Date: " + today)

# Run the daily backup
daily_backup()

# Run the globals backup during first day of the month (1)
if datetime.datetime.now().day == 1:
    global_backup()

# Delete the old backups if possible
delete_backup()

print("Backup for " + today + " successful.")