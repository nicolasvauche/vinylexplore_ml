import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from .schemas import RecommendationRequest, Album
from .services import recommend_album

load_dotenv()
API_TOKEN = os.getenv("ML_API_TOKEN")

app = FastAPI()


@app.get("/")
async def api_home():
    return {
        "name": "VinyleXplore ML API",
        "status": "ok"
    }


@app.post("/recommend", response_model=Album)
async def get_recommendation(request: RecommendationRequest, req: Request):
    auth_header = req.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")

    token = auth_header.split("Bearer ")[1]

    if token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return recommend_album(request)
