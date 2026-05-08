#!/usr/bin/env bash
# Script to import data on Render
# Run this in Render Shell after deployment

echo "🔄 Running migrations..."
python manage.py migrate

echo "📥 Importing database backup..."
python manage.py loaddata data_backup.json

echo "✅ Data import completed!"
echo ""
echo "🔐 Admin credentials:"
echo "   Email: admin@growfund.com"
echo "   Password: (the password from your local database)"
echo ""
echo "🌐 Your app should now have all the local data!"
