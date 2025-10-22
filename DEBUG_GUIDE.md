# ETL Sidecar Debug Mode Guide

## 🐛 Complete Debug Setup and Testing

This guide explains how to run the ETL Sidecar in debug mode with comprehensive monitoring, testing, and troubleshooting.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Debug Modes](#debug-modes)
3. [Debug Features](#debug-features)
4. [Testing](#testing)
5. [Monitoring](#monitoring)
6. [Troubleshooting](#troubleshooting)
7. [Performance Analysis](#performance-analysis)

## Quick Start

### Option 1: Simple Debug Mode
```bash
cd /home/gyan/Documents/vendora/etl-sidecar
source .venv/bin/activate
uvicorn app:app --host 0.0.0.0 --port 3009 --reload
```

### Option 2: Enhanced Debug Mode
```bash
cd /home/gyan/Documents/vendora/etl-sidecar
source .venv/bin/activate
uvicorn app:app --host 0.0.0.0 --port 3009 --reload --log-level debug --access-log
```

### Option 3: Debug Script (Recommended)
```bash
cd /home/gyan/Documents/vendora/etl-sidecar
./debug_start.sh
```

### Option 4: Enhanced Debug App
```bash
cd /home/gyan/Documents/vendora/etl-sidecar
source .venv/bin/activate
python debug_app.py
```

## Debug Modes

### 1. Basic Debug Mode
- **Auto-reload**: Code changes trigger automatic restart
- **Debug logging**: Enhanced log output
- **Access logs**: HTTP request/response logging

```bash
uvicorn app:app --host 0.0.0.0 --port 3009 --reload --log-level debug --access-log
```

### 2. Enhanced Debug Mode
- **Performance monitoring**: Request timing and memory usage
- **Debug endpoints**: Additional debugging endpoints
- **Detailed logging**: Function-level logging with line numbers
- **System metrics**: CPU, memory, and process information

```bash
python debug_app.py
```

### 3. Production Debug Mode
- **Structured logging**: JSON-formatted logs
- **Metrics collection**: Prometheus-compatible metrics
- **Health monitoring**: Advanced health checks
- **Error tracking**: Detailed error reporting

## Debug Features

### 1. Enhanced Logging

#### Log Levels
- **DEBUG**: Detailed function execution
- **INFO**: Service operations and status
- **WARNING**: Non-critical issues
- **ERROR**: Error conditions and failures

#### Log Format
```
2024-01-01 12:00:00 - etl-sidecar - DEBUG - load_model:35 - Loading sentence transformer model...
2024-01-01 12:00:01 - etl-sidecar - INFO - load_model:40 - Model loaded successfully in 2.34 seconds
```

### 2. Debug Endpoints

#### Health Check with Debug Info
```http
GET /healthz
```

**Response**:
```json
{
  "status": "ok",
  "model": "all-MiniLM-L6-v2",
  "service": "etl-sidecar-debug",
  "debug_info": {
    "model_load_time": 2.34,
    "request_count": 15,
    "total_processing_time": 1.23,
    "average_request_time": 0.082,
    "memory_usage": {
      "total": 8.0,
      "available": 4.2,
      "used": 3.8,
      "percent": 47.5
    },
    "cpu_percent": 12.3,
    "uptime": 3600
  }
}
```

#### Debug Statistics
```http
GET /debug/stats
```

**Response**:
```json
{
  "service": "etl-sidecar-debug",
  "timestamp": "2024-01-01T12:00:00Z",
  "stats": {
    "request_count": 15,
    "total_processing_time": 1.23,
    "average_request_time": 0.082,
    "model_load_time": 2.34,
    "memory": {
      "total_gb": 8.0,
      "available_gb": 4.2,
      "used_gb": 3.8,
      "percent": 47.5
    },
    "cpu_percent": 12.3,
    "model_loaded": true
  }
}
```

#### Debug Test Endpoint
```http
GET /debug/test
```

**Purpose**: Run automated similarity calculation test
**Response**: Test results with similarity matrix

### 3. Performance Monitoring

#### Request Timing
- **Total request time**: End-to-end processing time
- **Model loading time**: Time to load sentence transformer
- **Embedding generation**: Time to generate embeddings
- **Similarity calculation**: Time to calculate cosine similarity

#### Memory Monitoring
- **Total memory**: System total memory
- **Available memory**: Free memory available
- **Used memory**: Memory currently in use
- **Memory percentage**: Memory usage percentage

#### CPU Monitoring
- **CPU percentage**: Current CPU usage
- **Process information**: Process-specific metrics

## Testing

### 1. Automated Test Suite

#### Run Complete Test Suite
```bash
cd /home/gyan/Documents/vendora/etl-sidecar
python test_debug.py
```

#### Run Tests with Custom URL
```bash
python test_debug.py --url http://localhost:3009 --wait 10
```

#### Test Output Example
```
🧪 ETL Sidecar Debug Test Suite
==================================================

📋 Basic Endpoint Tests
✅ PASS Health Check
   📝 Status: ok, Model: all-MiniLM-L6-v2
✅ PASS Root Endpoint
   📝 Service: ETL Sidecar - Debug Mode, Version: 1.0.0-debug

🔧 Core Functionality Tests
✅ PASS Similarity Calculation
   📝 Matrix: 4x5, Time: 0.234s
   📊 Similarity Matrix:
     customer_name → name: 0.950
     customer_name → email: 0.120
     customer_name → phone: 0.880
     customer_name → created_at: 0.230
     customer_name → address: 0.150
     email_address → name: 0.150
     email_address → email: 0.920
     email_address → phone: 0.180
     email_address → created_at: 0.450
     email_address → address: 0.200
     phone_number → name: 0.220
     phone_number → email: 0.190
     phone_number → phone: 0.890
     phone_number → created_at: 0.310
     phone_number → address: 0.250
     created_date → name: 0.180
     created_date → email: 0.160
     created_date → phone: 0.200
     created_date → created_at: 0.950
     created_date → address: 0.100

🐛 Debug-Specific Tests
✅ PASS Debug Stats
   📝 Requests: 15, Memory: 47.5%
✅ PASS Debug Test
   📝 Status: success

🚀 Performance Test (3 requests)
   Request 1: 0.234s
   Request 2: 0.198s
   Request 3: 0.201s
✅ PASS Performance Test
   📝 Success: 3/3, Avg: 0.211s, Min: 0.198s, Max: 0.234s

🔍 Error Handling Test
✅ PASS Invalid JSON
   📝 Status: 422
✅ PASS Missing Fields
   📝 Status: 422
✅ PASS Empty Arrays
   📝 Status: 200

📊 Test Summary
==================================================
Total Tests: 8
Passed: 8
Failed: 0
Success Rate: 100.0%

🎉 All tests passed! ETL Sidecar is working correctly.
```

### 2. Manual Testing

#### Test Health Check
```bash
curl -v http://localhost:3009/healthz
```

#### Test Similarity Calculation
```bash
curl -X POST http://localhost:3009/similarity/headers \
  -H "Content-Type: application/json" \
  -d '{
    "headers": ["customer_name", "email_address", "phone_number"],
    "canonicalFields": ["name", "email", "phone", "address"]
  }'
```

#### Test Debug Stats
```bash
curl http://localhost:3009/debug/stats
```

#### Test Debug Test
```bash
curl http://localhost:3009/debug/test
```

### 3. Load Testing

#### Simple Load Test
```bash
# Run multiple requests in parallel
for i in {1..10}; do
  curl -X POST http://localhost:3009/similarity/headers \
    -H "Content-Type: application/json" \
    -d '{"headers":["name","email"],"canonicalFields":["customer_name","email_address"]}' &
done
wait
```

#### Performance Monitoring
```bash
# Monitor system resources
watch -n 1 'curl -s http://localhost:3009/debug/stats | jq .stats.memory.percent'
```

## Monitoring

### 1. Real-time Monitoring

#### System Resources
```bash
# Monitor memory usage
watch -n 1 'curl -s http://localhost:3009/debug/stats | jq .stats.memory'

# Monitor CPU usage
watch -n 1 'curl -s http://localhost:3009/debug/stats | jq .stats.cpu_percent'

# Monitor request count
watch -n 1 'curl -s http://localhost:3009/debug/stats | jq .stats.request_count'
```

#### Log Monitoring
```bash
# Monitor debug logs
tail -f debug.log

# Filter specific log levels
tail -f debug.log | grep "DEBUG"

# Monitor errors
tail -f debug.log | grep "ERROR"
```

### 2. Performance Analysis

#### Request Timing Analysis
```bash
# Test request timing
time curl -X POST http://localhost:3009/similarity/headers \
  -H "Content-Type: application/json" \
  -d '{"headers":["name"],"canonicalFields":["customer_name"]}'
```

#### Memory Usage Analysis
```bash
# Check memory usage before and after requests
curl -s http://localhost:3009/debug/stats | jq .stats.memory.used_gb
```

### 3. Debug Logging

#### Enable Detailed Logging
```python
# In debug_app.py, modify logging level
logging.basicConfig(level=logging.DEBUG)
```

#### Log Analysis
```bash
# Analyze log patterns
grep "processing_time" debug.log | awk '{print $NF}' | sort -n

# Find slow requests
grep "completed in" debug.log | awk '{print $NF}' | sort -n | tail -10
```

## Troubleshooting

### 1. Common Issues

#### Service Not Starting
```bash
# Check if port is already in use
lsof -i :3009

# Check virtual environment
source .venv/bin/activate
which python
python --version
```

#### Model Loading Issues
```bash
# Check if model can be loaded
python -c "from sentence_transformers import SentenceTransformer; model = SentenceTransformer('all-MiniLM-L6-v2'); print('Model loaded successfully')"

# Check available memory
free -h
```

#### Connection Issues
```bash
# Test local connectivity
curl -v http://localhost:3009/healthz

# Test from different host
curl -v http://<server-ip>:3009/healthz
```

### 2. Debug Commands

#### Check Service Status
```bash
# Health check
curl http://localhost:3009/healthz

# Debug stats
curl http://localhost:3009/debug/stats

# Service info
curl http://localhost:3009/
```

#### Check Logs
```bash
# View recent logs
tail -n 50 debug.log

# Search for errors
grep -i error debug.log

# Search for specific patterns
grep "model" debug.log
```

#### Check System Resources
```bash
# Check memory usage
ps aux | grep python

# Check disk space
df -h

# Check network connections
netstat -tlnp | grep 3009
```

### 3. Performance Issues

#### Slow Response Times
```bash
# Check average request time
curl -s http://localhost:3009/debug/stats | jq .stats.average_request_time

# Check memory usage
curl -s http://localhost:3009/debug/stats | jq .stats.memory.percent
```

#### High Memory Usage
```bash
# Check memory details
curl -s http://localhost:3009/debug/stats | jq .stats.memory

# Restart service to clear memory
pkill -f "uvicorn app:app"
./debug_start.sh
```

#### Model Loading Issues
```bash
# Check model load time
curl -s http://localhost:3009/debug/stats | jq .stats.model_load_time

# Force model reload
curl -X POST http://localhost:3009/debug/reload
```

## Performance Analysis

### 1. Benchmarking

#### Single Request Benchmark
```bash
# Time a single request
time curl -X POST http://localhost:3009/similarity/headers \
  -H "Content-Type: application/json" \
  -d '{"headers":["customer_name","email_address"],"canonicalFields":["name","email"]}'
```

#### Batch Request Benchmark
```bash
# Test with larger datasets
curl -X POST http://localhost:3009/similarity/headers \
  -H "Content-Type: application/json" \
  -d '{
    "headers": ["customer_name", "email_address", "phone_number", "created_date", "address_line1", "address_line2", "city", "state", "zip_code", "country"],
    "canonicalFields": ["name", "email", "phone", "created_at", "street", "street2", "city", "state", "postal_code", "country"]
  }'
```

### 2. Performance Metrics

#### Key Metrics to Monitor
- **Request Count**: Total number of requests processed
- **Average Request Time**: Mean processing time per request
- **Memory Usage**: Current memory consumption
- **CPU Usage**: Current CPU utilization
- **Model Load Time**: Time to load the sentence transformer model

#### Performance Targets
- **Response Time**: < 500ms for typical requests
- **Memory Usage**: < 2GB total
- **CPU Usage**: < 50% under normal load
- **Model Load Time**: < 5 seconds

### 3. Optimization

#### Memory Optimization
```python
# In debug_app.py, add memory monitoring
import gc
gc.collect()  # Force garbage collection
```

#### Performance Optimization
```python
# Batch processing optimization
embeddings = model.encode(all_texts, batch_size=32)
```

#### Caching Optimization
```python
# Model caching
if model is None:
    model = SentenceTransformer('all-MiniLM-L6-v2')
```

## Debug Mode Summary

### ✅ What Debug Mode Provides

1. **Enhanced Logging**: Detailed function-level logging
2. **Performance Monitoring**: Request timing and system metrics
3. **Debug Endpoints**: Additional debugging endpoints
4. **Error Tracking**: Comprehensive error reporting
5. **System Monitoring**: Memory, CPU, and process information
6. **Automated Testing**: Complete test suite for validation
7. **Real-time Monitoring**: Live system status and metrics

### 🚀 How to Use Debug Mode

1. **Start Debug Service**: Use any of the debug startup methods
2. **Run Tests**: Execute the automated test suite
3. **Monitor Performance**: Use debug endpoints for real-time monitoring
4. **Analyze Logs**: Review debug logs for detailed information
5. **Troubleshoot Issues**: Use debug commands for problem diagnosis

### 📊 Debug Mode Benefits

- **Faster Development**: Auto-reload and detailed logging
- **Better Testing**: Comprehensive test suite and validation
- **Performance Insights**: Detailed performance metrics and analysis
- **Easier Troubleshooting**: Enhanced error reporting and debugging tools
- **Production Readiness**: Performance monitoring and optimization

---

## Conclusion

Debug mode provides comprehensive monitoring, testing, and troubleshooting capabilities for the ETL Sidecar service. Use it during development, testing, and production debugging to ensure optimal performance and reliability.

The debug mode includes automated testing, performance monitoring, and detailed logging to help identify and resolve issues quickly and efficiently.

