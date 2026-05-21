# Create Your Custom Admin User

## 🔧 Option 1: Edit the Script (Recommended)

### 1. Edit `backend-growfund/create_new_admin.py`

Change these lines to your desired credentials:

```python
# New admin credentials - CUSTOMIZE THESE
email = 'your-email@example.com'     # ← Change this
password = 'YourSecurePassword123!'  # ← Change this  
first_name = 'Your'                  # ← Change this
last_name = 'Name'                   # ← Change this
```

### 2. Example Customization:

```python
# New admin credentials - CUSTOMIZE THESE
email = 'ceo@growfund.com'
password = 'SuperSecure2024!'
first_name = 'John'
last_name = 'Smith'
```

---

## 🔧 Option 2: Environment Variables

### Add to Render Environment Variables:

```
CUSTOM_ADMIN_EMAIL=your-email@example.com
CUSTOM_ADMIN_PASSWORD=YourSecurePassword123!
CUSTOM_ADMIN_FIRST_NAME=Your
CUSTOM_ADMIN_LAST_NAME=Name
```

Then the script will use these automatically.

---

## 🔧 Option 3: Multiple Admins

### Edit `backend-growfund/create_new_admin.py` for multiple admins:

```python
# Multiple admin accounts
admins = [
    {
        'email': 'ceo@growfund.com',
        'password': 'CEOPassword123!',
        'first_name': 'CEO',
        'last_name': 'Name'
    },
    {
        'email': 'admin@growfund.com', 
        'password': 'AdminPassword123!',
        'first_name': 'Admin',
        'last_name': 'User'
    }
]

for admin_data in admins:
    # Create each admin...
```

---

## ✅ What Happens After Deployment

When your fresh service deploys, it will automatically:

1. **Run migrations** (create database tables)
2. **Create Tabby admin**: `Tabby@gmail.com` / `Tabby123!`
3. **Create your custom admin**: With your credentials
4. **Start the server**

---

## 🧪 Test Your Custom Admin

After deployment, test login:

```bash
curl -X POST https://your-service.onrender.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your-email@example.com",
    "password": "YourSecurePassword123!"
  }'
```

---

## 📝 Current Admin Accounts

After deployment, you'll have:

### 1. Default Tabby Admin:
```
Email: Tabby@gmail.com
Password: Tabby123!
```

### 2. Your Custom Admin:
```
Email: [whatever you set]
Password: [whatever you set]
```

---

## 🔐 Security Best Practices

### Strong Password Requirements:
- ✅ At least 12 characters
- ✅ Mix of uppercase, lowercase, numbers, symbols
- ✅ Not easily guessable
- ✅ Unique to this system

### Example Strong Passwords:
```
GrowFund2024!Admin
SecureBackend#2024
MyCompany$Admin2024
```

---

## 🎯 Quick Setup Steps

1. **Edit** `backend-growfund/create_new_admin.py`
2. **Change** the email, password, first_name, last_name
3. **Commit and push** the changes
4. **Deploy** your fresh service
5. **Login** with your custom credentials

---

## 📞 Need Help?

If you want me to customize the script for you, just tell me:
- Your desired admin email
- Your desired admin password  
- Your first and last name

I'll update the script with your credentials!

---

## ⚠️ Important Notes

- **Don't use weak passwords** like "admin123" or "password"
- **Use your real email** so you can reset password if needed
- **Keep credentials secure** - don't share them
- **Change default passwords** after first login

---

**Your custom admin will be created automatically when the fresh service deploys!** 🚀