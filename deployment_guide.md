# Deployment Guide

Follow these steps to deploy **LAWkeash BOT** for free using **Render** (Backend) and **Vercel** (Frontend).

## Prerequisites

1.  **GitHub Account**: You need to push your code to a GitHub repository.
2.  **Render Account**: Sign up at [render.com](https://render.com).
3.  **Vercel Account**: Sign up at [vercel.com](https://vercel.com).

---

## Part 1: Push Code to GitHub

1.  Initialize git if you haven't:
    ```bash
    git init
    git add .
    git commit -m "Initial commit"
    ```
2.  Create a new repository on GitHub.
3.  Push your code:
    ```bash
    git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
    git branch -M main
    git push -u origin main
    ```

---

## Part 2: Deploy Backend (Render)

1.  **Create New Web Service**:
    - Go to Render Dashboard > New > **Web Service**.
    - Connect your GitHub repository.

2.  **Configure Service**:
    - **Name**: `lawkeash-backend` (or similar)
    - **Region**: Choose the one closest to you (e.g., Singapore/Frankfurt).
    - **Branch**: `main`
    - **Root Directory**: `.` (leave empty or dot)
    - **Runtime**: **Python 3**
    - **Build Command**: `pip install -r requirements.txt`
    - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port 10000`
    - **Plan**: **Free**

3.  **Environment Variables**:
    - Scroll down to "Environment Variables" and add:
        - `Key`: `PYTHON_VERSION` | `Value`: `3.10` (or `3.11`)
        - `Key`: `GEMINI_API_KEY` | `Value`: `your_actual_api_key_here`

4.  **Deploy**:
    - Click **Create Web Service**.
    - Wait for the deployment to finish. It will give you a URL like `https://lawkeash-backend.onrender.com`. **Copy this URL.**

---

## Part 3: Deploy Frontend (Vercel)

1.  **Import Project**:
    - Go to Vercel Dashboard > **Add New...** > **Project**.
    - Select your GitHub repository.

2.  **Configure Project**:
    - **Framework Preset**: Next.js (should detect automatically).
    - **Root Directory**: Click "Edit" and select `frontend`. **Important!**

3.  **Environment Variables**:
    - Expand "Environment Variables".
    - Add:
        - `Key`: `BACKEND_URL`
        - `Value`: `https://lawkeash-backend.onrender.com` (The URL from Render, **without** the trailing slash).

4.  **Deploy**:
    - Click **Deploy**.
    - Wait for the build to complete.

---

## Part 4: Final Verification

1.  Open your Vercel deployment URL (e.g., `https://lawkeash-frontend.vercel.app`).
2.  Type a message in the chat.
3.  Ensure the bot responds. If it works, your deployment is successful!

---

## Troubleshooting

-   **Backend Error**: Check Render logs. If it says "ModuleNotFound", ensure `requirements.txt` is updated and pushed.
-   **Frontend Error**: If the chat says "Failed to communicate", check the `BACKEND_URL` variable in Vercel settings. It must match your Render URL exactly.
