#!/bin/bash

# Script de Testing Automatizado - Frontend
# Ejecuta todos los tests del frontend React

set -e  # Exit on error

echo "=================================="
echo "  ASOPADEL - Frontend Tests"
echo "=================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Navigate to frontend directory
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}⚠️  node_modules not found${NC}"
    echo "Installing dependencies..."
    npm install
fi

echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Run tests
echo "Running React tests..."
echo "----------------------"
npm run test

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ All frontend tests passed!${NC}"
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
    npm run test -- --coverage
    
    echo ""
    echo -e "${GREEN}✓ Coverage report generated${NC}"
fi

echo ""
echo "=================================="
echo "  Tests completed"
echo "=================================="
