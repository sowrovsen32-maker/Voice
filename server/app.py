"""
VoxFree TTS backend — free Microsoft Edge TTS proxy.
No API key needed. Run locally:  uvicorn app:app --host 0.0.0.0 --port 8000
"""
import os
from fastapi import FastAPI, Header, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import edge_tts

API_TOKEN = os.environ.get("API_TOKEN", "").strip()   # optional protection

app = FastAPI(title="VoxFree TTS API", version="1.0.0")

# Browser apps on a different origin (GitHub Pages, HopWeb) need these headers.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TTSRequest(BaseModel):
    text: str
    voice: str = "bn-BD-PradeepNeural"
    rate: str = "+0%"
    pitch: str = "+0Hz"
    volume: str = "+0%"


def check_token(token: str):
    if API_TOKEN and token != API_TOKEN:
        raise HTTPException(status_code=401, detail="bad or missing X-Api-Token")


async def synth(text: str, voice: str, rate: str, pitch: str, volume: str) -> bytes:
    try:
        comm = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch, volume=volume)
    except TypeError:
        # older edge-tts builds may not accept rate/pitch/volume keywords
        comm = edge_tts.Communicate(text, voice)
    buf = bytearray()
    async for chunk in comm.stream():
        if isinstance(chunk, dict) and chunk.get("type") == "audio":
            buf.extend(chunk["data"])
    return bytes(buf)


@app.get("/")
def root():
    return {"service": "VoxFree TTS API", "endpoints": ["GET /health", "GET /voices", "POST /tts"]}


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/voices")
async def voices():
    """Full free Edge TTS voice list (300+ voices)."""
    try:
        raw = await edge_tts.list_voices()
        out = [{
            "ShortName": v.get("ShortName", ""),
            "Gender": v.get("Gender", ""),
            "Locale": v.get("Locale", ""),
            "FriendlyName": v.get("FriendlyName", ""),
        } for v in raw]
        return {"voices": out}
    except Exception as exc:
        raise HTTPException(status_code=502, detail="voice list failed: %s" % exc)


@app.post("/tts")
async def tts(req: TTSRequest, x_api_token: str = Header(default="")):
    check_token(x_api_token)
    text = (req.text or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="text is required")
    if len(text) > 20000:
        raise HTTPException(status_code=400, detail="text too long (max 20000 chars)")
    try:
        audio = await synth(text, req.voice, req.rate, req.pitch, req.volume)
    except Exception as exc:
        raise HTTPException(status_code=502, detail="edge-tts failed: %s" % exc)
    if not audio:
        raise HTTPException(status_code=502, detail="edge-tts returned no audio")
    return Response(content=audio, media_type="audio/mpeg",
                    headers={"Cache-Control": "no-store"})
