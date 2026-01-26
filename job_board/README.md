# 💼 Job Board Platform API

A backend **Job Board Platform** built using **FastAPI** and **SQLModel**.  
Users can register and log in using **JWT authentication**. Recruiters can create and manage **companies** and **job postings**, while job seekers can browse jobs using **search, filters, tags, and pagination** — all through a clean, well-documented API using **Swagger UI**.

---

## 🚀 Features

### 🔐 Authentication & Authorization

* User registration and login using **JWT** (access tokens)
* Secure password hashing using **Passlib**
* Role-based access control:
  * **Recruiter**: Can create companies and manage jobs
  * **Normal User**: Can only browse jobs
* Protected API endpoints using dependency-based auth
* Token-based access control via Swagger UI

---

### 🏢 Company Management

* Recruiters can:
  * Create companies
  * Update their own companies
  * Delete their own companies
* Each company is owned by a recruiter user
* Ownership is enforced at API level

---

### 💼 Job Management

* Recruiters can:
  * Create, update, delete jobs for their own companies
* Each job:
  * Belongs to a company
  * Is owned indirectly by the recruiter who owns the company
* Only the owner recruiter can modify or delete jobs

---

### 🔎 Job Browsing & Search

Public job listing endpoint with:

* Search by:
  * Title
  * Keywords
  * Location
* Filter by:
  * Company
  * Tags
* Tag-based search (many-to-many)
* Pagination support:
  * `page`
  * `limit`
* Returns metadata:
  * Total count
  * Current page
  * Items

---

### 🏷️ Tag System

* Jobs can have multiple tags
* Tags are:
  * Auto-created if not present
  * Reused across jobs
* Many-to-many relationship between Jobs and Tags

---

## 🧩 Tech Stack

| Layer                | Technology        |
| -------------------- | ----------------- |
| **Backend**          | FastAPI           |
| **Database**         | SQLite (default) / PostgreSQL (optional) |
| **ORM**              | SQLModel          |
| **Authentication**   | JWT (python-jose) |
| **Password Hashing** | Passlib (bcrypt)  |
| **API Docs**         | Swagger (OpenAPI) |
| **Server**           | Uvicorn           |
| **Containerization** | Docker, Docker Compose |

---

## 📁 Folder Structure

```
job_board/
│
├── app/
│ ├── main.py
│ │
│ ├── database.py
│ │
│ ├── models.py
│ │
│ ├── schemas.py
│ │
│ ├── schemas/
│ │ ├── user.py
│ │ ├── company.py
│ │ └── job.py
│ │
│ ├── core/
│ │ ├── security.py
│ │ └── dependency.py
│ │
│ ├── routers/
│ │ ├── auth.py
│ │ ├── company.py
│ │ └── jobs.py
│ │
│ └── config.py
│
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```


---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone <your-repo-url>
cd recipe_api
```

### 2️⃣ Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate # Linux/Mac
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

Or:

```bash
pip install fastapi uvicorn sqlmodel python-jose passlib[bcrypt] python-multipart
```

---

## ▶️ Run the Server

```bash
uvicorn app.main:app --reload
```

Server will start at:

```
http://127.0.0.1:8000
```

---

## 📚 API Documentation

* Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## 🔐 Authentication Flow

1. Register:

```
POST /auth/register
```

2. Login:

```
POST /auth/login
```

3. Click **Authorize** in Swagger and enter:

```
Bearer <your_token>
```

4. Now you can access protected routes.

---

## 🏢 Company Endpoints
```
POST   /companies/        → Create company (recruiter only)
GET    /companies/        → List companies
GET    /companies/{id}    → Get company by ID
PUT    /companies/{id}    → Update company (owner only)
DELETE /companies/{id}    → Delete company (owner only)
```

## 💼 Job Endpoints
```
POST   /jobs/             → Create job (recruiter only, own company)
GET    /jobs/             → List jobs (public, supports filters)
GET    /jobs/{id}         → Get job by ID
PUT    /jobs/{id}         → Update job (owner only)
DELETE /jobs/{id}         → Delete job (owner only)
```
