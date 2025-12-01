#!/bin/bash

# Script de Testing Automatizado - Backend
# Ejecuta todos los tests del backend Django

set -e  # Exit on error

echo "=================================="
echo "  ASOPADEL - Backend Tests"
echo "=================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment not activated${NC}"
    echo "Activating venv..."
    source venv/bin/activate
fi

echo -e "${GREEN}✓ Virtual environment active${NC}"
echo ""

# Run Django tests
echo "Running Django tests..."
echo "------------------------"
python manage.py test --verbosity=2

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ All backend tests passed!${NC}"
else
    echo ""
    echo -e "${RED}❌ Some tests failed${NC}"
    exit 1
fi

# Optional: Run with coverage
read -p "Run with coverage? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Running tests with coverage..."
    echo "------------------------------"
    
    # Install coverage if not installed
    pip show coverage > /dev/null 2>&1 || pip install coverage
    
    coverage run --source='.' manage.py test
    coverage report
    coverage html
    
    echo ""
    echo -e "${GREEN}✓ Coverage report generated in htmlcov/index.html${NC}"
fi

echo ""
echo "=================================="
echo "  Tests completed"
echo "=================================="
