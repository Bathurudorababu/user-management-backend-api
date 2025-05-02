# 🧩 User Management Backend API

This is a backend system for managing users, built using **FastAPI** and **MongoDB**. It was created as part of my journey to enhance my backend development skills by building real-world, production-style authentication APIs.

The project includes features such as user registration, login, logout, and fetching the current logged-in user — all secured with JWT authentication.

---

## 🚀 Tech Stack

- **FastAPI** – High-performance Python web framework  
- **MongoDB** – NoSQL database for flexible document-based storage  
- **Pydantic** – Data validation and schema modeling  
- **JWT** – For stateless user authentication  
- **Swagger UI** – Interactive documentation and testing interface  
- **Mongo Express** – Web-based MongoDB admin interface  
- **Docker** – Containerized environment for FastAPI and MongoDB

---

## ⚙️ Features

- 🔐 **User Authentication APIs**:
  - Register
  - Login
  - Logout
  - Get Current Logged-in User
- ✅ **JWT-based Authentication**
- 🧩 **Modular and Scalable Codebase**
- 🐳 **Dockerized Deployment**
- 🖥️ **MongoDB Admin UI via Mongo Express**

---

## 🛠️ Local Setup Instructions

### 1. Clone the Repository

To begin, clone the repository to your local machine:

```bash
git clone https://github.com/Bathurudorababu/user-management-backend-api.git
cd user-management-backend-api
```

### 2. Build and Run with Docker Compose

Instead of running FastAPI and MongoDB manually, you can use Docker to simplify everything.

Make sure you have **Docker** and **Docker Compose** installed. Then, in the project root directory, run:

```bash
docker-compose up --build -d
```

This command will:
- 🐳 Build the FastAPI Docker image using the `Dockerfile`
- 📦 Launch the following containers:
  - `fastapi-app` on port **8000**
  - `mongodb` on port **27017**
  - `mongo-express` on port **8081**
- 🔁 Run everything in the background using the `-d` (detached) flag

---

### 3. Access the Application

After the containers are up and running, you can access the services using your browser:

- 🚀 **FastAPI Backend**:  
  [http://localhost:8000](http://localhost:8000)

- 📘 **Swagger UI (API Docs)**:  
  [http://localhost:8000/docs](http://localhost:8000/docs)

- 📊 **Mongo Express (MongoDB Admin Panel)**:  
  [http://localhost:8081](http://localhost:8081)

> 🛂 **Login Credentials for Mongo Express:**
> - **Username:** `admin`  
> - **Password:** `pass`

These credentials are defined in the `docker-compose.yml` under the `mongo-express` environment section.

---

### 4. MongoDB Connection in FastAPI

The FastAPI app connects to MongoDB using an internal Docker network hostname (`mongo`) and credentials set in `docker-compose.yml`.

```env
mongodb://admin:secret@mongo:27017
```

In your FastAPI code, make sure to load it like this:

```python
import os
mongo_url = os.getenv("MONGO_URL")
```

This is already configured via the `MONGO_URL` environment variable in `docker-compose.yml`.

---

### 5. Stopping the Containers

To gracefully stop all running containers:

```bash
docker-compose down
```

To also remove images and volumes:

```bash
docker-compose down --volumes --rmi all
```

---

### 6. Rebuild After Code Changes

If you modify your FastAPI code and want those changes to reflect inside the container:

```bash
docker-compose up --build -d
```

This forces Docker to rebuild the FastAPI image with your latest changes.

---

### 7. View Logs (Optional)

To check logs for debugging, especially for the FastAPI app:

```bash
docker-compose logs -f fastapi-app
```

Replace `fastapi-app` with `mongo` or `mongo-express` to see logs for those containers.

---

## ✅ Summary

Your development environment is now fully containerized and ready to go.

- You can test APIs via Swagger UI at `/docs`
- Manage the MongoDB data visually using Mongo Express
- Easily scale or deploy this setup anywhere Docker is supported

---

## 🧪 Want to Run Without Docker?

If you prefer to run the project without Docker:

1. Install MongoDB locally.
2. Change the MongoDB URL in `.env` or inside your code:
   ```env
   mongodb://localhost:27017
   ```
3. Install dependencies and run the server:
   ```bash
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

---

## 📬 Contact

Feel free to open issues or contribute to the repository.

Happy coding! 🚀
