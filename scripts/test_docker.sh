#!/bin/bash

# Script de Testing Completo - Docker
# Ejecuta todos los tests en contenedores Docker

set -e  # Exit on error

echo "=================================="
echo "  ASOPADEL - Docker Tests"
echo "=================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Docker is running${NC}"
echo ""

# Check if containers are running
echo "Checking Docker containers..."
if ! docker compose ps | grep -q "Up"; then
    echo -e "${YELLOW}⚠️  Containers not running${NC}"
    echo "Starting containers..."
    docker compose up -d
    echo "Waiting for services to be ready..."
    sleep 10
fi

echo -e "${GREEN}✓ Containers are running${NC}"
echo ""

# Test 1: Backend container health
echo -e "${BLUE}Test 1: Backend container health${NC}"
if docker compose exec backend python manage.py check; then
    echo -e "${GREEN}✓ Backend health check passed${NC}"
else
    echo -e "${RED}✗ Backend health check failed${NC}"
    exit 1
fi
echo ""

# Test 2: Database connection
echo -e "${BLUE}Test 2: Database connection${NC}"
if docker compose exec backend python manage.py migrate --check; then
    echo -e "${GREEN}✓ Database connection OK${NC}"
else
    echo -e "${RED}✗ Database connection failed${NC}"
    exit 1
fi
echo ""

# Test 3: Run backend tests in Docker
echo -e "${BLUE}Test 3: Backend tests in Docker${NC}"
if docker compose exec backend python manage.py test; then
    echo -e "${GREEN}✓ Backend tests passed${NC}"
else
    echo -e "${RED}✗ Backend tests failed${NC}"
    exit 1
fi
echo ""

# Test 4: Frontend container health
echo -e "${BLUE}Test 4: Frontend container health${NC}"
if curl -s http://localhost:5173 > /dev/null; then
    echo -e "${GREEN}✓ Frontend is accessible${NC}"
else
    echo -e "${RED}✗ Frontend is not accessible${NC}"
    exit 1
fi
echo ""

# Test 5: API endpoints
echo -e "${BLUE}Test 5: API endpoints${NC}"
if curl -s http://localhost:8000/api/ | grep -q "usuarios"; then
    echo -e "${GREEN}✓ API is responding${NC}"
else
    echo -e "${RED}✗ API is not responding${NC}"
    exit 1
fi
echo ""

# Test 6: Database data integrity
echo -e "${BLUE}Test 6: Database tables${NC}"
table_count=$(docker compose exec db psql -U asopadel_user -d asopadel_barinas -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" | tr -d ' ')
if [ "$table_count" -gt 0 ]; then
    echo -e "${GREEN}✓ Database has $table_count tables${NC}"
else
    echo -e "${RED}✗ Database has no tables${NC}"
    exit 1
fi
echo ""

# Summary
echo "=================================="
echo "  Docker Tests Summary"
echo "=================================="
echo -e "${GREEN}✅ All Docker tests passed!${NC}"
echo ""
echo "Container Status:"
docker compose ps
echo "=================================="
