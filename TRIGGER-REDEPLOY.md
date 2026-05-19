# Trigger Manual Redeploy on Render

## 🔄 How to Manually Redeploy

### Option 1: Via Render Dashboard (Recommended)

1. **Go to**: https://dashboard.render.com/
2. **Click on**: `growfund-backend` service
3. **Click**: "Manual Deploy" button (top right corner)
4. **Select**: "Clear build cache & deploy"
5. **Click**: "Deploy"

This will force a fresh deployment with the latest code.

---

### Option 2: Make a Small Change and Push

If you want to trigger auto-deploy:

```bash
# Make a small change (add a comment)
echo "# Trigger redeploy" >> backend-growfund/README.md

# Commit and push
git add .
git commit -m "Trigger redeploy"
git push origin main
```

---

### Option 3: Via Render API (Advanced)

If you have a Render API key:

```bash
curl -X POST https://api.render.com/v1/services/YOUR_SERVICE_ID/deploys \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json"
```

---

## 📊 What to Monitor

After triggering redeploy, watch the logs for:

### Build Phase:
```
==> Building...
Successfully installed Django-4.2.7 ...
160 static files copied
==> Build successful 🎉
```

### Deploy Phase (THIS IS WHAT YOU WANT TO SEE):
```
==> Deploying...
🔄 Running database migrations...
Operations to perform:
  Apply all migrations: accounts, admin, auth, ...
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying accounts.0001_initial... OK
  Applying accounts.0002_referral... OK
  Applying accounts.0003_auto_verify_users... OK
  ... (many more)
  Applying transactions.0001_initial... OK
  Applying binary_trading.0001_initial... OK
⚙️ Setting up platform settings...
Platform settings initialized successfully
💰 Setting up crypto prices...
Crypto prices initialized successfully
🚀 Starting Gunicorn server...
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:10000
==> Your service is live 🎉
```

---

## ✅ Success Checklist

After redeploy completes:

- [ ] Logs show "🔄 Running database migrations..."
- [ ] Logs show "Applying accounts.0001_initial... OK"
- [ ] Logs show "Platform settings initialized successfully"
- [ ] Logs show "Your service is live 🎉"
- [ ] Health endpoint works: `curl https://growfund-backend.onrender.com/api/health/`
- [ ] Register endpoint returns 201 (not 500)
- [ ] Login endpoint returns 200 (not 500)

---

## 🧪 Test After Redeploy

### 1. Health Check
```bash
curl https://growfund-backend.onrender.com/api/health/
```
**Expected**: `{"status":"ok"}`

### 2. Register User
```bash
curl -X POST https://growfund-backend.onrender.com/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "password": "securepass123",
    "full_name": "New User"
  }'
```
**Expected**: 201 Created (NOT 500!)

### 3. Login
```bash
curl -X POST https://growfund-backend.onrender.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "password": "securepass123"
  }'
```
**Expected**: 200 OK with JWT tokens

---

## 🔍 If Migrations Still Don't Run

If you still don't see migration messages in logs:

### Check Environment Variables:
1. Go to Render Dashboard → Your Service → Environment
2. Verify `DATABASE_URL` is set
3. Verify `SECRET_KEY` is set

### Check Dockerfile:
The entrypoint script should be created during build:
```dockerfile
RUN echo '#!/bin/bash
python manage.py migrate --noinput
...' > /app/entrypoint.sh
```

### Check Logs for Errors:
Look for:
- Database connection errors
- Permission errors
- Python tracebacks

---

## 🚨 Emergency Fix

If nothing works, you can run migrations manually via Render Shell:

1. Go to Render Dashboard → Your Service → Shell
2. Run:
```bash
cd /app
python manage.py migrate
python manage.py setup_platform_settings
python manage.py setup_crypto_prices
```

Then restart the service.

---

## 📞 Current Status

- ✅ Code is pushed to GitHub
- ✅ Dockerfile is fixed with bash entrypoint
- ✅ Environment variables should be set
- 🔄 Waiting for manual redeploy trigger

**Next Step**: Go to Render Dashboard and click "Manual Deploy"!
