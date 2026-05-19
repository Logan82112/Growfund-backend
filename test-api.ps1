# Test GrowFund Backend API
Write-Host "Testing GrowFund Backend API..." -ForegroundColor Cyan
Write-Host ""

# Test 1: Health Check
Write-Host "1. Testing Health Endpoint..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "https://growfund-backend.onrender.com/api/health/" -Method GET
    Write-Host "   SUCCESS: Health check passed - $($health.status)" -ForegroundColor Green
} catch {
    Write-Host "   FAILED: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test 2: Register User
Write-Host "2. Testing Registration..." -ForegroundColor Yellow
$randomEmail = "testuser$(Get-Random)@example.com"
$registerBody = "{`"email`":`"$randomEmail`",`"password`":`"testpass123`",`"full_name`":`"Test User`"}"

try {
    $register = Invoke-RestMethod -Uri "https://growfund-backend.onrender.com/api/auth/register/" -Method POST -ContentType "application/json" -Body $registerBody
    Write-Host "   SUCCESS: User registered - $randomEmail" -ForegroundColor Green
    $testEmail = $randomEmail
} catch {
    Write-Host "   FAILED: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.ErrorDetails.Message) {
        Write-Host "   Details: $($_.ErrorDetails.Message)" -ForegroundColor Red
    }
    $testEmail = $null
}
Write-Host ""

# Test 3: Login
Write-Host "3. Testing Login..." -ForegroundColor Yellow
if ($testEmail) {
    $loginBody = "{`"email`":`"$testEmail`",`"password`":`"testpass123`"}"
    try {
        $login = Invoke-RestMethod -Uri "https://growfund-backend.onrender.com/api/auth/login/" -Method POST -ContentType "application/json" -Body $loginBody
        Write-Host "   SUCCESS: Login successful!" -ForegroundColor Green
        Write-Host "   Token: $($login.tokens.access.Substring(0,30))..." -ForegroundColor Gray
    } catch {
        Write-Host "   FAILED: $($_.Exception.Message)" -ForegroundColor Red
        if ($_.ErrorDetails.Message) {
            Write-Host "   Details: $($_.ErrorDetails.Message)" -ForegroundColor Red
        }
    }
} else {
    Write-Host "   SKIPPED: No user to login with" -ForegroundColor Yellow
}
Write-Host ""

# Test 4: Public Settings
Write-Host "4. Testing Public Settings..." -ForegroundColor Yellow
try {
    $settings = Invoke-RestMethod -Uri "https://growfund-backend.onrender.com/api/settings/public/" -Method GET
    Write-Host "   SUCCESS: Settings retrieved" -ForegroundColor Green
    Write-Host "   Platform: $($settings.data.platformName)" -ForegroundColor Gray
} catch {
    Write-Host "   FAILED: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

Write-Host "API Testing Complete!" -ForegroundColor Cyan
