# 🍲 Recipe Management API

A backend **Recipe Management System** built using **FastAPI** and **SQLModel**.
Users can register, log in using **JWT authentication**, and manage their own recipes with full **CRUD functionality** — including optional image uploads — through a clean, well-documented API interface using **Swagger UI**.

This project is designed as an **assignment-grade, production-style backend** to demonstrate clean architecture, authentication, validation, and database integration.

---

## 🚀 Features

### 🔐 Authentication

* User registration and login using **JWT** (access tokens)
* Secure password hashing using **Passlib**
* Protected API endpoints using dependency-based auth
* Token-based access control via Swagger UI

### 🍽️ Recipe Management

* Create, read, update, and delete recipes
* Each recipe belongs to a specific user
* Only the owner can update or delete their recipes
* Fields include:

  * Title
  * Description
  * Ingredients
  * Steps
  * Optional image

### 🖼️ Image Upload (Optional)

* Upload recipe images using multipart/form-data
* Images are stored locally in `/media/recipes/`
* Image path is saved in the database

---

## 🧩 Tech Stack

| Layer                | Technology        |
| -------------------- | ----------------- |
| **Backend**          | FastAPI           |
| **Database**         | SQLite            |
| **ORM**              | SQLModel          |
| **Authentication**   | JWT (python-jose) |
| **Password Hashing** | Passlib (bcrypt)  |
| **API Docs**         | Swagger (OpenAPI) |
| **Server**           | Uvicorn           |

---

## 📁 Folder Structure

```
recipe_api/
│
├── app/
│   ├── main.py
│   │
│   ├── database.py
│   │
│   ├── models.py
│   │
│   ├── auth.py
│   │
│   ├── routers/
│   │   ├──__init__.py
│   │   ├── auth.py
│   │   └── recipes.py
│   │
│   └── config.py
│
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

## 🍽️ Recipe Endpoints

```
POST   /recipes/        → Create recipe (auth required)
GET    /recipes/        → List all recipes
GET    /recipes/{id}    → Get recipe by ID
PUT    /recipes/{id}    → Update recipe (owner only)
DELETE /recipes/{id}    → Delete recipe (owner only)
```

---

## 🧪 What This Project Demonstrates

* Clean FastAPI project structure
* JWT authentication & authorization
* SQLModel-based database modeling
* Ownership-based permissions
* Dependency injection
* File upload handling
* Production-style backend practices

---

## 🏁 Assignment Objective

> To demonstrate understanding of:

* RESTful CRUD APIs
* Models and validation
* Authentication & authorization
* FastAPI architecture
* Database integration

---

## 👨‍💻 Author

**Satyam Jha**

---

## 📜 License

This project is for educational and assignment purposes.

---

If you want, I can:

* Shrink this for **company submission**
* Add **screenshots section**
* Add **API example requests**
* Align wording for **resume / portfolio**

---  

recipe_api/  
│  
├── app/  
│   ├── main.py  
│   │  
│   ├── database.py  
│   │  
│   ├── auth.py  
│   │  
│   ├── models.py  
│   │  
│   ├── routers/  
│   │   ├──__init__.py  
│   │   ├── auth.py  
│   │   └── recipes.py  
│   │  
│   └── config.py  
│  
└── requirements.txt   
