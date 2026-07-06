# 🚀 Vercel Deployment Guide: CDAM LMS Platform

This guide walks you through deploying the Chuka University Center for Data Analytics & Modelling (CDAM) LMS platform to **Vercel** as a serverless Python web application.

---

## ⚠️ Important Production Considerations

Before deploying to Vercel, please note these architecture requirements:

> [!IMPORTANT]
> **Ephemeral Filesystem (No SQLite)**: Vercel serverless containers are stateless and have a read-only filesystem. Any local file database (like SQLite `cdam.db`) will be reset every time the container restarts. You **must** connect to a hosted MySQL or PostgreSQL database for production.
>
> **R Sandbox Limitations on Vercel**: Vercel serverless runtimes do not have the R compiler/interpreter preinstalled. If your production environment requires the interactive R code execution sandbox, you should deploy using a Docker container on platforms like **Render**, **Railway**, or **AWS EC2** instead.

---

## 🛠️ Step 1: Set Up a Hosted Database

You can use any cloud-hosted SQL provider. Below are two free options:

### Option A: Hosted MySQL (Aiven)
1. Sign up for a free tier account at [Aiven.io](https://aiven.io).
2. Create a new **MySQL** service.
3. Once active, copy the **Service URI**. It will look similar to:
   `mysql://avnadmin:password@mysql-instance.aivencloud.com:port/defaultdb`

### Option B: Hosted PostgreSQL (Neon / Supabase)
1. Sign up for a free account at [Neon.tech](https://neon.tech) or [Supabase.com](https://supabase.com).
2. Create a new project database.
3. Copy the connection string. It will look similar to:
   `postgresql://user:password@ep-cool-pool-12345.us-east-2.aws.neon.tech/neondb?sslmode=require`

---

## 🔑 Step 2: Configure Environment Variables

Vercel will inject these variables into your app securely at runtime:

| Variable | Description | Example / Recommended Value |
| :--- | :--- | :--- |
| `DATABASE_URL` | Your hosted database connection string | `mysql://avnadmin:pass@mysql-instance.com/db` |
| `SECRET_KEY` | Flask session encryptor key | A random string (e.g. `c0ffeeface991122334455`) |
| `GEMINI_API_KEY` | Google Generative AI key for practice quiz generation | Get one from [Google AI Studio](https://aistudio.google.com/) |

---

## 🚀 Step 3: Deploy to Vercel

### 1. Push to GitHub
Ensure all your files are pushed to your GitHub repository:
```bash
git add .
git commit -m "Prepare codebase for Vercel deployment"
git push origin main
```

### 2. Import to Vercel
1. Log in to [Vercel](https://vercel.com).
2. Click **Add New** -> **Project**.
3. Select your GitHub repository (`Python-CDAM-system`) and click **Import**.

### 3. Configure Build & Environment Settings
1. **Framework Preset**: Leave as `Other` (Vercel will auto-detect the configuration from `vercel.json`).
2. **Root Directory**: Leave as `./` (Project Root).
3. Expand **Environment Variables** and add the variables defined in Step 2:
   - `DATABASE_URL`
   - `SECRET_KEY`
   - `GEMINI_API_KEY`

### 4. Deploy!
Click **Deploy**. Vercel will build the serverless functions, link the static assets directory, and deploy the application. Once complete, you will receive a public `.vercel.app` URL.

---

## 🔧 Database Migration & Seeding on First Launch
The application is configured to run database schema setup and automatic curriculum seeding (including R/Python sessions and default admin accounts) automatically on startup (during import of `backend/app.py`).

Once the deployment completes and you open the site:
* The tables will be auto-migrated on your hosted database.
* The 9-session R syllabus and Python tracks will be populated.
* You can log in using the default administrator account:
  * **Email**: `admin@cdam.local`
  * **Password**: `admin123` *(Be sure to change this password in the profile section after first login!)*
