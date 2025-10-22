"""
Enhanced Debug Version of ETL Sidecar
Includes detailed logging, performance monitoring, and debug endpoints
"""

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Dict, Any
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import logging
import time
import psutil
import os
from datetime import datetime

# Enhanced logging configuration
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('debug.log')
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app with debug settings
app = FastAPI(
    title="ETL Sidecar - Debug Mode",
    description="Semantic similarity service for Smart-ETL header mapping (DEBUG)",
    version="1.0.0-debug",
    debug=True
)

# Global variables for debugging
model = None
request_count = 0
total_processing_time = 0
model_load_time = 0

def load_model():
    """Load the sentence transformer model with debug logging"""
    global model, model_load_time
    if model is None:
        start_time = time.time()
        logger.debug("🔄 Loading sentence transformer model...")
        logger.debug(f"📊 Available memory: {psutil.virtual_memory().available / 1024**3:.2f} GB")
        
        try:
            model = SentenceTransformer('all-MiniLM-L6-v2')
            model_load_time = time.time() - start_time
            logger.info(f"✅ Model loaded successfully in {model_load_time:.2f} seconds")
            logger.debug(f"📊 Model memory usage: {psutil.virtual_memory().used / 1024**3:.2f} GB")
        except Exception as e:
            logger.error(f"❌ Model loading failed: {e}")
            raise
    return model

@app.middleware("http")
async def debug_middleware(request: Request, call_next):
    """Debug middleware for request/response logging"""
    global request_count, total_processing_time
    
    start_time = time.time()
    request_count += 1
    
    logger.debug(f"🔍 Request #{request_count}: {request.method} {request.url}")
    logger.debug(f"📋 Headers: {dict(request.headers)}")
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    total_processing_time += process_time
    
    logger.debug(f"⏱️  Request #{request_count} completed in {process_time:.3f}s")
    logger.debug(f"📊 Status: {response.status_code}")
    
    return response

@app.get("/healthz")
async def health_check():
    """Enhanced health check with debug information"""
    try:
        start_time = time.time()
        model = load_model()
        
        # System information
        memory_info = psutil.virtual_memory()
        cpu_percent = psutil.cpu_percent()
        
        health_data = {
            "status": "ok",
            "model": "all-MiniLM-L6-v2",
            "service": "etl-sidecar-debug",
            "debug_info": {
                "model_load_time": model_load_time,
                "request_count": request_count,
                "total_processing_time": total_processing_time,
                "average_request_time": total_processing_time / max(request_count, 1),
                "memory_usage": {
                    "total": memory_info.total / 1024**3,
                    "available": memory_info.available / 1024**3,
                    "used": memory_info.used / 1024**3,
                    "percent": memory_info.percent
                },
                "cpu_percent": cpu_percent,
                "uptime": time.time() - os.path.getctime(__file__)
            }
        }
        
        logger.debug(f"🏥 Health check completed in {time.time() - start_time:.3f}s")
        return health_data
        
    except Exception as e:
        logger.error(f"❌ Health check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Service unhealthy: {str(e)}")

class SimilarityRequest(BaseModel):
    headers: List[str]
    canonicalFields: List[str]

class SimilarityResponse(BaseModel):
    model: str
    similarities: List[List[float]]
    debug_info: Dict[str, Any] = {}

@app.post("/similarity/headers", response_model=SimilarityResponse)
async def calculate_similarities(request: SimilarityRequest):
    """Calculate semantic similarities with debug information"""
    try:
        start_time = time.time()
        
        # Load model
        model = load_model()
        
        logger.debug(f"🔍 Processing similarity request:")
        logger.debug(f"📋 Headers: {request.headers}")
        logger.debug(f"📋 Canonical Fields: {request.canonicalFields}")
        
        # Combine all texts for batch processing
        all_texts = request.headers + request.canonicalFields
        logger.debug(f"📊 Total texts to process: {len(all_texts)}")
        
        # Get embeddings for all texts
        embedding_start = time.time()
        embeddings = model.encode(all_texts)
        embedding_time = time.time() - embedding_start
        
        logger.debug(f"🧠 Embedding generation took {embedding_time:.3f}s")
        logger.debug(f"📊 Embedding shape: {embeddings.shape}")
        
        # Split embeddings back to headers and canonical fields
        header_embeddings = embeddings[:len(request.headers)]
        canonical_embeddings = embeddings[len(request.headers):]
        
        # Calculate similarity matrix
        similarity_start = time.time()
        similarities = cosine_similarity(header_embeddings, canonical_embeddings)
        similarity_time = time.time() - similarity_start
        
        logger.debug(f"📐 Similarity calculation took {similarity_time:.3f}s")
        logger.debug(f"📊 Similarity matrix shape: {similarities.shape}")
        
        # Convert to list of lists for JSON serialization
        similarities_list = similarities.tolist()
        
        # Log similarity matrix for debugging
        logger.debug("📊 Similarity Matrix:")
        for i, header in enumerate(request.headers):
            for j, canonical in enumerate(request.canonicalFields):
                score = similarities_list[i][j]
                logger.debug(f"  {header} → {canonical}: {score:.3f}")
        
        total_time = time.time() - start_time
        
        debug_info = {
            "processing_time": total_time,
            "embedding_time": embedding_time,
            "similarity_time": similarity_time,
            "matrix_shape": similarities.shape,
            "max_similarity": float(np.max(similarities)),
            "min_similarity": float(np.min(similarities)),
            "average_similarity": float(np.mean(similarities))
        }
        
        logger.info(f"✅ Similarity calculation completed in {total_time:.3f}s")
        
        return SimilarityResponse(
            model="all-MiniLM-L6-v2",
            similarities=similarities_list,
            debug_info=debug_info
        )
        
    except Exception as e:
        logger.error(f"❌ Error calculating similarities: {e}")
        logger.error(f"📊 Error details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error calculating similarities: {str(e)}")

@app.get("/debug/stats")
async def debug_stats():
    """Debug statistics endpoint"""
    memory_info = psutil.virtual_memory()
    return {
        "service": "etl-sidecar-debug",
        "timestamp": datetime.now().isoformat(),
        "stats": {
            "request_count": request_count,
            "total_processing_time": total_processing_time,
            "average_request_time": total_processing_time / max(request_count, 1),
            "model_load_time": model_load_time,
            "memory": {
                "total_gb": memory_info.total / 1024**3,
                "available_gb": memory_info.available / 1024**3,
                "used_gb": memory_info.used / 1024**3,
                "percent": memory_info.percent
            },
            "cpu_percent": psutil.cpu_percent(),
            "model_loaded": model is not None
        }
    }

@app.get("/debug/test")
async def debug_test():
    """Debug test endpoint"""
    test_headers = ["customer_name", "email_address", "phone_number"]
    test_canonical = ["name", "email", "phone", "address"]
    
    logger.debug("🧪 Running debug test...")
    
    # Simulate similarity calculation
    request = SimilarityRequest(headers=test_headers, canonicalFields=test_canonical)
    response = await calculate_similarities(request)
    
    return {
        "test": "debug_test",
        "status": "success",
        "result": response
    }

@app.get("/")
async def root():
    """Root endpoint with debug information"""
    return {
        "service": "ETL Sidecar - Debug Mode",
        "version": "1.0.0-debug",
        "endpoints": {
            "health": "/healthz",
            "similarity": "/similarity/headers",
            "debug_stats": "/debug/stats",
            "debug_test": "/debug/test",
            "docs": "/docs"
        },
        "debug_mode": True
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3009, log_level="debug", reload=True)

