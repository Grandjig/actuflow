#!/bin/bash
# ===========================================
# Database Migration Script for ActuFlow
# ===========================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "==========================================="
echo "ActuFlow Database Migration"
echo "==========================================="

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Check if running in Docker or locally
if command -v docker &> /dev/null && docker ps | grep -q actuflow-backend; then
    echo -e "${YELLOW}Running migrations via Docker...${NC}"
    EXEC_CMD="docker exec actuflow-backend"
else
    echo -e "${YELLOW}Running migrations locally...${NC}"
    EXEC_CMD=""
    cd backend
fi

# Check current migration status
echo ""
echo "Current migration status:"
$EXEC_CMD alembic current

# Run migrations
echo ""
echo "Running migrations..."
$EXEC_CMD alembic upgrade head

# Show migration history
echo ""
echo "Migration history:"
$EXEC_CMD alembic history --verbose | head -30

echo ""
echo -e "${GREEN}✓ Migrations completed successfully!${NC}"
echo ""
