# request-sentinel 🛡️

A Flask web server that automatically logs all incoming HTTP requests to a remote database.

## Project Structure

```
request-sentinel/
├── app/
│   ├── middleware/
│   │   └── request_logger.py   # Before/after request hooks
│   ├── models/
│   │   ├── db.py               # SQLAlchemy init
│   │   └── request_log.py      # RequestLog model
│   └── routes/
│       └── main.py             # API endpoints
├── config/
│   └── settings.py             # Dev / prod / test configs
├── tests/
│   └── test_app.py
├── .env.example
├── requirements.txt
└── run.py                      # Entrypoint
```

## Getting Started

```bash
# 1. Clone and enter the repo
git clone <your-repo-url> && cd request-sentinel

# 2. Create a virtual environment
python -m venv venv && source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and set your DATABASE_URL

# 5. Run the server
python run.py
```

## Endpoints

| Method | Path   | Description                        |
|--------|--------|------------------------------------|
| GET    | `/`    | Health check                       |
| GET    | `/logs`| Returns the 100 most recent logs   |

## Running Tests

```bash
pytest tests/
```

## Configuration

Set `DATABASE_URL` in `.env` to point to your remote database:

- **PostgreSQL**: `postgresql://user:password@host:5432/dbname`
- **SQLite (local dev)**: `sqlite:///dev_sentinel.db`