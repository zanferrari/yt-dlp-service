from fastapi import FastAPI, Query
import yt_dlp

app = FastAPI()

@app.get("/")
def root():
    return {"message": "yt-dlp service running"}

@app.get("/info")
def get_info(url: str = Query(..., description="Video URL")):
    try:
        with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "title": info.get("title"),
                "uploader": info.get("uploader"),
                "duration": info.get("duration"),
                "formats": [
                    {"format_id": f["format_id"], "ext": f["ext"], "resolution": f.get("resolution")}
                    for f in info.get("formats", [])
                ],
            }
    except Exception as e:
        return {"error": str(e)}

