from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional, Union, Dict


# ===== REQUEST SCHEMA =====
class ModerationRequest(BaseModel):
    content: List[str] = Field(default_factory=list)
    pictures: List[HttpUrl] = Field(default_factory=list)
    videos: List[HttpUrl] = Field(default_factory=list)


# ===== PREDICTION RESULTS =====

# Picture prediction
class PicturePredicts(BaseModel):
    nude_score: float
    violence_score: float


class PicturePredictionResult(BaseModel):
    path: str
    isContainNude: bool
    isContainViolence: bool
    predicts: PicturePredicts


# Video prediction
class VideoPredictionResult(BaseModel):
    path: str
    type: str  # e.g., "This video contains NSFW content"
    timestamps: Dict[str, str]  # Example: {"0:00:01": "Nude"}


# ===== INDIVIDUAL RESULT ITEMS =====

class ContentResult(BaseModel):
    field: str = "content"
    offensive_words: List[str]


class MediaItem(BaseModel):
    source: HttpUrl
    predictions: Optional[Union[PicturePredictionResult, VideoPredictionResult]] = None
    error: Optional[str] = None


class MediaGroupResult(BaseModel):
    field: str  # "pictures" or "videos"
    results: List[MediaItem]


# ===== FULL RESPONSE SCHEMA =====

class ModerationResponse(BaseModel):
    data: List[Union[ContentResult, MediaGroupResult]]
