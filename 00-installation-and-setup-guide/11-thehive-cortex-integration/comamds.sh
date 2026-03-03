#!/bin/bash

##########################################################
# TheHive ↔ Cortex Integration
# Verification & Health Check Script
# AWS EC2 Deployment
##########################################################

echo "--------------------------------------------"
echo "TheHive ↔ Cortex Integration Health Check"
echo "--------------------------------------------"

##########################################################
# 1️⃣ Check Docker Containers
##########################################################

echo "Checking running Docker containers..."
docker ps

echo "Ensure these containers are running:"
echo "- thehive"
echo "- cassandra"
echo "- elasticsearch (TheHive)"
echo "- cortex"
echo "- elasticsearch (Cortex)"
echo "--------------------------------------------"

##########################################################
# 2️⃣ Check Cortex Port (9001)
##########################################################

echo "Checking Cortex port 9001..."
sudo ss -tulnp | grep 9001

echo "If no output → Cortex not listening."
echo "--------------------------------------------"

##########################################################
# 3️⃣ Check TheHive Port (9000)
##########################################################

echo "Checking TheHive port 9000..."
sudo ss -tulnp | grep 9000

echo "If no output → TheHive not listening."
echo "--------------------------------------------"

##########################################################
# 4️⃣ Test Cortex API Connectivity
##########################################################

echo "Testing Cortex API endpoint..."
curl -s http://localhost:9001/api/status | jq

echo "If API returns JSON → Cortex reachable."
echo "If connection refused → Cortex not accessible."
echo "--------------------------------------------"

##########################################################
# 5️⃣ Test API Key (Manual Replace Required)
##########################################################

echo "Testing Cortex API Key (Replace YOUR_API_KEY)..."
echo "Example:"
echo "curl -H \"Authorization: Bearer YOUR_API_KEY\" http://localhost:9001/api/user"

echo "If valid → User details returned."
echo "If 401 → API key incorrect."
echo "--------------------------------------------"

##########################################################
# 6️⃣ Check Cortex Logs
##########################################################

echo "Recent Cortex logs:"
docker logs cortex --tail 50

echo "--------------------------------------------"

##########################################################
# 7️⃣ Check TheHive Logs
##########################################################

echo "Recent TheHive logs:"
docker logs thehive --tail 50

echo "--------------------------------------------"

##########################################################
# 8️⃣ Check Cortex Job Containers (Analyzer Execution)
##########################################################

echo "Checking temporary analyzer containers..."
docker ps -a | grep cortex-job

echo "If analyzer ran successfully, you should see:"
echo "cortex-job-xxxxxxxx"
echo "--------------------------------------------"

##########################################################
# 9️⃣ Check Resource Usage
##########################################################

echo "System memory usage:"
free -h

echo "Docker resource usage:"
docker stats --no-stream

echo "--------------------------------------------"

##########################################################
# 🔟 Final Integration Checklist
##########################################################

echo "Manual GUI Validation Steps:"
echo "1. TheHive → Platform Management → Connectors → Cortex"
echo "2. Status must show GREEN (OK)"
echo "3. Entities Management → Analyzer Templates"
echo "4. Confirm analyzers are visible"
echo "5. Run analyzer on test observable"
echo "6. Verify job appears in Cortex → Job History"

echo "--------------------------------------------"
echo "Health Check Complete"
echo "--------------------------------------------"
