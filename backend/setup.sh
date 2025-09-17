#!/bin/bash
# FRA Atlas DSS - Quick Setup Script
# Sets up the backend for development and production

set -e

echo "🌳 FRA Atlas DSS Backend Setup"
echo "================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip."
    exit 1
fi

# Create virtual environment
echo "📦 Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing Python dependencies..."
pip install -r requirements.txt

# Create environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "⚙️ Creating environment configuration..."
    cp .env.example .env
    echo "✅ Created .env file. Please update it with your configuration."
fi

# Check if PostgreSQL is available
echo "🗃️ Checking database connection..."
if command -v psql &> /dev/null; then
    echo "✅ PostgreSQL client found"
else
    echo "⚠️ PostgreSQL client not found. Install it to connect to the database."
fi

# Initialize database (if PostgreSQL is running)
echo "🚀 Setting up database..."
if python -c "import psycopg2" 2>/dev/null; then
    echo "✅ PostgreSQL Python adapter available"
    echo "Run 'python init_db.py' to initialize the database"
else
    echo "⚠️ PostgreSQL Python adapter not available. Install psycopg2-binary."
fi

echo ""
echo "🎉 Backend setup completed!"
echo ""
echo "Next steps:"
echo "1. Update .env file with your database credentials"
echo "2. Set up PostgreSQL database with PostGIS extension"
echo "3. Run: python init_db.py"
echo "4. Run: python run.py"
echo ""
echo "For development:"
echo "source venv/bin/activate"
echo "python run.py"
echo ""
echo "For production:"
echo "docker-compose up -d"