# 🧩 User Management Backend API

This project is a backend system for managing users , built using **FastAPI**, **MongoDB**, and **PostgreSQL/PostGIS**, and containerized with **Docker**. It replicates a real-world backend system inspired by my experience at **Avihs Technologies**.

---

## 🚀 Tech Stack

- **FastAPI** – API framework for Python
- **PostgreSQL + PostGIS** – For relational and geospatial data
- **MongoDB** – For flexible document-based storage
- **Docker** – For containerized, reproducible development
- **Postman** – For endpoint testing
- **Pydantic** – For data validation and schema definition

---

## ⚙️ Features

- 🔐 **User Management** – Register, login, JWT-based auth
- ✅ **RESTful Endpoints** – Built with FastAPI's modular routing
- 🐳 **Dockerized** – Simple local development using Docker Compose

---

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/Bathurudorababu/user-management-backend-api.git
cd user-property-backend-api

# (Optional) create and activate virtualenv
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the API
uvicorn main:app --reload
