# Fix: API 404 Error - `/Api` vs `/api`

## ❌ The Problem

Your frontend is making a request to:
```
GET https://growfund-backend.onrender.com/Api
```

This returns **404 Not Found** because:
1. The path is `/Api` (capital 'A') instead of `/api` (lowercase)
2. `/Api` or `/api` alone doesn't exist - you need the full endpoint path like `/api/health/`

---

## ✅ The Solution

### Backend Fix (Already Applied)

I've added routes to handle both `/api/` and `/Api/` to prevent this error.

Now these all work:
- ✅ `https://growfund-backend.onrender.com/` - Root
- ✅ `https://growfund-backend.onrender.com/api/` - API root
- ✅ `https://growfund-backend.onrender.com/Api/` - API root (capital A)

### Frontend Fix (You Need to Do This)

Check your frontend code for where the API base URL is configured.

#### Common Locations:

**1. Environment Variables (`.env` or `.env.local`)**
```env
# ❌ Wrong
REACT_APP_API_URL=https://growfund-backend.onrender.com/Api

# ✅ Correct
REACT_APP_API_URL=https://growfund-backend.onrender.com/api
```

**2. API Configuration File (e.g., `src/config/api.js`)**
```javascript
// ❌ Wrong
const API_BASE_URL = 'https://growfund-backend.onrender.com/Api';

// ✅ Correct
const API_BASE_URL = 'https://growfund-backend.onrender.com/api';
```

**3. Axios Instance (e.g., `src/services/api.js`)**
```javascript
// ❌ Wrong
const api = axios.create({
  baseURL: 'https://growfund-backend.onrender.com/Api'
});

// ✅ Correct
const api = axios.create({
  baseURL: 'https://growfund-backend.onrender.com/api'
});
```

---

## 🔍 How to Find the Issue

### Search Your Frontend Code:

1. **Search for `/Api`** (capital A):
   ```bash
   # In your frontend directory
   grep -r "/Api" src/
   ```

2. **Check environment files**:
   - `.env`
   - `.env.local`
   - `.env.production`

3. **Check API configuration files**:
   - `src/config/api.js`
   - `src/services/api.js`
   - `src/utils/axios.js`

---

## 📝 Correct API Endpoints

All API endpoints should start with lowercase `/api/`:

### ✅ Correct Examples:
```
https://growfund-backend.onrender.com/api/health/
https://growfund-backend.onrender.com/api/auth/login/
https://growfund-backend.onrender.com/api/auth/register/
https://growfund-backend.onrender.com/api/settings/public/
https://growfund-backend.onrender.com/api/investments/crypto/prices/
```

### ❌ Wrong Examples:
```
https://growfund-backend.onrender.com/Api/health/
https://growfund-backend.onrender.com/API/auth/login/
https://growfund-backend.onrender.com/Api/settings/public/
```

---

## 🧪 Test After Fixing

After updating your frontend, test these URLs:

### 1. API Root
```bash
curl https://growfund-backend.onrender.com/api/
```
**Expected**: API information (200 OK)

### 2. Health Check
```bash
curl https://growfund-backend.onrender.com/api/health/
```
**Expected**: `{"status":"ok"}` (200 OK)

### 3. Public Settings
```bash
curl https://growfund-backend.onrender.com/api/settings/public/
```
**Expected**: Platform settings (200 OK)

---

## 🔧 Quick Fix Steps

1. **Find the issue**:
   - Search for `/Api` in your frontend code
   - Check `.env` files

2. **Fix the URL**:
   - Change `/Api` to `/api` (lowercase)
   - Ensure no trailing slash on base URL

3. **Restart your frontend**:
   ```bash
   npm start
   ```

4. **Clear browser cache**:
   - Hard refresh: `Ctrl + Shift + R` (Windows/Linux)
   - Or: `Cmd + Shift + R` (Mac)

5. **Check browser console**:
   - Should see 200 OK responses
   - No more 404 errors

---

## 💡 Best Practice

### Recommended API Base URL Configuration:

```javascript
// src/config/api.js
const API_BASE_URL = process.env.REACT_APP_API_URL || 
  (process.env.NODE_ENV === 'production' 
    ? 'https://growfund-backend.onrender.com/api'
    : 'http://localhost:8000/api');

export default API_BASE_URL;
```

### In `.env.local` (Development):
```env
REACT_APP_API_URL=http://localhost:8000/api
```

### In `.env.production` (Production):
```env
REACT_APP_API_URL=https://growfund-backend.onrender.com/api
```

---

## 🐛 Still Getting 404?

If you still see 404 errors after fixing:

1. **Check the full URL** in browser console
   - Make sure it's not `/Api/api/...` (double path)
   - Should be `/api/endpoint/` not `/api/endpoint` (trailing slash matters)

2. **Clear all caches**:
   - Browser cache
   - Service worker cache
   - Local storage

3. **Check for typos**:
   - `/api/` not `/api` (trailing slash)
   - Lowercase 'a' not capital 'A'

4. **Verify endpoint exists**:
   - Check `API-ENDPOINTS-DOCUMENTATION.md` for valid endpoints

---

## 📚 Reference

See `API-ENDPOINTS-DOCUMENTATION.md` for complete list of available endpoints.

All endpoints use lowercase `/api/` prefix.

---

**After fixing, your API calls should work perfectly!** 🎉
