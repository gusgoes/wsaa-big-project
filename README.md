# Books REST API

A REST API built with Python and Flask to manage a collection of books, backed by a MySQL database.

This is the big project for the Web Services and Applications module.

## What it does

- Create, read, update and delete books via HTTP requests
- Each book has: title, author, price
- All responses return a consistent JSON format
- Input is validated before touching the database

## Project Structure

```
wsaa-big-project/
├── config/         database credentials (.env not committed)
├── docs/           setup guide and API reference
├── scripts/        database initialisation script
├── src/            Flask app and database layer
├── tests/          automated tests (18 tests)
└── requirements.txt
```

## Quick Start

See [docs/project/README.md](docs/project/README.md) for full setup steps.

Short version:
1. Create `config/.env` with your MySQL credentials
2. Run `python scripts/init_db.py` to create the database
3. Run `python src/app.py` to start the API on http://127.0.0.1:5000

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | /books | List all books |
| GET | /books/\<id\> | Get one book |
| POST | /books | Create a book |
| PUT | /books/\<id\> | Update a book |
| DELETE | /books/\<id\> | Delete a book |

See [docs/api/README.md](docs/api/README.md) for request/response examples.

## Running the Tests

```powershell
python -m pytest tests/ -v
```
