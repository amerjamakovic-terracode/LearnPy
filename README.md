# LoginPy – Learning Authentication with FastAPI & PostgreSQL

This is a **learning project** to understand how authentication, tokens, and databases work together.
The project provides a simple backend with:

* User registration (create account)
* Login with password hashing
* JWT-based authentication
* PostgreSQL database integration

---

## Features

* **User model** with fields:

  * `id` (primary key, auto increment)
  * `first_name`
  * `last_name`
  * `email` (unique)
  * `password` (hashed)
  * `active` (boolean, default `true`)
  * `created_at` (datetime, auto set)
  * `modified_at` (datetime, auto updated)

* **Endpoints**:

  * `POST /register` – create a new user
  * `POST /login` – log in and get JWT token
  * `GET /me` – retrieve current user from token

---

## Tech Stack

* [FastAPI](https://fastapi.tiangolo.com/) – backend API framework
* [PostgreSQL](https://www.postgresql.org/) – database
* [SQLAlchemy](https://www.sqlalchemy.org/) – ORM for models
* [Alembic](https://alembic.sqlalchemy.org/) – migrations
* [Passlib](https://passlib.readthedocs.io/en/stable/) – password hashing (bcrypt)
* [python-jose](https://python-jose.readthedocs.io/en/latest/) – JWT tokens
* [python-dotenv](https://pypi.org/project/python-dotenv/) – environment variables

---

## Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd LoginPy
```

### 2. Create a virtual environment

```bash
uv venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
# With uv
uv pip install -r requirements.txt

# Or with pip
pip install -r requirements.txt

```

### 4. Setup PostgreSQL

Create a database and user in PostgreSQL, for example:

```sql
CREATE DATABASE loginpy;
CREATE USER loginpy_user WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE loginpy TO loginpy_user;
```

### 5. Environment variables

Create a `.env` file in the root of the project:

```
DATABASE_URL=postgresql+asyncpg://loginpy_user:yourpassword@localhost/loginpy
SECRET_KEY=supersecretkey123
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 6. Run migrations

```bash
alembic upgrade head
```

### 7. Start the app

```bash
uvicorn main:app --reload
```

---

## Learning Goals

* Understand how FastAPI handles request/response.
* Learn how JWT tokens work for authentication.
* Learn password hashing with bcrypt.
* Connect and manage a PostgreSQL database with SQLAlchemy & Alembic.

---

