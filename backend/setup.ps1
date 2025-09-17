# FRA Atlas DSS - Backend Setup (Windows)
# PowerShell script for Windows setup

Write-Host "🌳 FRA Atlas DSS Backend Setup" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not installed. Please install Python 3.8 or higher." -ForegroundColor Red
    exit 1
}

# Check if pip is installed
try {
    pip --version | Out-Null
    Write-Host "✅ pip is available" -ForegroundColor Green
} catch {
    Write-Host "❌ pip is not installed. Please install pip." -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host "📦 Creating Python virtual environment..." -ForegroundColor Yellow
python -m venv venv

# Activate virtual environment
Write-Host "🔄 Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Upgrade pip
Write-Host "⬆️ Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install dependencies
Write-Host "📚 Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Create environment file if it doesn't exist
if (!(Test-Path ".env")) {
    Write-Host "⚙️ Creating environment configuration..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "✅ Created .env file. Please update it with your configuration." -ForegroundColor Green
}

# Check PostgreSQL
Write-Host "🗃️ Checking for PostgreSQL..." -ForegroundColor Yellow
try {
    psql --version | Out-Null
    Write-Host "✅ PostgreSQL client found" -ForegroundColor Green
} catch {
    Write-Host "⚠️ PostgreSQL client not found. Install PostgreSQL with PostGIS extension." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎉 Backend setup completed!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Update .env file with your database credentials"
Write-Host "2. Set up PostgreSQL database with PostGIS extension"
Write-Host "3. Run: python init_db.py"
Write-Host "4. Run: python run.py"
Write-Host ""
Write-Host "For development:"
Write-Host ".\venv\Scripts\Activate.ps1"
Write-Host "python run.py"