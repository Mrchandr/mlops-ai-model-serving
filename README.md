# End-to-End MLOps Pipeline for AI Model Serving on AWS

This project demonstrates a complete MLOps pipeline that automatically builds, containerizes, and deploys an AI inference service on AWS.

## What This Project Does

1. Creates a FastAPI-based AI model inference API
2. Packages the application using multi-stage Docker builds
3. Automatically builds and pushes the Docker image to **Amazon ECR** using **GitHub Actions**
4. Deploys and runs the application on **AWS EC2**

## Architecture Flow
Developer pushes code to GitHub
↓
GitHub Actions runs (Lint + Build)
↓
Docker image is pushed to Amazon ECR
↓
Image is pulled and run on AWS EC2
↓
API becomes available on port 8000

## Tech Stack

- **Python + FastAPI** → AI Inference API
- **Docker** → Containerization
- **GitHub Actions** → CI/CD Pipeline
- **Amazon ECR** → Docker Image Registry
- **AWS EC2** → Application Hosting

## Project Structure
mlops-ai-model-serving/
├── app/
│   ├── main.py
│   ├── model.py
│   └── requirements.txt
├── docker/
│   └── Dockerfile
├── .github/workflows/
│   └── ci-cd.yml
└── README.md

## How to Run Locally

# Without Docker

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r app/requirements.txt
cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
Open: http://65.0.180.141:8000/docs

# Using Docker

docker build -t ai-inference:latest -f docker/Dockerfile .
docker run -d -p 8000:8000 --name ai-inference ai-inference:latest

## Deploy on EC2

docker run -d -p 8000:8000 --name ai-inference \
  881940379792.dkr.ecr.ap-south-1.amazonaws.com/ai-inference:latest

## API Endpoints

| Endpoint     | Method | Description                  |
|--------------|--------|------------------------------|
| `/health`    | GET    | Health check                 |
| `/ready`     | GET    | Readiness check              |
| `/predict`   | POST   | Make prediction              |
| `/docs`      | GET    | Swagger UI documentation     |

##Author
Chandrasekhar Sai Durga Gummadi
DevOps & Cloud Engineer | AIML Graduate
