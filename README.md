# **🐦 Twitter Clone (Flask + React) - Dockerized**

A **Twitter-like social media app** built with **Flask (backend) and React (frontend)**, fully containerized with **Docker** for easy deployment and setup.

---

## **🚀 Features**
- ✅ User authentication (register, login, logout)
- ✅ Post, edit, and delete tweets
- ✅ View and search user profiles
- ✅ Fetch all tweets on the homepage
- ✅ Fully containerized with **Docker** for easy setup

---

## **📦 Installation & Setup**

### **1️⃣ Prerequisites**
Make sure you have **Docker** and **Docker Compose** installed.

🔹 **Check if Docker is installed:**

```
docker --version
docker-compose --version
```

If not installed, download it from [Docker's official website](https://www.docker.com/products/docker-desktop).

---

### **2️⃣ Clone the Repository**

```
git clone https://github.com/Faiaaz/twitter-clone.git
cd twitter-clone
```

---

### **3️⃣ Build and Run the Project**
Run the following command to **build and start the containers**:

```
docker-compose up --build
```

This will:
- Start the **Flask backend** at `http://localhost:5000`
- Start the **React frontend** at `http://localhost:3000`

---

### **4️⃣ Access the Application**
📌 **Frontend (React)** → Open **[`http://localhost:3000`](http://localhost:3000)**  
📌 **Backend (Flask API)** → Open **[`http://localhost:5000/api/tweets`](http://localhost:5000/api/tweets)**

---

## **🛠️ Useful Docker Commands**

🛑 **Stop the containers:**

```
docker-compose down
```

♻️ **Rebuild containers (if needed):**

```
docker-compose up --build
```

📋 **View running containers:**

```
docker ps
```

🔍 **Check logs for errors:**

```
docker logs twitter-clone-backend-1
docker logs twitter-clone-frontend-1
```

---

## **💡 Tech Stack**
- **Backend**: Flask, Flask-Login, Flask-SQLAlchemy, Flask-CORS  
- **Frontend**: React, React Router  
- **Database**: SQLite (can be extended to PostgreSQL)  
- **Containerization**: Docker & Docker Compose  

---

## **🛠️ Next Steps & Improvements**
📌 **Future Features:**
- Add likes & comments on tweets
- Add user follow option
- Improve UI/UX with Tailwind CSS or Material UI


---

### **🚀  Anyone Can Run this Project Easily!**

