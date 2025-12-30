# src/app.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os

from src.pipeline import run_pipeline
from src.report_generator import save_html_report, make_safe_filename


# ---------------------------------------------------
# FASTAPI INITIALIZATION
# ---------------------------------------------------
app = FastAPI(
    title="YouTube Fact Checker API",
    description="Uploads a YouTube URL or local transcript and returns a structured fact-check report.",
    version="1.0.0"
)


# ---------------------------------------------------
# ENABLE CORS FOR STREAMLIT FRONTEND
# ---------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------
# REQUEST BODY SCHEMA
# ---------------------------------------------------
class CheckRequest(BaseModel):
    url: str
    save_report: Optional[bool] = False  # default false


# ---------------------------------------------------
# HEALTH CHECK ENDPOINT
# ---------------------------------------------------
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "YouTube Fact Checker API is running!"}


# ---------------------------------------------------
# MAIN FACT CHECK ENDPOINT
# ---------------------------------------------------
@app.post("/check")
def check_video(req: CheckRequest):
    """
    Accepts a YouTube URL OR local transcript path.
    Runs full pipeline and optionally saves HTML report.
    """

    video_input = req.url.strip()
    print(f"[API] Received input: {video_input}")

    try:
        report = run_pipeline(video_input)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline failed: {e}")

    saved_report_path = None
    if req.save_report:
        try:
            os.makedirs("reports", exist_ok=True)
            safe_name = make_safe_filename(video_input)
            out_path = f"reports/report_{safe_name}.html"
            saved_report_path = save_html_report(report, out_path)
        except Exception as e:
            saved_report_path = f"Failed to save HTML report: {e}"

    return {
        "status": "ok",
        "report": report,
        "saved_report": saved_report_path
    }


# ---------------------------------------------------
# ROOT ENDPOINT
# ---------------------------------------------------
@app.get("/")
def root():
    return {
        "status": "ok",
        "usage": "POST /check with JSON: { 'url': 'VIDEO_URL', 'save_report': true }"
    }


# ---------------------------------------------------
# LOCAL DEVELOPMENT SERVER
# ---------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    # Correct module path: src.app
    uvicorn.run("src.app:app", host="0.0.0.0", port=8000, reload=True)
