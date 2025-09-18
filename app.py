from fastapi import FastAPI, Query
import yt_dlp

app = FastAPI()

@app.get("/")
def root():
    return {"message": "yt-dlp public video service running"}

@app.get("/info")
def get_info(url: str = Query(..., description="Public video URL")):
    try:
        ydl_opts = {
            "quiet": True,
            "noplaylist": True,
            "ignoreerrors": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if not info:
                return {"error": "Video not available or restricted"}

            # Select best video+audio format
            best_stream = None
            best_audio = None
            for f in info.get("formats", []):
                # Best video+audio
                if f.get("vcodec") != "none" and f.get("acodec") != "none":
                    if best_stream is None or f.get("height", 0) > best_stream.get("height", 0):
                        best_stream = f
                # Best audio-only
                if f.get("acodec") != "none" and f.get("vcodec") == "none":
                    if best_audio is None or f.get("abr", 0) > best_audio.get("abr", 0):
                        best_audio = f

            return {
                "title": info.get("title"),
                "uploader": info.get("uploader"),
                "duration": info.get("duration"),
                "thumbnail": info.get("thumbnail"),
                "best_audio_url": best_audio.get("url") if best_audio else None,
                "best_stream_url": best_stream.get("url") if best_stream else None
            }

    except Exception as e:
        return {"error": str(e)}
