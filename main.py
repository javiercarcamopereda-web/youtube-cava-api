from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

@app.get("/")
def root():
    return {"status": "API running"}
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

class ChannelRequest(BaseModel):
    channelId: str
    maxResults: int = 5

@app.post("/channelVideos")
def channel_videos(req: ChannelRequest):

    params = {
        "part": "snippet",
        "channelId": req.channelId,
        "type": "video",
        "order": "date",
        "maxResults": req.maxResults,
        "key": YOUTUBE_API_KEY,
    }

    r = requests.get(
        "https://www.googleapis.com/youtube/v3/search",
        params=params,
        timeout=30
    )

    data = r.json()

    videos = []

    for item in data.get("items", []):
        videos.append({
            "videoId": item["id"]["videoId"],
            "title": item["snippet"]["title"],
            "publishedAt": item["snippet"]["publishedAt"]
        })

    return {"videos": videos}
