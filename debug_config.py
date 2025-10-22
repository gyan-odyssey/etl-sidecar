"""
Debug Configuration for ETL Sidecar
Enhanced logging and debugging settings
"""

import logging
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('debug.log')
    ]
)

# Create debug logger
debug_logger = logging.getLogger('etl-sidecar-debug')

def create_debug_app():
    """Create FastAPI app with debug settings"""
    app = FastAPI(
        title="ETL Sidecar - Debug Mode",
        description="Semantic similarity service for Smart-ETL header mapping (DEBUG)",
        version="1.0.0-debug",
        debug=True
    )
    
    # Add CORS middleware for debugging
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    return app

def run_debug_server():
    """Run the debug server with enhanced settings"""
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=3009,
        reload=True,
        log_level="debug",
        access_log=True,
        debug=True,
        reload_dirs=["./"],
        reload_delay=1.0
    )

if __name__ == "__main__":
    run_debug_server()

