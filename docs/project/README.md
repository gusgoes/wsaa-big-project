# Project Setup and Run Guide

Use this exact sequence from the repository root:

`...\25-26-8640----WEB-SERVICES-AND-APPLICATIONS`

## 1. Prerequisites

- Python 3.11+
- MySQL Server running on localhost:3306
- Virtual environment exists at `.venv`

## 2. Activate Virtual Environment (PowerShell)

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

Expected prompt starts with:

```text
(.venv)
```

## 3. Install Dependencies

```powershell
python -m pip install -r project\requirements.txt
```

## 4. Configure Database Credentials

Create this file:

`project\config\.env`

Add:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=wsaa
```

## 5. Initialize Database and Table

```powershell
python project\scripts\init_db.py
```

Expected success:

```text
Database and table ready
```

## 6. Run API

```powershell
python project\src\app.py
```

Expected:

```text
* Running on http://127.0.0.1:5000
```

## 7. Quick API Test (PowerShell)

Create:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5000/books -Method POST -ContentType "application/json" -Body '{"title":"1984","author":"George Orwell","price":10.5}'
```

Read all:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5000/books -Method GET
```

Read by id:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5000/books/1 -Method GET
```

Update:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5000/books/1 -Method PUT -ContentType "application/json" -Body '{"title":"1984","author":"George Orwell","price":8.99}'
```

Delete:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5000/books/1 -Method DELETE
```

## 8. Troubleshooting

- `No module named mysql`
Activate `.venv` first, then run commands again.

- `Access denied for user 'root'@'localhost'`
Check `DB_PASSWORD` in `project\config\.env`.

- `Can't connect to MySQL server on localhost:3306`
Start MySQL service, then rerun `init_db.py`.