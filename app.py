from fastapi import FastAPI, Query
import yt_dlp

app = FastAPI()

@app.get("/")
def root():
    return {"message": "yt-dlp public video service running"}

@app.get("/info")
def get_info(url: str = Query(..., description="Public video URL")):
    try:
        # yt-dlp options for metadata only, no cookies
        ydl_opts = {
            "quiet": True,
            "format": "bestaudio/best",  # best audio fallback
            "noplaylist": True,
            "ignoreerrors": True,        # skip restricted videos
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if not info:
                return {"error": "Video not available or restricted"}

            # Find best audio
            best_audio = None
            for f in info.get("formats", []):
                if f.get("acodec") != "none" and (best_audio is None or f.get("abr",0) > best_audio.get("abr",0)):
                    best_audio = f

            return {
                "title": info.get("title"),
                "uploader": info.get("uploader"),
                "duration": info.get("duration"),
                "thumbnail": info.get("thumbnail"),
                "best_audio_url": best_audio.get("url") if best_audio else None,
                "stream_ur_
