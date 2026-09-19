import os
import joblib
import boto3
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

S3_BUCKET = os.getenv("S3_BUCKET", "your-mlops-models-bucket")
S3_PREFIX = os.getenv("S3_PREFIX", "models/inference")
AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")
LOCAL_MODEL_PATH = "model.joblib"
MODEL_VERSION = os.getenv("MODEL_VERSION", datetime.utcnow().strftime("v%Y%m%d-%H%M%S"))

def train_model():
    logger.info("Generating synthetic training data...")
    X = np.random.rand(1000, 5)
    y = X @ np.array([1.5, -2.0, 0.8, 3.2, -0.5]) + np.random.randn(1000) * 0.1

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    score = model.score(X_test, y_test)
    logger.info(f"Model R² score: {score:.4f}")

    joblib.dump(model, LOCAL_MODEL_PATH)
    logger.info(f"Model saved locally → {LOCAL_MODEL_PATH}")
    return LOCAL_MODEL_PATH

def upload_to_s3(local_path: str, version: str):
    s3 = boto3.client("s3", region_name=AWS_REGION)

    s3_key = f"{S3_PREFIX}/{version}/model.joblib"
    latest_key = f"{S3_PREFIX}/latest/model.joblib"

    logger.info(f"Uploading to s3://{S3_BUCKET}/{s3_key}")
    s3.upload_file(local_path, S3_BUCKET, s3_key)
    s3.upload_file(local_path, S3_BUCKET, latest_key)
    logger.info(f"Also updated s3://{S3_BUCKET}/{latest_key}")

    return f"s3://{S3_BUCKET}/{s3_key}"

if __name__ == "__main__":
    model_path = train_model()
    s3_uri = upload_to_s3(model_path, MODEL_VERSION)
    print(f"\nModel successfully trained and uploaded:")
    print(f"   Version : {MODEL_VERSION}")
    print(f"   S3 URI  : {s3_uri}")
