from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from model import ModelService

app = FastAPI(
    title="AI Model Inference API",
    description="High-throughput FastAPI server for model serving on AWS EKS",
    version="1.0.0"
)

model_service = ModelService()

class PredictionRequest(BaseModel):
    features: List[float]
    model_version: Optional[str] = "latest"

class PredictionResponse(BaseModel):
    prediction: float
    model_version: str
    confidence: Optional[float] = None

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": model_service.is_ready()}

@app.get("/ready")
async def readiness_check():
    if not model_service.is_ready():
        raise HTTPException(status_code=503, detail="Model not ready")
    return {"status": "ready"}

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    try:
        result = model_service.predict(request.features, request.model_version)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, workers=4)
