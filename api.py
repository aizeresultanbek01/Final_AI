import os
from pathlib import Path

import pandas as pd
from functools import lru_cache

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from models.train_models import train_all_models
from models.bayes_model import predict_message
from models.ml_model import predict_ml_message

app = FastAPI(
    title="Qorgau AI API",
    description="Naive Bayes және Logistic Regression модельдері арқылы хабарламаларды жіктеу",
    version="1.0.0"
)

# For deployment, set FRONTEND_ORIGIN to the GitHub Pages origin.
frontend_origin = os.getenv("FRONTEND_ORIGIN", "*")
allowed_origins = ["*"] if frontend_origin == "*" else [frontend_origin.rstrip("/")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@lru_cache(maxsize=1)
def get_models():
    try:
        return train_all_models()
    except Exception as exc:
        raise RuntimeError(f"Модельдерді дайындау қатесі: {exc}") from exc

class MessageRequest(BaseModel):
    message: str = Field(min_length=1, max_length=3000)

@app.get("/")
def home():
    return {"service": "Qorgau AI API", "status": "online"}

@app.get("/api/health")
def health():
    try:
        bayes, logistic, metrics = get_models()
        return {
            "status": "ok",
            "models": ["Naive Bayes", "Logistic Regression"],
            "dataset_rows": int(len(pd.read_csv(Path(__file__).parent / "data" / "messages.csv"))),
            "metrics": metrics
        }
    except Exception as exc:
        raise HTTPException(status_code=503, detail=str(exc))

@app.post("/api/predict")
def predict(payload: MessageRequest):
    message = payload.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Хабарлама бос болмауы керек.")

    try:
        bayes, logistic, metrics = get_models()
        bayes_result = predict_message(bayes, message)
        logistic_result = predict_ml_message(logistic, message)

        same = bayes_result["category"] == logistic_result["category"]
        category = bayes_result["category"] if same else "unknown"

        return {
            "category": category,
            "agreement": same,
            "models": {
                "naive_bayes": bayes_result,
                "logistic_regression": logistic_result
            },
            "note": (
                "Екі модель бір санатты таңдады."
                if same else
                "Модельдердің нәтижесі әртүрлі. Қосымша тексеру қажет."
            )
        }
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Талдау қатесі: {exc}")
