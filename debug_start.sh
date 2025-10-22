#!/bin/bash

# ETL Sidecar Debug Startup Script
# Enhanced debugging and monitoring

echo "🐛 Starting ETL Sidecar in Debug Mode..."

# Navigate to the sidecar directory
cd /home/gyan/Documents/vendora/etl-sidecar

# Activate virtual environment
echo "📦 Activating virtual environment..."
source .venv/bin/activate

# Check if virtual environment is active
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Virtual environment activated: $VIRTUAL_ENV"
else
    echo "❌ Failed to activate virtual environment"
    exit 1
fi

# Check Python packages
echo "🔍 Checking Python packages..."
python -c "
import fastapi, uvicorn, sentence_transformers, sklearn, numpy
print('✅ All required packages are available')
print(f'FastAPI: {fastapi.__version__}')
print(f'Uvicorn: {uvicorn.__version__}')
print(f'Sentence Transformers: {sentence_transformers.__version__}')
print(f'Scikit-learn: {sklearn.__version__}')
print(f'NumPy: {numpy.__version__}')
"

# Create debug log directory
mkdir -p logs
echo "📁 Created logs directory"

# Start the debug server
echo "🚀 Starting ETL Sidecar debug server..."
echo "📍 Server will be available at: http://localhost:3009"
echo "🔍 Health check: http://localhost:3009/healthz"
echo "📊 API docs: http://localhost:3009/docs"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

# Run with debug configuration
uvicorn app:app \
    --host 0.0.0.0 \
    --port 3009 \
    --reload \
    --log-level debug \
    --access-log \
    --reload-dir ./ \
    --reload-delay 1.0

