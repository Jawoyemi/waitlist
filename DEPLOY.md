# Unibuy Waitlist Backend - Deployment Guide (Render)

## 1. Create a Database first

1. Log in to [Render Dashboard](https://dashboard.render.com).
2. Click **New +** -> **PostgreSQL**.
3. Name it `unibuy-db`.
4. Choose the **Free** plan.
5. Click **Create Database**.
6. Wait for it to be created.
7. **Copy the "Internal Database URL"** (starts with `postgres://...`). You will need this in a moment.

## 2. Create the Web Service

1. Go back to Dashboard.
2. Click **New +** -> **Web Service**.
3. Select "Build and deploy from a Git repository".
4. Connect your valid GitHub repo: `Jawoyemi/waitlist`.
5. Name it `unibuy-backend`.
6. **Region**: Choose one close to you (e.g., Frankfurt/London).
7. **Branch**: `master`
8. **Runtime**: Python 3
9. **Build Command**: `pip install -r requirements.txt`
10. **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 10000`
11. **Plan**: Free

## 3. Environment Variables (Critical!)

Scroll down to "Environment Variables" and click **Add Environment Variable**. Add all of these:

| Key               | Value                                                       |
| ----------------- | ----------------------------------------------------------- |
| `DATABASE_URL`    | Paste the **Internal Database URL** you copied in Step 1.   |
| `MAIL_USERNAME`   | `campuscart67@gmail.com`                                    |
| `MAIL_PASSWORD`   | `your_16_char_app_password` (Get this from your local .env) |
| `MAIL_FROM`       | `jedidiahawoyemi@gmail.com`                                 |
| `MAIL_PORT`       | `587`                                                       |
| `MAIL_SERVER`     | `smtp.gmail.com`                                            |
| `ADMIN_EMAIL`     | `jedidiahawoyemi@gmail.com`                                 |
| `ADMIN_SECRET`    | `your_secret_key` (Get this from your local .env)           |
| `ALLOWED_ORIGINS` | `https://uni-buy.vercel.app`                                |
| `PYTHON_VERSION`  | `3.11.5` (Optional, helps avoid version issues)             |

## 4. Deploy

1. Click **Create Web Service**.
2. Wait for the logs to say "Application startup complete".
3. **Copy your new Backend URL** from the top left (e.g., `https://unibuy-backend.onrender.com`).

## 5. Connect Frontend

1. Go to your frontend project code.
2. Update the API call URL:
   - Change `http://127.0.0.1:8000/join`
   - To `https://unibuy-backend.onrender.com/join`
3. Redeploy your frontend to Vercel.

**Done!** 🚀
