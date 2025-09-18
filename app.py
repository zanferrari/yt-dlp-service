import os
import tempfile
from fastapi import FastAPI, Query
import yt_dlp

app = FastAPI()

@app.get("/")
def root():
    return {"message": "yt-dlp service running"}

@app.get("/info")
def get_info(url: str = Query(..., description="YouTube or supported video URL")):
    try:
        # Read cookies from environment variable
        cookies_content = os.environ.get("YTCOKIES", "")
        if not cookies_content:
            return {"error": "YTCOKIES environment variable not set"}

        # Write cookies to a temporary file
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
            f.write(cookies_content)
            cookies_file_path = f.name

        # yt-dlp options
        ydl_opts = {
            "quiet": True,
            "cookiefile": cookies_file_path,
            "noplaylist": True,
        }

        # Extract video info
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
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
