import os
import json
from typing import List, Optional
from fastapi import FastAPI, WebSocket, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware

import schemas
from sentiment_analyzer import analyze_sentiment_and_tone
from evaluation_engine import run_full_evaluation
from question_generator import generate_interview_questions
from stream_handler import session_manager, handle_websocket_session

app = FastAPI(
    title="AI Mock Interview Test System API",
    description="NLP-powered interview response generation, sentiment analysis, audio/text stream processing, and answer scoring.",
    version="1.0.0"
)

# CORS configuration
origins = os.getenv("CORS_ORIGINS", "http://localhost:5174,http://localhost:5173,http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", tags=["System"])
def health_check():
    return {
        "status": "healthy",
        "service": "AI Mock Interview Test Engine",
        "version": "1.0.0",
        "ai_engine_mode": "Prototype & Statistical NLP (Explainable scoring & dynamic JD parsing)"
    }


# --- Sample Data Endpoints ---
@app.get("/api/jobs/samples", tags=["Job Descriptions"])
def get_sample_job_descriptions():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample_job_descriptions.json")
    if os.path.exists(data_path):
        with open(data_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


@app.get("/api/benchmarks/samples", tags=["Evaluation Benchmarks"])
def get_sample_benchmarks():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample_evaluation_benchmark.json")
    if os.path.exists(data_path):
        with open(data_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


# --- Dynamic Question Generation ---
@app.post("/api/questions/generate", response_model=schemas.GenerateQuestionsResponse, tags=["Questions"])
def generate_questions(payload: schemas.JobDescriptionRequest):
    return generate_interview_questions(payload)


# --- Automated Answer Evaluation & Scoring ---
@app.post("/api/evaluations/score", response_model=schemas.EvaluationResult, tags=["Evaluations"])
def score_candidate_answer(submission: schemas.AnswerSubmission):
    if not submission.candidate_answer or not submission.candidate_answer.strip():
        raise HTTPException(status_code=400, detail="Candidate answer cannot be empty.")
    return run_full_evaluation(submission)


# --- Sentiment & Tone Analysis Standalone ---
@app.post("/api/evaluations/sentiment", tags=["Evaluations"])
def analyze_sentiment(text: str = Body(..., embed=True)):
    return analyze_sentiment_and_tone(text)


# --- Stream Processing REST Emulation ---
@app.post("/api/sessions/start", tags=["Live Stream Processing"])
def start_live_session(session_id: str = Body(..., embed=True), question_id: str = Body("default-q", embed=True)):
    return session_manager.start_session(session_id, question_id)


@app.post("/api/sessions/chunk", tags=["Live Stream Processing"])
def post_stream_chunk(chunk: schemas.StreamChunk):
    return session_manager.append_chunk(chunk.session_id, chunk.token, chunk.mock_audio_amplitude or 0.5)


@app.post("/api/sessions/finalize", tags=["Live Stream Processing"])
def finalize_live_session(session_id: str = Body(..., embed=True)):
    return session_manager.finalize_session(session_id)


# --- Real-Time Audio / Text WebSocket Stream ---
@app.websocket("/api/ws/session/{session_id}")
async def websocket_session_endpoint(websocket: WebSocket, session_id: str):
    await handle_websocket_session(websocket, session_id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
