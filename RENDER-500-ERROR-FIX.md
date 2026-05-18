# Fix: 500 Internal Server Error on Render

## ❌ The Problem

Login and registration endpoints are returning **500 Internal Server Error**:
```
POST https://growfund-backend.onrender.com/api/auth/login/ 500
POST https://growfund-backend.onrender.com/api/auth/register/ 500
```

## 🔍 Root Cause

The database migrations likely didn't run during deployment. This means:
- Database tables don't exist
- User model can't be accessed
- All database operations fail with 500 errors

## ✅ Solution: Run Migrations Manually

### Option 1: Use Render Shell (Recommended)

1. **Go to Render Dashboard**: https://dashboard.render.com/
2. **Select your service**: `growfund-backend`
3. **Click on "Shell" tab** (left sidebar)
4. **Run these commands**:

```bash
cd /app
python manage.py migrate
python manage.py setup_platform_settings
python manage.py setup_crypto_prices
```

### Option 2: Use the Migration API Endpoint

Since you're an admin, you can trigger migrations via the API:

1. **First, create an admin user via Shell**:
```bash
cd /app
python create_tabby_admin.py
```

2. **Login as admin** and get your JWT token

3. **Call the migration endpoint**:
```bash
curl -X POST https://growfund-backend.onrender.com/api/admin/run-migrations/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Option 3: Redeploy with Manual Deploy

1. Go to Render Dashboard → Your Service
2. Click **Manual Deploy** → **Deploy latest commit**
3. Watch the logs to ensure migrations run

---

## 🔍 Check if Migrations Ran

### Via Render Logs

1. Go to Render Dashboard → Your Service → **Logs** tab
2. Look for these messages:
```
🔄 Running database migrations...
Operations to perform:
  Apply all migrations: accounts, admin, auth, ...
Running migrations:
  Applying accounts.0001_initial... OK
  Applying transactions.0001_initial... OK
  ...
⚙️ Setting up platform settings...
💰 Setting up crypto prices...
🚀 Starting Gunicorn server...
```

### Via API (After Creating Admin)

```bash
curl https://growfund-backend.onrender.com/api/admin/db-check/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## 🐛 Why Migrations Didn't Run

### Possible Causes:

1. **Docker CMD Issue**: The `start.sh` script might not be executing
2. **Database Connection**: Database wasn't accessible during startup
3. **Build vs Runtime**: Migrations tried to run during build phase

### Check Render Configuration:

1. Go to Render Dashboard → Your Service → **Settings**
2. Verify:
   - **Build Command**: Should be empty (Docker handles it)
   - **Start Command**: Should be empty (Dockerfile CMD handles it)
   - **Dockerfile Path**: Should be `backend-growfund/Dockerfile`

---

## 📝 Expected Behavior After Fix

Once migrations run successfully:

### ✅ Login Should Work:
```bash
curl -X POST https://growfund-backend.onrender.com/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123","full_name":"Test User"}'
```
**Expected**: 201 Created with user data

### ✅ Register Should Work:
```bash
curl -X POST https://growfund-backend.onrender.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123"}'
```
**Expected**: 200 OK with JWT tokens

---

## 🔧 Quick Fix Steps

1. **Go to Render Shell**
2. **Run migrations**:
   ```bash
   cd /app
   python manage.py migrate
   ```
3. **Create admin user**:
   ```bash
   python create_tabby_admin.py
   ```
4. **Restart service** (if needed):
   - Render Dashboard → Manual Deploy → Clear build cache & deploy

---

## 🧪 Test After Fix

### 1. Health Check (Should already work)
```bash
curl https://growfund-backend.onrender.com/api/health/
```
**Expected**: `{"status":"ok"}`

### 2. Register New User
```bash
curl -X POST https://growfund-backend.onrender.com/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "password": "securepass123",
    "full_name": "New User"
  }'
```
**Expected**: 201 Created

### 3. Login
```bash
curl -X POST https://growfund-backend.onrender.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "password": "securepass123"
  }'
```
**Expected**: 200 OK with tokens

---

## 📊 Verify Database Tables

After running migrations, check that tables exist:

```bash
cd /app
python manage.py dbshell
```

Then in the database shell:
```sql
\dt  -- List all tables (PostgreSQL)
SELECT * FROM accounts_user LIMIT 1;  -- Check users table
```

---

## 🚨 If Still Getting 500 Errors

1. **Check Render Logs** for the actual error:
   - Render Dashboard → Logs tab
   - Look for Python tracebacks

2. **Check Database Connection**:
   ```bash
   cd /app
   python manage.py check --database default
   ```

3. **Verify Environment Variables**:
   - `DATABASE_URL` should be set
   - `SECRET_KEY` should be set
   - `DEBUG` should be `False`

4. **Check for Missing Dependencies**:
   ```bash
   cd /app
   pip list | grep -i django
   ```

---

## 📚 Related Files

- `backend-growfund/Dockerfile` - Container configuration
- `backend-growfund/start.sh` - Startup script (runs migrations)
- `backend-growfund/growfund/settings.py` - Django settings

---

## ✅ Summary

**Problem**: 500 errors on login/register
**Cause**: Database migrations didn't run
**Solution**: Run migrations manually via Render Shell

```bash
cd /app
python manage.py migrate
python create_tabby_admin.py
```

Then test the endpoints again!
