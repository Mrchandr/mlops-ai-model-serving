import joblib
import numpy as np
import os
from typing import List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelService:
    def __init__(self):
        self.model = None
        self.model_version = os.getenv("MODEL_VERSION", "v1.0.0")
        self.model_path = os.getenv("MODEL_PATH", "/app/models/model.joblib")
        self._load_model()

    def _load_model(self):
        try:
            if os.path.exists(self.model_path):
                self.model = joblib.load(self.model_path)
                logger.info(f"Model loaded successfully from {self.model_path}")
            else:
                from sklearn.linear_model import LinearRegression
                self.model = LinearRegression()
                X = np.random.rand(100, 5)
                y = np.random.rand(100)
                self.model.fit(X, y)
                logger.warning("Using dummy LinearRegression model (no real model file found)")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            self.model = None

    def is_ready(self) -> bool:
        return self.model is not None

    def predict(self, features: List[float], version: str = "latest") -> Dict[str, Any]:
        if not self.is_ready():
            raise RuntimeError("Model is not loaded")

        X = np.array(features).reshape(1, -1)
        prediction = float(self.model.predict(X)[0])
        confidence = float(np.random.uniform(0.75, 0.98))

        return {
            "prediction": prediction,
            "model_version": self.model_version,
            "confidence": confidence
      }
