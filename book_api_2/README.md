# 📚 Book Management API (FastAPI)

A **production-style backend API** built using **FastAPI**, **SQLModel**, and **SQLite**.

This project supports:

* ✅ Secure Book CRUD operations
* ✅ User registration & login (JWT Authentication)
* ✅ Request logging middleware
* ✅ Automated tests with Pytest

---

## 🚀 Features

* 🔐 JWT-based authentication
* 📚 Book CRUD (Create, Read, Update, Delete)
* 👤 User registration & login
* 🛡️ Protected routes for write operations
* 🗃️ SQLite database using SQLModel ORM
* 🧾 Logging middleware:

  * Logs request path
  * HTTP method
  * Status code
  * Execution time
* 🧪 Full test coverage using pytest
* 📖 Interactive API docs using Swagger UI

---

## 🗂️ Project Structure

```
book_api/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   │
│   ├── models.py
│   │
│   ├── schemas.py
│   │
│   ├── routers/
│   │   ├── users.py
│   │   └── books.py
│   │
│   ├── auth.py
│   │
│   └── tests/
│        ├── __init__.py
│        ├── utils.py
│        ├── test_books.py
│        └── conftest.py
│
├── .env
├── requirements.txt
└── README.md
```

---

## ⚙️ Tech Stack

* FastAPI
* SQLModel
* SQLite
* PyJWT / python-jose
* Passlib (password hashing)
* Pytest
* Uvicorn

---

## 📦 Installation

```bash
git clone <your-repo-url>
cd book_api

python -m venv venv
venv\Scripts\activate   # Windows

pip install -r requirements.txt
```

---

## ▶️ Run Server

From project root:

```bash
uvicorn app.main:app --reload
```

Open:

```
http://127.0.0.1:8000/docs
```

---

## 🧾 Middleware Logging

Every request logs:

* Method
* Path
* Status code
* Execution time

Example:

```
GET /books/1 | Status: 200 | Time: 0.0023s
```

---

## 🔑 Authentication Flow

### 1️⃣ Register (Public)

```
POST /auth/register
```

```json
{
  "username": "your_username",
  "password": "######"
}
```

---

### 2️⃣ Login (Public)

```
POST /auth/login
```

```
username = your_username
password = ######
```

Response:

```json
{
  "access_token": "...",
  "token_type": "bearer"
}
```

---

## 📚 Book API Endpoints

### 🌍 Public

* `GET /books`
* `GET /books/{id}`
* `GET /books?author=...`
* `GET /books?title=...`

---

### 🔐 Protected (JWT required)

* `POST /books`
* `PUT /books/{id}`
* `DELETE /books/{id}`

---

## 🧪 Running Tests

```bash
pytest
```

Test coverage includes:

* ✅ Auth registration & login
* ✅ JWT protection
* ✅ Book CRUD
* ✅ Unauthorized access checks
* ✅ Database isolation using test DB
