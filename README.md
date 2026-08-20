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

![image alt](https://github.com/Dpk808/FastAPI-on-Azure-Supabase-Database/blob/main/FastAPI%20Screenshots/1a%20Create%20a%20RG.png)

---

### 2. Create Azure Container Registry (ACR)

Created an ACR instance to store the backend Docker image.

![image alt](https://github.com/Dpk808/FastAPI-on-Azure-Supabase-Database/blob/main/FastAPI%20Screenshots/1b%20Create%20ACR.png)

---

### 3. Copy ACR Access Keys

Enabled the admin user on the ACR and copied the login server, username, and password from **Access keys**.

![image alt](https://github.com/Dpk808/FastAPI-on-Azure-Supabase-Database/blob/main/FastAPI%20Screenshots/1c%20Copy%20ACR%20Access%20Keys.png)

---

### 4. Log in to ACR from Docker

Authenticated Docker locally against the ACR using the copied credentials.

```bash
docker login <acr-login-server>
```

![image alt](https://github.com/Dpk808/FastAPI-on-Azure-Supabase-Database/blob/main/FastAPI%20Screenshots/1d%20Login%20to%20Azure%20ACR.png)

---

### 5. Build and Push the Backend Image (linux/amd64)

Built the backend image for the `linux/amd64` platform (required for Azure Container Apps) and pushed it to ACR.

```bash
docker buildx build --platform linux/amd64 -t <acr-login-server>/fastapi-backend:v1 .
docker push <acr-login-server>/fastapi-backend:v1
```

![image alt](https://github.com/Dpk808/FastAPI-on-Azure-Supabase-Database/blob/main/FastAPI%20Screenshots/1e%20Build%20and%20Push%20the%20backend%20docker%20image%20amd64%20to%20the%20ACR.png)

---

### 6. Configure Environment Variables on the Container App

Set the backend's environment variables (e.g. `DATABASE_URL`, `CORS_ORIGINS`) in the Azure Container App configuration.

![image alt](https://github.com/Dpk808/FastAPI-on-Azure-Supabase-Database/blob/main/FastAPI%20Screenshots/1h%20Env%20Setup.png)

---

### 7. Configure Ingress

Enabled external ingress on the backend Container App and set the target port to match the app (e.g. `8000`).

![image alt](https://github.com/Dpk808/FastAPI-on-Azure-Supabase-Database/blob/main/FastAPI%20Screenshots/1i%20Ingress%20Setup.png)

---

### 8. Set Up the Database on Supabase

Created the project tables on Supabase.

![image alt](https://github.com/Dpk808/FastAPI-on-Azure-Supabase-Database/blob/main/FastAPI%20Screenshots/1j%20Tables%20were%20created%20on%20supabse%20for%20database.png)

---

### 9. Copy the Supabase Connection URL

Copied the ORM connection string from Supabase to use as the backend's `DATABASE_URL`.

![image alt](https://github.com/Dpk808/FastAPI-on-Azure-Supabase-Database/blob/main/FastAPI%20Screenshots/1k%20Connection%20Url%20copied%20from%20supabase-ORM%20sonnection.png)

---

### 10. Replace Dummy Env Values with Real Values

Updated the placeholder/dummy environment variable values in the Azure Container App with the real Supabase connection string and other config.

![image alt](https://github.com/Dpk808/FastAPI-on-Azure-Supabase-Database/blob/main/FastAPI%20Screenshots/1l%20Env%20values%20in%20azure%20container%20apps%20were%20replaced%20with%20previous%20dummy%20values.png)

---

### 11. Backend Successfully Deployed

Verified the backend Container App was up and reachable at its Azure-provided URL.

![image alt](https://github.com/Dpk808/FastAPI-on-Azure-Supabase-Database/blob/main/FastAPI%20Screenshots/2a%20Backend%20is%20Successully%20Deployed.png)

---

### 12. Locate the Backend URL for the Frontend Env Var

Found the backend's Application URL to use as the API base URL for the frontend.

![image alt](https://github.com/Dpk808/FastAPI-on-Azure-Supabase-Database/blob/main/FastAPI%20Screenshots/2b%20Finding%20the%20Env%20name%20for%20the%20backend%20to%20frontend%20connection.png)

---

### 13. Deploy the Frontend on Vercel

Deployed the React frontend on Vercel, setting the backend Azure URL as an environment variable (e.g. `REACT_APP_API_BASE_URL`).

![image alt](https://github.com/Dpk808/FastAPI-on-Azure-Supabase-Database/blob/main/FastAPI%20Screenshots/2c%20Deploying%20the%20frontend%20on%20vercel%20with%20env%20of%20the%20backend-url-azure.png)

---

### 14. Frontend Deployed and Fetching Data

Confirmed the frontend loads and successfully displays products fetched from the Azure-hosted backend.

![image alt](https://github.com/Dpk808/FastAPI-on-Azure-Supabase-Database/blob/main/FastAPI%20Screenshots/2d%20Frontend%20is%20Deployed%20and%20is%20showing%20products%20from%20the%20backend.png)

---

## ✅ End-to-End Verification

### Adding a Product via the Vercel Frontend

![image alt](https://github.com/Dpk808/FastAPI-on-Azure-Supabase-Database/blob/main/FastAPI%20Screenshots/6a%20Adding%20products%20via%20vercel%20frontend.png)

### Product Added Successfully

![image alt](https://github.com/Dpk808/FastAPI-on-Azure-Supabase-Database/blob/main/FastAPI%20Screenshots/6b%20Product%20is%20added%20successfully.png)

### Database Reflects the New Product

![image alt](https://github.com/Dpk808/FastAPI-on-Azure-Supabase-Database/blob/main/FastAPI%20Screenshots/6c%20Database%20is%20updated%20as%20well.png)

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
