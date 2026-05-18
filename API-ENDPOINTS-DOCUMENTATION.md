# GrowFund API Endpoints Documentation

**Base URL**: `https://growfund-backend.onrender.com`

---

## 🏠 General Endpoints

### Root
- **GET** `/` - API information and available endpoints
  - **Auth**: None
  - **Response**: API version, status, and endpoint list

### Health Check
- **GET** `/api/health/` - Health check endpoint
  - **Auth**: None
  - **Response**: `{"status": "ok"}`

### Admin Panel
- **GET** `/admin/` - Django admin panel
  - **Auth**: Admin credentials required

---

## 🔐 Authentication & User Management (`/api/auth/`)

### Authentication
- **POST** `/api/auth/register/` - Register new user
- **POST** `/api/auth/login/` - User login
- **POST** `/api/auth/verify-email/` - Verify email address
- **POST** `/api/auth/resend-verification/` - Resend verification email
- **POST** `/api/auth/forgot-password/` - Request password reset
- **POST** `/api/auth/reset-password/` - Reset password with token
- **POST** `/api/token/refresh/` - Refresh JWT token
- **GET** `/api/auth/ping/` - Check authentication status

### User Profile
- **GET** `/api/auth/me/` - Get current user info
- **GET/PUT** `/api/auth/profile/` - Get/Update user profile
- **GET/PUT** `/api/auth/settings/` - Get/Update user settings
- **POST** `/api/auth/change-password/` - Change password
- **GET** `/api/auth/balance/` - Get user balance
- **GET** `/api/auth/dashboard-stats/` - Get dashboard statistics

### Referrals
- **GET** `/api/auth/referrals/` - Get user referrals
- **GET** `/api/auth/referral-stats/` - Get referral statistics
- **POST** `/api/auth/generate-referral-code/` - Generate referral code

### Admin - User Management
- **GET** `/api/auth/admin/dashboard/` - Admin dashboard overview
- **GET** `/api/auth/admin/users/` - List all users
- **GET** `/api/auth/admin/users/suspended/` - List suspended users
- **GET** `/api/auth/admin/users/stats/` - User statistics
- **GET** `/api/auth/admin/users/{user_id}/` - Get user details
- **POST** `/api/auth/admin/users/{user_id}/verify/` - Verify user
- **POST** `/api/auth/admin/users/{user_id}/suspend/` - Suspend/Unsuspend user
- **POST** `/api/auth/admin/users/{user_id}/reset-password/` - Reset user password
- **POST** `/api/auth/admin/users/{user_id}/balance/` - Credit/Debit user balance
- **POST** `/api/auth/admin/users/bulk-credit/` - Bulk credit multiple users

---

## 💰 Investments (`/api/investments/`)

### Portfolio & Stats
- **GET** `/api/investments/all/` - Get all user investments
- **GET** `/api/investments/portfolio/` - Get live portfolio
- **GET** `/api/investments/dashboard-stats/` - Get investment dashboard stats
- **GET** `/api/investments/balance/` - Get investment balance

### Investment Plans
- **GET** `/api/investments/investment-plans/` - List capital investment plans
- **POST** `/api/investments/capital-plan/` - Invest in capital plan

### Crypto Trading
- **POST** `/api/investments/crypto/buy/` - Buy cryptocurrency
- **POST** `/api/investments/crypto/sell/` - Sell cryptocurrency
- **GET** `/api/investments/crypto/prices/` - Get crypto prices
- **GET** `/api/investments/crypto/portfolio/` - Get crypto portfolio

### Trades
- **GET** `/api/investments/trades/` - List trades
- **POST** `/api/investments/trades/` - Create trade
- **GET** `/api/investments/trades/{id}/` - Get trade details
- **PUT** `/api/investments/trades/{id}/` - Update trade
- **DELETE** `/api/investments/trades/{id}/` - Delete trade

### Admin - Crypto Price Management
- **GET** `/api/investments/admin/crypto-prices/` - Get all crypto prices
- **POST** `/api/investments/admin/crypto-prices/update/` - Update single crypto price
- **POST** `/api/investments/admin/crypto-prices/bulk-update/` - Bulk update prices
- **POST** `/api/investments/admin/crypto-prices/{coin}/toggle/` - Toggle crypto active status
- **GET** `/api/investments/admin/crypto-prices/{coin}/history/` - Get price history

---

## 💳 Transactions (`/api/transactions/`)

### Transaction Management
- **GET** `/api/transactions/` - List user transactions
- **GET** `/api/transactions/summary/` - Get transaction summary

### Deposits
- **POST** `/api/transactions/deposit/` - Generic deposit
- **POST** `/api/transactions/momo/deposit/` - MTN MoMo deposit
- **POST** `/api/transactions/korapay/deposit/` - Korapay deposit
- **POST** `/api/transactions/expresspay/deposit/` - ExpressPay deposit (Ghana)
- **POST** `/api/transactions/usdt/initiate/` - Initiate USDT TRC20 deposit
- **GET** `/api/transactions/usdt/status/{deposit_id}/` - Check USDT deposit status

### Withdrawals
- **POST** `/api/transactions/withdraw/` - Generic withdrawal
- **POST** `/api/transactions/momo/withdrawal/` - MTN MoMo withdrawal
- **POST** `/api/transactions/korapay/withdrawal/bank/` - Korapay bank withdrawal
- **POST** `/api/transactions/korapay/withdrawal/mobile/` - Korapay mobile money withdrawal

### Payment Verification
- **GET** `/api/transactions/momo/status/` - Check MoMo payment status
- **POST** `/api/transactions/korapay/verify/` - Verify Korapay transaction
- **POST** `/api/transactions/expresspay/verify/` - Verify ExpressPay transaction

### Payment Utilities
- **GET** `/api/transactions/korapay/banks/` - Get list of banks
- **POST** `/api/transactions/korapay/resolve-account/` - Resolve bank account

### Webhooks (Internal)
- **POST** `/api/transactions/momo/callback/` - MTN MoMo callback
- **POST** `/api/transactions/korapay/webhook/` - Korapay webhook
- **POST** `/api/transactions/expresspay/callback/` - ExpressPay callback
- **POST** `/api/transactions/expresspay/post-url/` - ExpressPay post URL

---

## 🔧 Admin - Transaction Management (`/api/admin/`)

### Deposits
- **GET** `/api/admin/deposits/` - List all deposits
- **POST** `/api/admin/deposits/{deposit_id}/approve/` - Approve deposit
- **POST** `/api/admin/deposits/{deposit_id}/reject/` - Reject deposit

### Withdrawals
- **GET** `/api/admin/withdrawals/` - List all withdrawals
- **POST** `/api/admin/withdrawals/{withdrawal_id}/approve/` - Approve withdrawal
- **POST** `/api/admin/withdrawals/{withdrawal_id}/reject/` - Reject withdrawal

### Investments
- **GET** `/api/admin/investments/` - List all investments
- **PUT** `/api/admin/investments/{investment_id}/edit/` - Edit investment
- **DELETE** `/api/admin/investments/{investment_id}/delete/` - Delete investment

### Transactions
- **GET** `/api/admin/transactions/` - List all transactions
- **PUT** `/api/admin/transactions/{transaction_id}/edit/` - Edit transaction
- **DELETE** `/api/admin/transactions/{transaction_id}/delete/` - Delete transaction

### System Management
- **POST** `/api/admin/run-migrations/` - Run database migrations (Admin only)
- **GET** `/api/admin/db-check/` - Check database migration status (Admin only)

---

## 🎮 Demo Account (`/api/demo/`)

### Demo Account Management
- **GET** `/api/demo/account/` - Get demo account info
- **GET** `/api/demo/balance/` - Get demo balance
- **POST** `/api/demo/deposit/` - Demo deposit (add virtual funds)

### Demo Trading
- **POST** `/api/demo/crypto/buy/` - Buy crypto with demo funds
- **POST** `/api/demo/crypto/sell/` - Sell crypto in demo account
- **POST** `/api/demo/capital-plan/` - Invest in capital plan (demo)
- **POST** `/api/demo/real-estate/` - Invest in real estate (demo)
- **POST** `/api/demo/invest/` - Generic demo investment

### Demo Portfolio
- **GET** `/api/demo/investments/` - Get demo investments
- **GET** `/api/demo/portfolio/` - Get demo portfolio
- **GET** `/api/demo/transactions/` - Get demo transactions

---

## 📊 Binary Trading (`/api/binary/`)

### Assets & Prices
- **GET** `/api/binary/assets/` - Get available trading assets
- **GET** `/api/binary/assets/{symbol}/price/` - Get current asset price
- **GET** `/api/binary/assets/{symbol}/chart/` - Get chart data for asset
- **GET** `/api/binary/prices/` - Get all asset prices

### Trading
- **POST** `/api/binary/trades/open/` - Open new binary trade
- **GET** `/api/binary/trades/active/` - Get active trades
- **GET** `/api/binary/trades/history/` - Get trade history
- **POST** `/api/binary/trades/{trade_id}/close/` - Close trade manually

### Account
- **GET** `/api/binary/balances/` - Get live and demo balances
- **GET** `/api/binary/stats/` - Get user trading statistics

### Social Features
- **GET** `/api/binary/feed/winners/` - Get recent winners
- **GET** `/api/binary/feed/live/` - Get live trading feed

### Admin
- **POST** `/api/binary/admin/close-expired/` - Close expired trades

---

## 🔔 Notifications (`/api/notifications/`)

### User Notifications
- **GET** `/api/notifications/` - List user notifications
- **POST** `/api/notifications/{notification_id}/read/` - Mark notification as read
- **POST** `/api/notifications/mark-all-read/` - Mark all notifications as read
- **DELETE** `/api/notifications/{notification_id}/delete/` - Delete notification
- **GET** `/api/notifications/stats/` - Get notification statistics
- **POST** `/api/notifications/create-welcome/` - Create welcome notifications

### Admin Notifications
- **POST** `/api/notifications/admin/send/` - Send notification to users
- **GET** `/api/notifications/admin/notifications/` - Get all notifications
- **DELETE** `/api/notifications/admin/notifications/{notification_id}/` - Delete notification

---

## ⚙️ Platform Settings (`/api/settings/`)

### Public Settings
- **GET** `/api/settings/public/` - Get public platform settings
  - **Auth**: None
  - **Returns**: Platform name, fees, limits, etc.

### Admin Settings
- **GET** `/api/settings/admin/settings/` - Get all platform settings
- **PUT** `/api/settings/admin/settings/` - Update platform settings
- **GET** `/api/settings/admin/settings/history/` - Get settings change history

---

## 🔗 Referrals (`/api/referrals/`)

Currently integrated into `/api/auth/` endpoints. See Authentication section above.

---

## 📝 Notes

### Authentication
Most endpoints require JWT authentication. Include the token in the header:
```
Authorization: Bearer <your_jwt_token>
```

### Admin Endpoints
Admin endpoints require staff or superuser privileges.

### Response Format
All endpoints return JSON responses with appropriate HTTP status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Server Error

### Pagination
List endpoints support pagination with query parameters:
- `?page=1` - Page number
- `?page_size=20` - Items per page

### Filtering & Search
Many list endpoints support filtering:
- `?status=pending` - Filter by status
- `?search=keyword` - Search by keyword
- `?ordering=-created_at` - Sort results

---

## 🧪 Testing Endpoints

### Quick Test Commands

```bash
# Health check
curl https://growfund-backend.onrender.com/api/health/

# Get API info
curl https://growfund-backend.onrender.com/

# Register user
curl -X POST https://growfund-backend.onrender.com/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123","full_name":"Test User"}'

# Login
curl -X POST https://growfund-backend.onrender.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123"}'

# Get crypto prices (requires auth)
curl https://growfund-backend.onrender.com/api/investments/crypto/prices/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 📚 Additional Resources

- **Admin Panel**: https://growfund-backend.onrender.com/admin/
- **API Root**: https://growfund-backend.onrender.com/
- **Health Check**: https://growfund-backend.onrender.com/api/health/

---

**Total Endpoints**: 100+ endpoints across 9 modules
**Last Updated**: May 18, 2026
