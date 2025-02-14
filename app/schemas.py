from pydantic import BaseModel, field_validator
from typing import List, Optional


class Context(BaseModel):
    dayOfWeek: str
    timeOfDay: str
    season: str
    mood: Optional[str] = None
    location: Optional[str] = None


class ListeningContext(BaseModel):
    dayOfWeek: str
    timeOfDay: str
    season: str
    location: Optional[str] = None
    status: Optional[str] = None
    choiceAt: Optional[int] = None


class Album(BaseModel):
    id: int
    moods: Optional[List[str]] = None
    genre: str
    style: Optional[str] = None
    playCount: Optional[int] = 0
    lastPlayedAt: Optional[int] = None
    listeningHistory: Optional[List[ListeningContext]] = None
    ignoredCount: Optional[int] = 0
    listenedCount: Optional[int] = 0

    @field_validator("listeningHistory", mode="before")
    @classmethod
    def convert_null_listening_history(cls, v):
        return v if v is not None else []


class RecommendationRequest(BaseModel):
    context: Context
    albums: List[Album]
