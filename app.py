"""
ETL Sidecar - Embeddings Service
FastAPI application for semantic similarity calculations
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="ETL Sidecar - Embeddings Service",
    description="Semantic similarity service for Smart-ETL header mapping",
    version="1.0.0"
)

# Global model variable
model = None

def load_model():
    """Load the sentence transformer model"""
    global model
    if model is None:
        logger.info("Loading sentence transformer model...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        logger.info("Model loaded successfully")
    return model

@app.get("/healthz")
async def health_check():
    """Health check endpoint"""
    try:
        # Ensure model is loaded
        load_model()
        return {
            "status": "ok",
            "model": "all-MiniLM-L6-v2",
            "service": "etl-sidecar"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Service unhealthy: {str(e)}")

class SimilarityRequest(BaseModel):
    headers: List[str]
    canonicalFields: List[str]

class SimilarityResponse(BaseModel):
    model: str
    similarities: List[List[float]]

@app.post("/similarity/headers", response_model=SimilarityResponse)
async def calculate_similarities(request: SimilarityRequest):
    """
    Calculate semantic similarities between headers and canonical fields
    """
    try:
        # Load model
        model = load_model()
        
        # Get embeddings for headers and canonical fields
        logger.info(f"Calculating similarities for {len(request.headers)} headers and {len(request.canonicalFields)} canonical fields")
        
        # Combine all texts for batch processing
        all_texts = request.headers + request.canonicalFields
        
        # Get embeddings for all texts
        embeddings = model.encode(all_texts)
        
        # Split embeddings back to headers and canonical fields
        header_embeddings = embeddings[:len(request.headers)]
        canonical_embeddings = embeddings[len(request.headers):]
        
        # Calculate similarity matrix
        similarities = cosine_similarity(header_embeddings, canonical_embeddings)
        
        # Convert to list of lists for JSON serialization
        similarities_list = similarities.tolist()
        
        logger.info(f"Successfully calculated {len(similarities_list)} x {len(similarities_list[0]) if similarities_list else 0} similarity matrix")
        
        return SimilarityResponse(
            model="all-MiniLM-L6-v2",
            similarities=similarities_list
        )
        
    except Exception as e:
        logger.error(f"Error calculating similarities: {e}")
        raise HTTPException(status_code=500, detail=f"Error calculating similarities: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "ETL Sidecar - Embeddings Service",
        "version": "1.0.0",
        "endpoints": {
            "health": "/healthz",
            "similarity": "/similarity/headers"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3009)
