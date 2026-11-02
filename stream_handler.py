"""Audio & Text Stream Processing Service

DISCLAIMER & AI BEHAVIOR LABEL:
This service provides lightweight stream ingestion and mock real-time speech/text processing.
In this prototype environment:
1. Speech stream simulation generates realistic word token sequences with synthetic audio amplitude/waveform data.
2. Websocket connection simulates bidirectional real-time audio/text transport during assessment sessions.
3. Silence/pause detection flags hesitation and pacing intervals.
For a production deployment, this service interfaces directly with WebRTC media servers and
streaming ASR engines (e.g., Whisper Streaming or Deepgram).
"""

import asyncio
import random
import time
from typing import Dict, List, Any
from fastapi import WebSocket, WebSocketDisconnect


class LiveSessionManager:
    def __init__(self):
        # Maps session_id -> { "transcript_buffer": [], "start_time": float, "last_chunk_time": float }
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
        self.active_websockets: Dict[str, WebSocket] = {}

    def start_session(self, session_id: str, question_id: str) -> Dict[str, Any]:
        """Initialize a new live streaming assessment session."""
        now = time.time()
        self.active_sessions[session_id] = {
            "session_id": session_id,
            "question_id": question_id,
            "transcript_buffer": [],
            "start_time": now,
            "last_chunk_time": now,
            "pause_count": 0,
            "total_speech_duration_sec": 0.0,
            "status": "recording"
        }
        return self.active_sessions[session_id]

    def append_chunk(self, session_id: str, token: str, amplitude: float = 0.5) -> Dict[str, Any]:
        """Appends incoming token chunk to transcript buffer and detects silence cadence."""
        if session_id not in self.active_sessions:
            self.start_session(session_id, "default-q")

        session = self.active_sessions[session_id]
        now = time.time()
        delta = now - session["last_chunk_time"]

        # If gap between spoken tokens exceeds 1.8 seconds, flag as pause
        if delta > 1.8 and len(session["transcript_buffer"]) > 0:
            session["pause_count"] += 1

        session["transcript_buffer"].append(token)
        session["last_chunk_time"] = now
        session["total_speech_duration_sec"] = round(now - session["start_time"], 1)

        return {
            "session_id": session_id,
            "current_transcript": " ".join(session["transcript_buffer"]),
            "word_count": len(session["transcript_buffer"]),
            "pause_count": session["pause_count"],
            "amplitude": amplitude
        }

    def finalize_session(self, session_id: str) -> Dict[str, Any]:
        """Marks the session finalized and returns accumulated candidate transcript."""
        session = self.active_sessions.get(session_id)
        if not session:
            return {"session_id": session_id, "final_transcript": "", "word_count": 0}

        session["status"] = "completed"
        final_text = " ".join(session["transcript_buffer"]).strip()
        return {
            "session_id": session_id,
            "question_id": session.get("question_id"),
            "final_transcript": final_text,
            "word_count": len(session["transcript_buffer"]),
            "duration_seconds": session["total_speech_duration_sec"],
            "pause_count": session["pause_count"]
        }


session_manager = LiveSessionManager()


async def handle_websocket_session(websocket: WebSocket, session_id: str):
    """Handles WebSocket streaming connection for live audio/text processing."""
    await websocket.accept()
    session_manager.start_session(session_id, "ws-live-q")

    try:
        while True:
            data = await websocket.receive_json()
            event_type = data.get("type", "chunk")

            if event_type == "chunk":
                token = data.get("token", "")
                amp = data.get("amplitude", random.uniform(0.3, 0.85))
                updated = session_manager.append_chunk(session_id, token, amp)
                await websocket.send_json({
                    "type": "stream_update",
                    "data": updated
                })

            elif event_type == "finalize":
                summary = session_manager.finalize_session(session_id)
                await websocket.send_json({
                    "type": "session_finalized",
                    "data": summary
                })
                break

            elif event_type == "ping":
                await websocket.send_json({"type": "pong", "timestamp": time.time()})

    except WebSocketDisconnect:
        session_manager.finalize_session(session_id)
    except Exception as e:
        await websocket.send_json({"type": "error", "message": str(e)})
        session_manager.finalize_session(session_id)
