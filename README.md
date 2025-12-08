🎓 University Information System

Backend + PostgreSQL DBA Portfolio Project

This project is a simplified backend system that simulates how a real university information system works behind the scenes.
It showcases Flask backend development, role-based authentication, and PostgreSQL database administration—including schemas, roles, permissions, migrations, and automated encrypted backups.

The goal is to demonstrate practical backend + DBA skills similar to what a junior backend/DBA hybrid role would require.

🌟 What This Project Demonstrates


🖥️ 1. Backend Engineering (Flask)
- Role-based login system (Admin, Faculty, Student, Librarian)
- Jinja templates + organized routing
- REST API structure
- Custom RBAC wrappers + @login_required
- Session-based authentication
- SQLAlchemy ORM models
- Flask-Migrate (Alembic) for schema versioning
- CRUD operations (Delete intentionally excluded for data integrity)


🗃️ 2. PostgreSQL Database Administration

This project includes real DBA tasks:

✔ Schema Design
Schemas for different functional areas, such as:
    
    - app
    - analysis
    - qa
    - etl

✔ Role Management
Custom PostgreSQL roles:  
    - admin (Superuser)
    - dba (Maintenance)
    - app_user (Flask app)
    - d_analyst
    - d_engineer
    - qa_engineer

✔ Grants & Permissions
- Fine-grained privileges (SELECT/INSERT/UPDATE)
- Schema-level access restrictions
- Ownership management
- Least-privilege model applied to all roles

✔ Backup & Restore Procedures

- Logical backups (pg_dump)
- Encrypted backup storage
- Decryption script for restoration
- Separate restore environment on port 5333


🛠️ 3. Realistic Project Structure

This project mimics how institutions separate data and responsibility across schemas and roles.
Each role sees only the functionality they are allowed—both at the app layer and database layer.

dba/
├── app/
│   ├── main.py                # Flask application
│   ├── config.py              # Flask config
│   ├── models.py              # SQLAlchemy ORM models
│   ├── forms.py               # WTForms
│   ├── templates/             # HTML files
│   └── static/                # Static Files
│
├── backups/                   # Encrypted backup files
│
├── backup_scripts/
│   ├── backup.py              # logic for pg_dump + encryption
│   └── decrypt.py             # logic for decryption
│
├── database-postgresql/
│   ├── SQL/                   # SQL scripts for roles, schemas, grants
│   ├── ERD/                   # ERD images
│   └── DB Restore Test/       # DB restore test images using PowerShell
│
├── migrations/                # From Flask-Migrate
│
├── tests/                     # Test environment for database restoration
│
├── .env.example
├── .gitignore
└── requirements.txt



🧪 Test Environment (Port 5333)

A dedicated PostgreSQL instance was set up for backup restore testing:

- Ensures dumps restore without errors
- Allows safe testing without touching the main DB
- Simulates real DBA workflows


🔄 Automated Logical Backup (Encrypted)

The backup process is handled by a standalone Python script, which can be automated using Task Scheduler (Windows) or cron (Linux).
The script performs:

✔ Daily pg_dump (logical backup)
✔ AES encryption
✔ Timestamped file naming
✔ Backup rotation (deletes old backups safely)
✔ .pgpass support (no password prompts)

This setup protects backups at rest and avoids storage overflow—similar to a real DBA environment.


🔓 Manual Decryption for Restore

A small utility script allows:

- Selecting an encrypted backup
- Decrypting it
- Preparing a clean .sql file
- Initialize a separate PostgreSQL instance
- Restore using pg_restore on a test database

This completes the full backup → encryption → decryption → restore workflow.


🎯 Why This Project Exists

I built this system to demonstrate BOTH:

✔ Backend Development Skills
✔ Database Administration Skills

Many junior roles require a mix of API, database, and system maintenance skills.

This project shows the ability to:

- Build real backend features
- Manage and secure databases
- Implement RBAC at both application + DB levels
- Perform migrations, backups, and restores
- Understand production-like workflows


📌 Project Status

✅ Backend complete
✅ RBAC implemented
✅ Schemas and permissions configured
✅ Logical backup automation done
✅ Encrypted backup + decryption script added
