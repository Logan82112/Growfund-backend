# Render Database Migration & Sync Guide

## Problem
After pushing code to GitHub, Render didn't run migrations automatically, and you want to sync your local database data to Render.

---

## Solution Options

### Option 1: Run Migrations on Render (Recommended First Step)

#### Step 1: Trigger Manual Deploy on Render
1. Go to your Render dashboard: https://dashboard.render.com
2. Select your backend service
3. Click "Manual Deploy" → "Deploy latest commit"
4. Wait for deployment to complete

#### Step 2: Run Migrations via Render Shell
1. In Render dashboard, go to your service
2. Click "Shell" tab (or "Console")
3. Run these commands:
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

#### Step 3: Create Admin User on Render
```bash
python manage.py create_admin
# Or use the shell:
python manage.py shell
```
Then in shell:
```python
from accounts.models import User
admin = User.objects.create_user(
    email='admin@growfund.com',
    password='Admin123!',
    first_name='Admin',
    last_name='User',
    is_staff=True,
    is_superuser=True,
    is_verified=True
)
print("Admin created!")
exit()
```

---

### Option 2: Export Local Data & Import to Render

This is the best way to sync your local database to Render.

#### Step 1: Export Local Database to JSON

```bash
cd backend-growfund

# Export all data
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 2 > data_backup.json

# Or export specific apps only (recommended):
python manage.py dumpdata accounts transactions investments notifications settings_app demo binary_trading --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 2 > data_backup.json
```

#### Step 2: Upload to Render

**Method A: Via Git (Recommended)**
```bash
# Add the backup file to git
git add backend-growfund/data_backup.json
git commit -m "Add database backup for Render import"
git push origin main
```

**Method B: Via Render Shell (Direct)**
1. Copy the content of `data_backup.json`
2. In Render Shell, create the file:
```bash
cat > data_backup.json << 'EOF'
# Paste your JSON content here
EOF
```

#### Step 3: Import Data on Render

In Render Shell:
```bash
# First, run migrations
python manage.py migrate

# Then load the data
python manage.py loaddata data_backup.json
```

---

### Option 3: Use PostgreSQL Dump (If Using PostgreSQL)

If Render is using PostgreSQL:

#### Step 1: Get Render Database Credentials
1. Go to Render Dashboard
2. Click on your PostgreSQL database
3. Copy the "External Database URL"

#### Step 2: Export Local SQLite to PostgreSQL Format

**Install pgloader** (converts SQLite to PostgreSQL):
```bash
# On Windows (using Chocolatey)
choco install pgloader

# Or download from: https://github.com/dimitri/pgloader/releases
```

**Convert and Upload**:
```bash
pgloader backend-growfund/db.sqlite3 postgresql://[RENDER_DB_URL]
```

---

### Option 4: Create Test Data on Render

If you just need sample data (not exact local data):

In Render Shell:
```bash
python manage.py create_test_data
```

This will create:
- 20 test users
- Sample transactions
- Sample investments
- Admin user

---

## Recommended Approach (Step-by-Step)

### Phase 1: Ensure Migrations Run
```bash
# On Render Shell
python manage.py migrate
python manage.py collectstatic --noinput
```

### Phase 2: Create Admin User
```bash
python manage.py shell
```
```python
from accounts.models import User
User.objects.create_user(
    email='admin@growfund.com',
    password='Admin123!',
    is_staff=True,
    is_superuser=True,
    is_verified=True
)
```

### Phase 3: Export & Import Data

**On Local Machine:**
```bash
cd backend-growfund
python manage.py dumpdata accounts transactions investments notifications settings_app --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 2 > data_backup.json
git add data_backup.json
git commit -m "Add database backup"
git push origin main
```

**On Render (after deploy):**
```bash
python manage.py loaddata data_backup.json
```

---

## Automatic Migrations on Render

To ensure migrations run automatically on every deploy:

### Update `build.sh` or Build Command

**File**: `backend-growfund/build.sh`

```bash
#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Run migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Create default settings if needed
python manage.py setup_platform_settings || true

# Setup crypto prices if needed
python manage.py setup_crypto_prices || true
```

Make it executable:
```bash
chmod +x backend-growfund/build.sh
```

### Update Render Build Command

In Render Dashboard:
1. Go to your service settings
2. Update "Build Command" to:
```bash
./build.sh
```

Or directly:
```bash
pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
```

---

## Quick Commands Reference

### Export Local Data
```bash
cd backend-growfund
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 2 > data_backup.json
```

### Import Data on Render
```bash
python manage.py loaddata data_backup.json
```

### Run Migrations on Render
```bash
python manage.py migrate
```

### Create Admin on Render
```bash
python manage.py create_admin
```

### Create Test Data on Render
```bash
python manage.py create_test_data
```

### Check Database Status
```bash
python manage.py showmigrations
```

---

## Troubleshooting

### Issue: "No such table" errors
**Solution**: Run migrations first
```bash
python manage.py migrate
```

### Issue: "Duplicate key" errors during import
**Solution**: Clear database first
```bash
python manage.py flush --noinput
python manage.py migrate
python manage.py loaddata data_backup.json
```

### Issue: Migrations not running automatically
**Solution**: Update build command in Render settings to include `python manage.py migrate`

### Issue: Can't access Render Shell
**Solution**: 
1. Check if service is running
2. Try "Restart Service"
3. Use Render's web-based shell (not SSH)

---

## Best Practices

### 1. Regular Backups
```bash
# Create backup script
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 2 > backup_$(date +%Y%m%d_%H%M%S).json
```

### 2. Separate Sensitive Data
Don't commit:
- User passwords (they're hashed, but still)
- Real user data
- Production secrets

### 3. Use Environment Variables
Ensure `.env` on Render has:
```env
DATABASE_URL=postgresql://...
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-render-url.onrender.com
```

### 4. Test Locally First
Before importing to Render:
```bash
# Test the backup file locally
python manage.py loaddata data_backup.json
```

---

## Current Status Checklist

- [ ] Code pushed to GitHub
- [ ] Render deployed latest commit
- [ ] Migrations run on Render
- [ ] Admin user created on Render
- [ ] Data exported from local
- [ ] Data imported to Render
- [ ] Test login on Render URL
- [ ] Verify data appears correctly

---

## Quick Start (TL;DR)

**1. Export local data:**
```bash
cd backend-growfund
python manage.py dumpdata accounts transactions investments notifications settings_app --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 2 > data_backup.json
```

**2. Commit and push:**
```bash
git add data_backup.json
git commit -m "Add database backup"
git push origin main
```

**3. On Render Shell:**
```bash
python manage.py migrate
python manage.py loaddata data_backup.json
```

**Done!** Your Render database now has the same data as local.

---

**Next Steps**: Choose your preferred method and follow the steps above.
