from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from src.sentiment_engine import generate_sentiment_report

app = FastAPI(title="AION Intelligence API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "status": "AION API is running",
        "endpoint": "/api/sentiment?q=Hormuz"
    }


@app.get("/api/sentiment")
def sentiment(q: str = Query(..., description="Search query for AION intelligence analysis")):
    report = generate_sentiment_report(q)
    return report