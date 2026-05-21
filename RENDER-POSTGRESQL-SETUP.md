# Production PostgreSQL Setup on Render

## 🗄️ Step-by-Step PostgreSQL Creation

### Step 1: Create PostgreSQL Database

1. **Go to Render Dashboard**: https://dashboard.render.com/
2. **Click "New +"** (top right corner)
3. **Select "PostgreSQL"**

### Step 2: Configure Database Settings

#### Basic Configuration:
| Setting | Value | Notes |
|---------|-------|-------|
| **Name** | `growfund-production-db` | Choose descriptive name |
| **Database** | `growfund_prod` | Database name (auto-generated) |
| **User** | `growfund_user` | Username (auto-generated) |
| **Region** | `Oregon (US West)` | Choose closest to your users |
| **PostgreSQL Version** | `15` | Latest stable version |
| **Plan** | See options below | Choose based on needs |

#### Plan Options:

| Plan | Price | Storage | RAM | Connections | Best For |
|------|-------|---------|-----|-------------|----------|
| **Free** | $0/month | 1 GB | Shared | 97 | Development/Testing |
| **Starter** | $7/month | 1 GB | 0.1 GB | 97 | Small apps |
| **Standard** | $20/month | 10 GB | 1 GB | 197 | Production apps |
| **Pro** | $65/month | 50 GB | 4 GB | 397 | High-traffic apps |

**Recommendation**: 
- **Free** for testing
- **Starter** for small production apps
- **Standard** for most production use cases

### Step 3: Advanced Settings (Optional)

#### Database Parameters:
- **shared_preload_libraries**: `pg_stat_statements` (for monitoring)
- **log_statement**: `all` (for debugging - disable in production)
- **max_connections**: Default (based on plan)

#### Backup Settings:
- **Automated Backups**: Enabled (default)
- **Backup Retention**: 7 days (Free), 30 days (Paid)
- **Point-in-time Recovery**: Available on paid plans

### Step 4: Create Database

1. **Review settings**
2. **Click "Create PostgreSQL"**
3. **Wait 2-5 minutes** for provisioning

---

## 📋 Step 3: Get Connection Details

### After Creation:

1. **Click on your database** in the dashboard
2. **Copy these values**:

#### Internal Database URL (for Render services):
```
postgresql://growfund_user:password@dpg-xxxxx-a/growfund_prod
```

#### External Database URL (for external connections):
```
postgresql://growfund_user:password@dpg-xxxxx-a.oregon-postgres.render.com/growfund_prod
```

#### Individual Connection Details:
- **Hostname**: `dpg-xxxxx-a.oregon-postgres.render.com`
- **Port**: `5432`
- **Database**: `growfund_prod`
- **Username**: `growfund_user`
- **Password**: `[auto-generated]`

---

## 🔐 Step 4: Security Configuration

### Database Access:

#### Internal Access (Render Services):
- ✅ **Automatic**: Services in same region can connect
- ✅ **Secure**: Uses internal network
- ✅ **Fast**: Low latency

#### External Access:
- ⚠️ **Limited**: Only from whitelisted IPs (paid plans)
- ⚠️ **Public**: Free plan allows public access
- 🔒 **SSL**: Always encrypted

### Security Best Practices:

1. **Use Internal URL**: Always use internal URL for Render services
2. **Strong Passwords**: Auto-generated passwords are secure
3. **Regular Backups**: Enable automated backups
4. **Monitor Access**: Check connection logs regularly
5. **Rotate Credentials**: Periodically update passwords

---

## 🔧 Step 5: Database Configuration for Django

### Environment Variables:

Add to your Render web service:

```bash
# Primary database connection
DATABASE_URL=postgresql://growfund_user:password@dpg-xxxxx-a/growfund_prod

# Optional: Separate read replica (for scaling)
DATABASE_READ_URL=postgresql://growfund_user:password@dpg-xxxxx-a/growfund_prod

# Connection pool settings
DB_CONN_MAX_AGE=600
DB_CONN_HEALTH_CHECKS=True
```

### Django Settings (already configured):

```python
# In settings.py
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
        conn_max_age=600  # Connection pooling
    )
}
```

---

## 📊 Step 6: Database Monitoring

### Built-in Monitoring:

1. **Go to your database** in Render dashboard
2. **Click "Metrics" tab**
3. **Monitor**:
   - CPU usage
   - Memory usage
   - Storage usage
   - Connection count
   - Query performance

### Key Metrics to Watch:

| Metric | Healthy Range | Action if Exceeded |
|--------|---------------|-------------------|
| **CPU Usage** | < 80% | Upgrade plan or optimize queries |
| **Memory Usage** | < 85% | Upgrade plan |
| **Storage Usage** | < 90% | Upgrade plan or clean data |
| **Connections** | < 80% of limit | Optimize connection pooling |

---

## 🔄 Step 7: Backup & Recovery

### Automated Backups:

#### Free Plan:
- **Frequency**: Daily
- **Retention**: 7 days
- **Recovery**: Manual restore

#### Paid Plans:
- **Frequency**: Continuous (WAL-E)
- **Retention**: 30 days
- **Recovery**: Point-in-time recovery

### Manual Backup:

```bash
# Create backup
pg_dump $DATABASE_URL > backup.sql

# Restore backup
psql $DATABASE_URL < backup.sql
```

### Backup Best Practices:

1. **Test Restores**: Regularly test backup restoration
2. **Multiple Locations**: Store backups in multiple locations
3. **Automated Testing**: Automate backup validation
4. **Documentation**: Document recovery procedures

---

## 🚀 Step 8: Performance Optimization

### Connection Pooling:

```python
# In Django settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'growfund_prod',
        'USER': 'growfund_user',
        'PASSWORD': 'password',
        'HOST': 'dpg-xxxxx-a',
        'PORT': '5432',
        'CONN_MAX_AGE': 600,  # Connection pooling
        'OPTIONS': {
            'MAX_CONNS': 20,  # Max connections per worker
        }
    }
}
```

### Query Optimization:

1. **Enable pg_stat_statements**:
```sql
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
```

2. **Monitor slow queries**:
```sql
SELECT query, calls, total_time, mean_time 
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;
```

3. **Add database indexes**:
```python
# In Django models
class User(AbstractUser):
    email = models.EmailField(unique=True, db_index=True)  # Index for lookups
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
```

---

## 🔗 Step 9: Connect to Web Service

### In Your Web Service Environment Variables:

```bash
DATABASE_URL=postgresql://growfund_user:password@dpg-xxxxx-a/growfund_prod
```

### Test Connection:

```python
# Test script
import psycopg2
import os

try:
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    cursor = conn.cursor()
    cursor.execute('SELECT version();')
    version = cursor.fetchone()
    print(f"Connected to: {version[0]}")
    conn.close()
    print("✅ Database connection successful!")
except Exception as e:
    print(f"❌ Database connection failed: {e}")
```

---

## 📝 Step 10: Production Checklist

### Before Going Live:

- [ ] **Database created** with appropriate plan
- [ ] **Backups enabled** and tested
- [ ] **Connection URL** added to web service
- [ ] **Migrations tested** on staging
- [ ] **Performance monitoring** set up
- [ ] **Security settings** reviewed
- [ ] **Backup/recovery** procedures documented

### After Going Live:

- [ ] **Monitor performance** daily
- [ ] **Check backup status** weekly
- [ ] **Review security logs** weekly
- [ ] **Update credentials** monthly
- [ ] **Test disaster recovery** quarterly

---

## 💰 Cost Optimization

### Free Plan Limitations:
- 1 GB storage
- Shared resources
- 7-day backup retention
- Public access only

### When to Upgrade:
- **Storage > 800 MB**: Upgrade to Starter
- **High traffic**: Upgrade to Standard
- **Mission critical**: Upgrade to Pro

### Cost-Saving Tips:
1. **Monitor usage**: Track storage and connection usage
2. **Optimize queries**: Reduce CPU usage
3. **Clean old data**: Archive or delete unused data
4. **Connection pooling**: Reduce connection overhead

---

## 🚨 Troubleshooting

### Common Issues:

#### Connection Refused:
- Check DATABASE_URL format
- Verify database is running
- Check network connectivity

#### Too Many Connections:
- Implement connection pooling
- Reduce concurrent connections
- Upgrade to higher plan

#### Slow Queries:
- Add database indexes
- Optimize Django queries
- Use query profiling tools

#### Storage Full:
- Clean old data
- Optimize data types
- Upgrade storage plan

---

## 📚 Additional Resources

### Render Documentation:
- [PostgreSQL Guide](https://render.com/docs/databases)
- [Connection Pooling](https://render.com/docs/database-connection-pooling)
- [Backup & Recovery](https://render.com/docs/database-backups)

### PostgreSQL Resources:
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Performance Tuning](https://wiki.postgresql.org/wiki/Performance_Optimization)
- [Security Best Practices](https://www.postgresql.org/docs/current/security.html)

---

## 🎯 Quick Setup Summary

1. **Create PostgreSQL** on Render (2 min)
2. **Choose appropriate plan** (Free/Starter/Standard)
3. **Copy Internal Database URL**
4. **Add to web service** as `DATABASE_URL`
5. **Deploy web service** with migrations
6. **Monitor and optimize** performance

**Your production PostgreSQL database is ready!** 🚀