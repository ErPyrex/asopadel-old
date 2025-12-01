#!/bin/bash

# Script de Testing de API - Automatizado
# Prueba todos los endpoints de la API REST

set -e  # Exit on error

echo "=================================="
echo "  ASOPADEL - API Integration Tests"
echo "=================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
API_URL="http://localhost:8000/api"
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Function to test endpoint
test_endpoint() {
    local method=$1
    local endpoint=$2
    local expected_status=$3
    local description=$4
    local data=$5
    local token=$6
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    echo -e "${BLUE}Test $TOTAL_TESTS: $description${NC}"
    
    # Build curl command
    if [ -n "$token" ]; then
        headers="-H 'Authorization: Bearer $token'"
    else
        headers=""
    fi
    
    if [ -n "$data" ]; then
        response=$(curl -s -w "\n%{http_code}" -X $method "$API_URL$endpoint" \
            -H "Content-Type: application/json" \
            $headers \
            -d "$data")
    else
        response=$(curl -s -w "\n%{http_code}" -X $method "$API_URL$endpoint" $headers)
    fi
    
    # Extract status code (last line)
    status_code=$(echo "$response" | tail -n1)
    
    # Check if status matches expected
    if [ "$status_code" -eq "$expected_status" ]; then
        echo -e "${GREEN}✓ PASSED${NC} (Status: $status_code)"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${RED}✗ FAILED${NC} (Expected: $expected_status, Got: $status_code)"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
    echo ""
}

# Check if API is running
echo "Checking if API is running..."
if ! curl -s "$API_URL/" > /dev/null; then
    echo -e "${RED}❌ API is not running at $API_URL${NC}"
    echo "Please start the server with: python manage.py runserver"
    echo "Or with Docker: docker compose up"
    exit 1
fi
echo -e "${GREEN}✓ API is running${NC}"
echo ""

# Test 1: API Root
test_endpoint "GET" "/" 200 "API Root accessible"

# Test 2: List Torneos (without auth)
test_endpoint "GET" "/torneos/" 200 "List torneos without authentication"

# Test 3: List Canchas
test_endpoint "GET" "/canchas/" 200 "List canchas"

# Test 4: List Partidos
test_endpoint "GET" "/partidos/" 200 "List partidos"

# Test 5: Login with invalid credentials
test_endpoint "POST" "/auth/login/" 400 "Login with invalid credentials" \
    '{"cedula":"invalid","password":"wrong"}'

# Test 6: List Usuarios without auth (should require auth)
test_endpoint "GET" "/usuarios/" 401 "List usuarios without authentication"

# Test 7: Create Torneo without auth (should fail)
test_endpoint "POST" "/torneos/" 401 "Create torneo without authentication" \
    '{"nombre":"Test","descripcion":"Test","fecha_inicio":"2025-01-01","fecha_fin":"2025-01-31"}'

# Summary
echo "=================================="
echo "  Test Summary"
echo "=================================="
echo -e "Total Tests:  $TOTAL_TESTS"
echo -e "${GREEN}Passed:       $PASSED_TESTS${NC}"
if [ $FAILED_TESTS -gt 0 ]; then
    echo -e "${RED}Failed:       $FAILED_TESTS${NC}"
else
    echo -e "Failed:       $FAILED_TESTS"
fi
echo "=================================="

# Exit with error if any test failed
if [ $FAILED_TESTS -gt 0 ]; then
    exit 1
fi

echo ""
echo -e "${GREEN}✅ All API tests passed!${NC}"
