# FastAPI Inventory Project

A full-stack inventory management app with a **FastAPI** backend deployed on **Azure Container Apps**, a **React** frontend deployed on **Vercel**, and a **Supabase (PostgreSQL)** database.

---

## 🏗️ Architecture

```
React Frontend (Vercel)
        │
        │  REST API calls (HTTPS)
        ▼
FastAPI Backend (Azure Container Apps)
        │
        │  psycopg / SQLAlchemy (SSL)
        ▼
Supabase PostgreSQL Database
```

- **Backend image** is built locally and pushed to **Azure Container Registry (ACR)**, then deployed as an **Azure Container App**.
- **Database** is a managed **Supabase PostgreSQL** instance (connected via its ORM/connection string).
- **Frontend** is a React app deployed on **Vercel**, configured with the backend's Azure URL as its API base.

---

## 🧰 Tech Stack

| Layer      | Technology                          |
|------------|--------------------------------------|
| Frontend   | React, deployed on Vercel            |
| Backend    | FastAPI, containerized with Docker   |
| Registry   | Azure Container Registry (ACR)       |
| Hosting    | Azure Container Apps                 |
| Database   | Supabase (PostgreSQL)                |

---

## 🚀 Deployment Guide

### 1. Create a Resource Group in Azure

Created a resource group in the Azure Portal to hold all project resources.

![image alt](1a Create a RG.png)

---

### 2. Create Azure Container Registry (ACR)

Created an ACR instance to store the backend Docker image.

![image alt](1b Create ACR.png)

---

### 3. Copy ACR Access Keys

Enabled the admin user on the ACR and copied the login server, username, and password from **Access keys**.

![image alt](1c Copy ACR Access Keys.png)

---

### 4. Log in to ACR from Docker

Authenticated Docker locally against the ACR using the copied credentials.

```bash
docker login <acr-login-server>
```

![image alt](1d Login to Azure ACR.png)

---

### 5. Build and Push the Backend Image (linux/amd64)

Built the backend image for the `linux/amd64` platform (required for Azure Container Apps) and pushed it to ACR.

```bash
docker buildx build --platform linux/amd64 -t <acr-login-server>/fastapi-backend:v1 .
docker push <acr-login-server>/fastapi-backend:v1
```

![image alt](1e Build and Push the backend docker image amd64 to the ACR.png)

---

### 6. Configure Environment Variables on the Container App

Set the backend's environment variables (e.g. `DATABASE_URL`, `CORS_ORIGINS`) in the Azure Container App configuration.

![image alt](1h Env Setup.png)

---

### 7. Configure Ingress

Enabled external ingress on the backend Container App and set the target port to match the app (e.g. `8000`).

![image alt](1i Ingress Setup.png)

---

### 8. Set Up the Database on Supabase

Created the project tables on Supabase.

![image alt](1j Tables were created on supabase for database.png)

---

### 9. Copy the Supabase Connection URL

Copied the ORM connection string from Supabase to use as the backend's `DATABASE_URL`.

![image alt](k Connection Url copied from supabase-ORM connection.png)

---

### 10. Replace Dummy Env Values with Real Values

Updated the placeholder/dummy environment variable values in the Azure Container App with the real Supabase connection string and other config.

![image alt](1l Env values in azure container apps were replaced with previous dummy values.png)

---

### 11. Backend Successfully Deployed

Verified the backend Container App was up and reachable at its Azure-provided URL.

![image alt](2a Backend is Successully Deployed.png)

---

### 12. Locate the Backend URL for the Frontend Env Var

Found the backend's Application URL to use as the API base URL for the frontend.

![image alt](2b Finding the Env name for the backend to frontend connection.png)

---

### 13. Deploy the Frontend on Vercel

Deployed the React frontend on Vercel, setting the backend Azure URL as an environment variable (e.g. `REACT_APP_API_BASE_URL`).

![image alt](2c Deploying the frontend on vercel with env of the backend-url-azure.png)

---

### 14. Frontend Deployed and Fetching Data

Confirmed the frontend loads and successfully displays products fetched from the Azure-hosted backend.

![image alt](2d Frontend is Deployed and is showing products from the backend.png)

---

## ✅ End-to-End Verification

### Adding a Product via the Vercel Frontend

![image alt](6a Adding products via vercel frontend.png)

### Product Added Successfully

![image alt](6b Product is added successfully.png)

### Database Reflects the New Product

![image alt](6c Database is updated as well.png)

---

## 🔑 Environment Variables

**Backend (Azure Container App):**

| Variable        | Description                                              |
|------------------|-----------------------------------------------------------|
| `DATABASE_URL`   | Supabase PostgreSQL connection string (`postgresql+psycopg://...?sslmode=require`) |
| `CORS_ORIGINS`   | Allowed frontend origin(s), e.g. the Vercel deployment URL |

**Frontend (Vercel):**

| Variable                   | Description                          |
|------------------------------|---------------------------------------|
| `REACT_APP_API_BASE_URL`   | Base URL of the deployed Azure backend |

---

## 📌 Notes

- Backend images must be built for `linux/amd64` when pushing from an Apple Silicon (M-series) Mac, since Azure Container Apps runs on `amd64`.
- CORS on the backend must exactly match the frontend's deployed URL (including `https://`) or requests from the frontend will be blocked.
- The database was ultimately hosted on **Supabase** rather than Azure Database for PostgreSQL, while the backend remained on Azure Container Apps.

---
