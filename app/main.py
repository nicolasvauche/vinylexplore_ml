from fastapi import FastAPI
from .schemas import RecommendationRequest, Album
from .services import recommend_album

app = FastAPI()


@app.get("/")
async def api_home():
    return {
        "name": "VinyleXplore ML API",
        "status": "ok"
    }


@app.post("/recommend", response_model=Album)
async def get_recommendation(request: RecommendationRequest):
    return recommend_album(request)
