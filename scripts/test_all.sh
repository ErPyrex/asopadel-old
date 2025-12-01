#!/bin/bash

# Script Maestro de Testing
# Ejecuta todos los tests del proyecto

set -e  # Exit on error

echo "=========================================="
echo "  ASOPADEL - Complete Test Suite"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

# Parse arguments
RUN_BACKEND=true
RUN_FRONTEND=true
RUN_API=true
RUN_DOCKER=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --backend-only)
            RUN_FRONTEND=false
            RUN_API=false
            RUN_DOCKER=false
            shift
            ;;
        --frontend-only)
            RUN_BACKEND=false
            RUN_API=false
            RUN_DOCKER=false
            shift
            ;;
        --api-only)
            RUN_BACKEND=false
            RUN_FRONTEND=false
            RUN_DOCKER=false
            shift
            ;;
        --docker)
            RUN_DOCKER=true
            shift
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --backend-only    Run only backend tests"
            echo "  --frontend-only   Run only frontend tests"
            echo "  --api-only        Run only API integration tests"
            echo "  --docker          Run Docker tests"
            echo "  --help            Show this help message"
            echo ""
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Track results
TOTAL_SUITES=0
PASSED_SUITES=0
FAILED_SUITES=0

# Function to run test suite
run_suite() {
    local name=$1
    local script=$2
    
    TOTAL_SUITES=$((TOTAL_SUITES + 1))
    
    echo ""
    echo "=========================================="
    echo -e "${BLUE}Running: $name${NC}"
    echo "=========================================="
    
    if bash "$script"; then
        echo -e "${GREEN}✅ $name: PASSED${NC}"
        PASSED_SUITES=$((PASSED_SUITES + 1))
        return 0
    else
        echo -e "${RED}❌ $name: FAILED${NC}"
        FAILED_SUITES=$((FAILED_SUITES + 1))
        return 1
    fi
}

# Run test suites
if [ "$RUN_DOCKER" = true ]; then
    run_suite "Docker Tests" "$SCRIPT_DIR/test_docker.sh" || true
fi

if [ "$RUN_BACKEND" = true ]; then
    run_suite "Backend Tests" "$SCRIPT_DIR/test_backend.sh" || true
fi

if [ "$RUN_FRONTEND" = true ]; then
    run_suite "Frontend Tests" "$SCRIPT_DIR/test_frontend.sh" || true
fi

if [ "$RUN_API" = true ]; then
    run_suite "API Integration Tests" "$SCRIPT_DIR/test_api.sh" || true
fi

# Final summary
echo ""
echo "=========================================="
echo "  FINAL TEST SUMMARY"
echo "=========================================="
echo -e "Total Test Suites:  $TOTAL_SUITES"
echo -e "${GREEN}Passed:             $PASSED_SUITES${NC}"
if [ $FAILED_SUITES -gt 0 ]; then
    echo -e "${RED}Failed:             $FAILED_SUITES${NC}"
else
    echo -e "Failed:             $FAILED_SUITES"
fi
echo "=========================================="

# Exit with error if any suite failed
if [ $FAILED_SUITES -gt 0 ]; then
    echo ""
    echo -e "${RED}❌ Some test suites failed${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✅ All test suites passed!${NC}"
