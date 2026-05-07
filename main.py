from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp
import os
import uuid

app = FastAPI()

# Mamela ny Lovable hifandray amin'ity server ity
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DOWNLOAD_DIR = "downloads"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

@app.get("/convert")
async def convert_video(url: str):
    file_id = str(uuid.uuid4())
    output_template = f"{DOWNLOAD_DIR}/{file_id}.%(ext)s"
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_template,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            mp3_file = f"{DOWNLOAD_DIR}/{file_id}.mp3"
            
            # Mamerina ilay rakitra mp3 mivantana amin'ny browser
            return FileResponse(
                path=mp3_file, 
                filename=f"{info['title']}.mp3", 
                media_type='audio/mpeg'
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
